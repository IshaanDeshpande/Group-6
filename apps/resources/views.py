from django.shortcuts import render
from rest_framework import viewsets


def find_resources(request):
    return render(request, 'resources/find_resources.html')


class ResourceViewSet(viewsets.ModelViewSet):
    pass
