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

from apps.resources.views import _search_211_colorado

CURATED_VOLUNTEER_FACTS = """
Awards:
- American Volunteer Service Award: This award is offered to individuals who reach a certain number of service hours in 12 months. Learn more: https://volunteerscholars.org/avsa/
- National Service Honor: This award tracks and awards cumulative volunteer milestones for individuals. Learn more: https://www.nationalservicehonor.org

Feel good:
- According to the Mayo Clinic (https://www.mayoclinichealthsystem.org/hometown-health/speaking-of-health/3-health-benefits-of-volunteering), participating in volunteering was shown to improve physical and mental health, provide a sense of purpose, and strengthen relationships.

Volunteer hours:
- When you volunteer, you can log your hours. Volunteer hours can be very beneficial, as they can look good on college applications and resumes. Volunteering can also lead to learning new skills that can help in your career.

Socialize/meet people:
- Volunteering can help to make connections with people that you're helping and people that you're working with.
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


def _estimate_tokens(text):
    return max(1, len(re.findall(r'\b\w+\b', text or '')))


def _message_token_count(message):
    content = message.get('content', '') if isinstance(message, dict) else ''
    role = message.get('role', '') if isinstance(message, dict) else ''
    return _estimate_tokens(str(role)) + _estimate_tokens(str(content)) + 4


def _trim_text_to_tokens(text, max_tokens):
    if max_tokens <= 0:
        return ''

    tokens = re.findall(r'\b\w+\b|[^\w\s]+', text or '')
    if len(tokens) <= max_tokens:
        return text or ''

    trimmed_tokens = tokens[:max_tokens]
    trimmed_text = ' '.join(trimmed_tokens)
    return re.sub(r'\s+([.,!?;:])', r'\1', trimmed_text)


def _fit_messages_to_token_budget(messages, max_tokens=1000):
    if not messages:
        return messages

    system_messages = [message for message in messages if message.get('role') == 'system']
    non_system_messages = [message for message in messages if message.get('role') != 'system']

    fitted_messages = list(system_messages)
    fitted_total = sum(_message_token_count(message) for message in fitted_messages)

    if not non_system_messages:
        return fitted_messages

    user_message = non_system_messages[-1]
    history_messages = non_system_messages[:-1]

    user_tokens = _message_token_count(user_message)
    if user_tokens >= max_tokens:
        user_message = {
            **user_message,
            'content': _trim_text_to_tokens(user_message.get('content', ''), max_tokens // 2),
        }
        user_tokens = _message_token_count(user_message)

    available_for_history = max_tokens - fitted_total - user_tokens
    if available_for_history < 0:
        available_for_history = 0

    trimmed_history = []
    history_budget_used = 0
    for message in reversed(history_messages):
        message_tokens = _message_token_count(message)
        if history_budget_used + message_tokens > available_for_history:
            break
        trimmed_history.append(message)
        history_budget_used += message_tokens

    trimmed_history.reverse()
    fitted_messages.extend(trimmed_history)
    fitted_messages.append(user_message)

    total_tokens = sum(_message_token_count(message) for message in fitted_messages)
    if total_tokens <= max_tokens:
        return fitted_messages

    context_index = next(
        (
            index
            for index, message in enumerate(fitted_messages)
            if message.get('role') == 'system' and message.get('content', '').startswith('Context:\n')
        ),
        None,
    )
    if context_index is not None:
        context_message = fitted_messages[context_index]
        overhead_tokens = total_tokens - _message_token_count(context_message)
        remaining_for_context = max_tokens - overhead_tokens
        if remaining_for_context > 0:
            context_body = context_message.get('content', '')[len('Context:\n'):]
            trimmed_context = _trim_text_to_tokens(context_body, remaining_for_context)
            fitted_messages[context_index] = {
                **context_message,
                'content': f'Context:\n{trimmed_context}',
            }

    return fitted_messages


def _is_homelessness_related_ai(user_message, api_key, api_url, model):
    """Use AI to classify if the message is about homelessness/housing support."""
    classification_prompt = {
        'model': model,
        'messages': [
            {
                'role': 'system',
                'content': (
                    'You are a topic classifier for ResourceConnect, a website about homelessness support and volunteering. '
                    'Respond with ONLY "YES" or "NO". '
                    'YES if the question relates to: homelessness, housing, shelters, poverty, social services, '
                    'volunteering, charitable work, emergency assistance, health services, employment assistance, '
                    'helping vulnerable populations, getting involved with causes, benefits of volunteering, '
                    'or finding/providing resources to people in need. '
                    'YES if it asks about ResourceConnect itself, how to help, or what we do. '
                    'NO only for completely unrelated topics (sports, cooking, weather, movies, math homework, etc). '
                    'When in doubt, answer YES - it is better to try to help than to turn someone away.'
                ),
            },
            {'role': 'user', 'content': user_message},
        ],
        'temperature': 0.0,
        'max_tokens': 5,
    }

    req = urllib.request.Request(
        api_url,
        data=json.dumps(classification_prompt).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            classification = (result.get('choices', [{}])[0].get('message', {}).get('content', 'YES')).strip().upper()
            return 'YES' in classification
    except Exception:
        # If classification fails, be permissive and allow the message
        return True


@lru_cache(maxsize=1)
def _load_site_documents():
    return [
        {
            'title': 'ResourceConnect Mission',
            'text': (
                'ResourceConnect is dedicated to supporting individuals experiencing homelessness by '
                'connecting them with shelter, housing assistance, food banks, mental health services, '
                'job training, healthcare, and other critical support resources. We help vulnerable '
                'communities access emergency services and long-term solutions.'
            ),
            'tokens': _tokenize('ResourceConnect homelessness shelter housing assistance resources vulnerable emergency support'),
        },
        {
            'title': 'Volunteer Awards And Benefits',
            'text': (
                'Volunteering to help people experiencing homelessness can improve physical and mental health, '
                'give a sense of purpose, strengthen relationships, help build skills, and support resumes. '
                'Awards include the American Volunteer Service Award and the National Service Honor.'
            ),
            'tokens': _tokenize(CURATED_VOLUNTEER_FACTS),
        },
        {
            'title': 'Get Involved',
            'text': (
                'ResourceConnect suggests starting with the quiz or learning page to understand homelessness, '
                'then finding local volunteer opportunities with shelter organizations, food banks, or housing nonprofits.'
            ),
            'tokens': _tokenize('ResourceConnect Get Involved volunteer homelessness shelter housing food bank nonprofit organizations'),
        },
        {
            'title': 'Find Resources',
            'text': (
                'ResourceConnect helps users find nearby support resources including shelters, emergency housing, '
                'food assistance, healthcare, mental health services, job training, and other community support hubs.'
            ),
            'tokens': _tokenize('ResourceConnect find resources shelter housing emergency food healthcare mental health job training support'),
        },
    ]


def _build_grounding_context(user_message, max_docs=1):
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

    selected_docs = selected_docs[:max_docs]

    sections = [f"{doc['title']}: {doc['text']}" for doc in selected_docs]
    return '\n\n'.join(sections)

def home(request):
    return render(request, 'core/home.html')

def get_involved(request):
    search_query = (request.GET.get('q') or '').strip()
    results = []
    total_results = 0
    search_error = ''

    if search_query:
        try:
            results, total_results = _search_211_colorado(search_query)
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, ValueError, json.JSONDecodeError):
            search_error = 'Unable to reach the 2-1-1 Colorado database right now.'

    favorited_names = []
    if request.user.is_authenticated:
        favorited_names = list(request.user.favorites.values_list('name', flat=True))

    return render(
        request,
        'core/get_involved.html',
        {
            'active_tab': 'main',
            'search_query': search_query,
            'results': results,
            'total_results': total_results,
            'search_error': search_error,
            'favorited_names': favorited_names,
        },
    )

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

    # Extract conversation history if provided
    conversation_history = payload.get('history') or []

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
    grounding_context = _trim_text_to_tokens(grounding_context, 220)

    # Check if message is homelessness-related using AI classification
    if not _is_homelessness_related_ai(user_message, api_key, api_url, model):
        return JsonResponse({
            'error': 'I can only help with questions related to homelessness support and resources. '
                     'Please ask me a question about housing, shelters, social services, or volunteering to help people in need.'
        }, status=400)

    # Build messages with conversation history
    messages = [
        {
            'role': 'system',
            'content': (
                'You are a helpful assistant for ResourceConnect, a website dedicated to supporting '
                'individuals experiencing homelessness. You ONLY answer questions related to homelessness, '
                'housing, shelter, support resources, volunteering, or how to help people in need. '
                'If a question is not related to these topics, politely decline and redirect the user to '
                'homelessness-related resources. Use the provided context to give accurate answers. '
                'Be concise and compassionate.'
            ),
        },
        {
            'role': 'system',
            'content': f'Context:\n{grounding_context}',
        },
    ]
    
    # Add conversation history (previous exchanges)
    for history_msg in conversation_history:
        messages.append({
            'role': history_msg.get('role', 'user'),
            'content': history_msg.get('content', '')
        })
    
    # Add current user message
    messages.append({'role': 'user', 'content': user_message})

    request_body = {
        'model': model,
        'messages': _fit_messages_to_token_budget(messages, max_tokens=1000),
        'temperature': 0.2,
    }

    req = urllib.request.Request(
        api_url,
        data=json.dumps(request_body).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
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
    except (TimeoutError, Exception) as err:
        return JsonResponse({'error': f'Unable to reach AI provider. {type(err).__name__}: {str(err)[:100]}'}, status=502)

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
