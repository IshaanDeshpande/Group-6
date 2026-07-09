from django.urls import path

from . import views

app_name = 'resources'
urlpatterns = [
    path('', views.find_resources, name='find_resources'),
    path('map/', views.find_resources_map, name='find_resources_map'),
    path('personalized-help/', views.find_resources_personalized, name='find_resources_personalized'),
]
