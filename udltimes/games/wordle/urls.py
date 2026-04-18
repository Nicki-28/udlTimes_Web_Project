from django.urls import path
from . import views

urlpatterns = [
    path('', views.wordle_page, name='wordle'),
    path('check-guess/', views.check_guess, name='check_guess'),
    path('daily/', views.dailyWordle, name='dailyWordle'),
]