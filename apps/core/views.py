from django.shortcuts import render

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

def why_it_matters(request):
    return render(request, 'core/why_it_matters.html')

def about(request):
    return render(request, 'core/about.html')

def success_stories(request):
    return render(request, 'core/success_stories.html')
