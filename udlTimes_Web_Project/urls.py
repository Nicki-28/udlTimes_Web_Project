"""
URL configuration for udlTimes_Web_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from udltimes.views import WordleCreateView, WordleUpdateView, WordleDeleteView, custom_wordle_view

from udltimes.views import (
    SignUpView,
    api_connections_complete,
    api_connections_guess,
    api_connections_today,
    api_framed_guess,
    api_framed_today,
    api_wordle_guess,
    api_wordle_today,
    connections_save_view,
    connections_view,
    framed_api,
    framed_autocomplete,
    framed_save_api,
    framed_view,
    home,
    login_view,
    profile_view,
    register_view,
    wordle_view,
    WordleCreateView,
    WordleDeleteView,
    WordleUpdateView
)
from django.contrib.auth.views import LogoutView
from udltimes.wordle.views import check_guess,dailyWordle

urlpatterns = [
    path('wordle/', wordle_view, name='wordle'),
    path('wordle/check-guess/', check_guess, name='check_guess'),
    path('connections/', connections_view, name='connections'),
    path('framed/', framed_view, name='framed'),
    path('api/framed/', framed_api, name='framed-api'),
    path('api/framed/save/', framed_save_api, name='framed_save_api'),
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('connections/save/', connections_save_view, name='connections_save'),
    path('accounts/login/', login_view, name='login'),
    path("accounts/register/", register_view, name="register"),
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('wordle/daily/', dailyWordle, name='dailyWordle'),
    path('framed/movie-autocomplete/', framed_autocomplete, name='framed autocomplete'),
    path('api/wordle/today/', api_wordle_today, name='api_wordle_today'),
    path('api/wordle/today/guess/', api_wordle_guess, name='api_wordle_guess'),
    path('api/connections/today/', api_connections_today, name='api_connections_today'),
    path('api/connections/today/guess/', api_connections_guess, name='api_connections_guess'),
    path('api/connections/today/complete/', api_connections_complete, name='api_connections_complete'),
    path('api/framed/today/', api_framed_today, name='api_framed_today'),
    path('api/framed/today/guess/', api_framed_guess, name='api_framed_guess'),
    path('wordle/new/', WordleCreateView.as_view(), name='wordle_create'),
    path('wordle/<slug:pk>/edit/', WordleUpdateView.as_view(), name='wordle_update'),
    path('wordle/<slug:pk>/delete/', WordleDeleteView.as_view(), name='wordle_delete'),
    path('wordle/play/<int:pk>/', custom_wordle_view, name='play_custom_wordle'),
    path('wordle/edit/<int:pk>/', WordleUpdateView.as_view(), name='wordle_edit'),
    path('wordle/delete/<int:pk>/', WordleDeleteView.as_view(), name='wordle_delete'),
]
