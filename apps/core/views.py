import json
import re
import urllib.error
import urllib.request
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

CURATED_VOLUNTEER_FACTS = """
Awards:
- American Volunteer Service Award: offered to individuals who reach a certain number of service hours in 12 months.
  Learn more: https://volunteerscholars.org/avsa/
- National Service Honor: tracks and awards cumulative volunteer milestones for individuals.
  Learn more: https://www.nationalservicehonor.org

Benefits of volunteering:
- According to Mayo Clinic, volunteering can improve physical and mental health,
  provide a sense of purpose, and strengthen relationships.
  Source: https://www.mayoclinichealthsystem.org/hometown-health/speaking-of-health/3-health-benefits-of-volunteering
- Volunteer hours can support college applications and resumes.
- Volunteering can help people build new skills for career growth.
- Volunteering helps people socialize and build connections with those they help
  and those they volunteer alongside.
""".strip()


def _strip_template_markup(html_text):
    text = re.sub(r'{%.*?%}', ' ', html_text, flags=re.DOTALL)
    text = re.sub(r'{{.*?}}', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<script.*?</script>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _tokenize(text):
    return {tok for tok in re.findall(r'[a-zA-Z]{3,}', text.lower())}


@lru_cache(maxsize=1)
def _load_site_documents():
    templates_root = Path(settings.BASE_DIR) / 'templates'
    candidate_dirs = [
        templates_root / 'core',
        templates_root / 'resources',
        templates_root / 'users',
    ]

    docs = []
    for directory in candidate_dirs:
        if not directory.exists():
            continue

        for html_file in directory.glob('*.html'):
            try:
                raw_text = html_file.read_text(encoding='utf-8', errors='ignore')
            except OSError:
                continue

            cleaned = _strip_template_markup(raw_text)
            if not cleaned:
                continue

            docs.append(
                {
                    'title': html_file.stem.replace('_', ' ').title(),
                    'text': cleaned[:2200],
                    'tokens': _tokenize(cleaned),
                }
            )

    docs.append(
        {
            'title': 'Volunteer Awards And Benefits',
            'text': CURATED_VOLUNTEER_FACTS,
            'tokens': _tokenize(CURATED_VOLUNTEER_FACTS),
        }
    )

    return docs


def _build_grounding_context(user_message, max_docs=6):
    docs = _load_site_documents()
    query_tokens = _tokenize(user_message)
    scored = []

    for doc in docs:
        overlap = len(query_tokens & doc['tokens'])
        priority_bonus = 2 if doc['title'] == 'Volunteer Awards And Benefits' else 0
        scored.append((overlap + priority_bonus, doc))

    scored.sort(key=lambda item: item[0], reverse=True)
    selected_docs = [doc for score, doc in scored if score > 0][:max_docs]
    if not selected_docs:
        selected_docs = docs[:2]

    sections = [f"{doc['title']}: {doc['text']}" for doc in selected_docs]
    return '\n\n'.join(sections)

def home(request):
    return render(request, 'core/home.html')

def get_involved(request):
    search_query = request.GET.get('q', '')
    return render(request, 'core/get_involved.html', {'active_tab': 'main', 'search_query': search_query})

def get_involved_learn(request):
    return render(request, 'core/get_involved_learn.html', {'active_tab': 'learn'})

def get_involved_quiz(request):
    return render(request, 'core/get_involved_quiz.html', {'active_tab': 'quiz'})

def chatbot(request):
    return render(request, 'core/chatbot.html')


@require_POST
def chatbot_message(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    user_message = (payload.get('message') or '').strip()
    if not user_message:
        return JsonResponse({'error': 'Message is required.'}, status=400)

    api_key = getattr(settings, 'AI_API_KEY', '')
    api_url = getattr(settings, 'AI_API_URL', 'https://api.openai.com/v1/chat/completions')
    model = getattr(settings, 'AI_MODEL', 'gpt-4o-mini')

    parsed_api_url = urlparse(api_url)
    if parsed_api_url.hostname == 'localhost':
        api_url = api_url.replace('://localhost', '://127.0.0.1', 1)

    if not api_key:
        return JsonResponse(
            {'error': 'AI chatbot is not configured. Set AI_API_KEY in your .env file.'},
            status=500,
        )

    grounding_context = _build_grounding_context(user_message)

    request_body = {
        'model': model,
        'messages': [
            {
                'role': 'system',
                'content': (
                    'You are a helpful assistant for ResourceConnect. '
                    'Focus on homelessness support resources and ways users can get involved. '
                    'Use the supplied context from the ResourceConnect website and volunteer facts '
                    'to answer. If an answer is not in context, say you are not sure and suggest '
                    'relevant ResourceConnect pages the user can check.'
                ),
            },
            {
                'role': 'system',
                'content': f'Context:\n{grounding_context}',
            },
            {'role': 'user', 'content': user_message},
        ],
        'temperature': 0.4,
    }

    req = urllib.request.Request(
        api_url,
        data=json.dumps(request_body).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        method='POST',
    )

    request_timeout = getattr(settings, 'AI_TIMEOUT_SECONDS', 180)

    try:
        with urllib.request.urlopen(req, timeout=request_timeout) as response:
            response_data = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as err:
        detail = err.read().decode('utf-8', errors='ignore')
        return JsonResponse({'error': f'AI provider error: {detail or err.reason}'}, status=502)
    except urllib.error.URLError as err:
        reason = str(getattr(err, 'reason', err))
        return JsonResponse({'error': f'Unable to reach AI provider. {reason}'}, status=502)
    except TimeoutError:
        return JsonResponse({'error': 'Unable to reach AI provider. Request timed out.'}, status=502)

    ai_reply = ''
    choices = response_data.get('choices') or []
    if choices:
        ai_reply = (choices[0].get('message') or {}).get('content', '').strip()

    if not ai_reply:
        return JsonResponse({'error': 'AI provider returned an empty response.'}, status=502)

    return JsonResponse({'reply': ai_reply})

def why_it_matters(request):
    return render(request, 'core/why_it_matters.html')

def about(request):
    return render(request, 'core/about.html')

def success_stories(request):
    return render(request, 'core/success_stories.html')
