from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('get-involved/', views.get_involved, name='get_involved'),
    path('get-involved/learn/', views.get_involved_learn, name='get_involved_learn'),
    path('get-involved/quiz/', views.get_involved_quiz, name='get_involved_quiz'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('why-it-matters/', views.why_it_matters, name='why_it_matters'),
    path('about/', views.about, name='about'),
    path('success-stories/', views.success_stories, name='success_stories'),
]
