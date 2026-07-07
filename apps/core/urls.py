from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('get-involved/', views.get_involved, name='get_involved'),
]
