from django.shortcuts import render
from rest_framework import viewsets


def find_resources(request):
    return render(request, 'resources/find_resources.html', {'active_tab': 'main'})

def find_resources_map(request):
    return render(request, 'resources/find_resources_map.html', {'active_tab': 'map'})

def find_resources_personalized(request):
    return render(request, 'resources/find_resources_personalized.html', {'active_tab': 'personalized'})


class ResourceViewSet(viewsets.ModelViewSet):
    pass
