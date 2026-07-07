from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def get_involved(request):
    return render(request, 'core/get_involved.html')
