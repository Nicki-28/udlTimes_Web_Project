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
from django.urls import path, include

from udltimes.views import SignUpView, home, wordle_view, connections_view, framed_view, register_view, login_view, profile_view
from django.contrib.auth.views import LogoutView
from udltimes.games.wordle.views import check_guess,dailyWordle

urlpatterns = [
    path('wordle/', wordle_view, name='wordle'),
    path('wordle/check-guess/', check_guess, name='check_guess'),
    path('connections/', connections_view, name='connections'),
    path('framed/', framed_view, name='framed'),
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', login_view, name='login'),
    path("accounts/register/", register_view, name="register"),
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('wordle/daily/', dailyWordle, name='dailyWordle'),
]
