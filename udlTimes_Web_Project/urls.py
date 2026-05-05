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

from udltimes.views import (
    SignUpView,
    api_connections_complete,
    api_connections_guess,
    api_connections_today,
    api_framed_guess,
    api_framed_today,
    api_wordle_guess,
    api_wordle_today,
    connections_view,
    framed_view,
    home,
    login_view,
    profile_view,
    register_view,
    wordle_view,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('wordle/', wordle_view, name='wordle'),
    path('connections/', connections_view, name='connections'),
    path('framed/', framed_view, name='framed'),
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', login_view, name='login'),
    path("accounts/register/", register_view, name="register"),
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('api/wordle/today/', api_wordle_today, name='api_wordle_today'),
    path('api/wordle/today/guess/', api_wordle_guess, name='api_wordle_guess'),
    path('api/connections/today/', api_connections_today, name='api_connections_today'),
    path('api/connections/today/guess/', api_connections_guess, name='api_connections_guess'),
    path('api/connections/today/complete/', api_connections_complete, name='api_connections_complete'),
    path('api/framed/today/', api_framed_today, name='api_framed_today'),
    path('api/framed/today/guess/', api_framed_guess, name='api_framed_guess'),
]
