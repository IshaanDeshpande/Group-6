from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def get_involved(request):
    return render(request, 'core/get_involved.html')

def why_it_matters(request):
    return render(request, 'core/why_it_matters.html')

def about(request):
    return render(request, 'core/about.html')
