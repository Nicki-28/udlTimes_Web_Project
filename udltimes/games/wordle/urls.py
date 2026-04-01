from django.urls import path
from . import views

urlpatterns = [
    path('', views.wordle_view, name='wordle_view'),

    path('check-guess/', views.check_guess, name='check_guess'),
]