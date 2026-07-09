from django.urls import path

from . import views

app_name = 'resources'
urlpatterns = [
    path('', views.find_resources, name='find_resources'),
]
