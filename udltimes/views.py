import json
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.db.models import Count, Q, Sum
from udltimes.models import StatsWordle, StatsFramed, StatsConnections, Connections
from django.conf import settings
from django.utils import timezone


def wordle_view(request):
    return render(request, 'wordle.html')

@login_required
def connections_view(request):
    return render(request, 'connections/connections.html')


@require_POST
def connections_save_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=401)

    try:
        data = json.loads(request.body)

        # le pedimos al Frontend que nos envíe directamente las vidas restantes (1, 2, 3 o 4)
        vidas_restantes = data.get("vidas", 0)
        completed = data.get("completed", False)

        # puntuacion simple: si ganó, multiplica vidas por 100. Si perdió o hizo trampas con vidas < 0, 0 puntos.
        points = (vidas_restantes * 100) if completed and vidas_restantes > 0 else 0

        today = timezone.now().date()

        # buscamos el puzzle de hoy
        game = Connections.objects.filter(date=today).first()
        if not game:
            return JsonResponse({"error": "No puzzle today"}, status=404)

        # guardamos la estadística
        stat, created = StatsConnections.objects.get_or_create(
            user=request.user,
            game=game,
            defaults={"completed": completed, "points": points}
        )

        # si ya había jugado (quizás la refrescó sin querer) y ahora tiene más puntos (o la primera no la guardó como completa), la actualizamos
        if not created and stat.points < points:
            stat.completed = completed
            stat.points = points
            stat.save()

        return JsonResponse({"points": points, "success": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def framed_view(request):
    return render(request, 'framed.html')


def home(request):
    ee_user = getattr(settings, 'EE_USER', '')

    wordle_leaderboard = (
        StatsWordle.objects
        .filter(completed=True)
        .values('user__username')
        .annotate(wins=Count('id'))
        .order_by('-wins')[:3]
    )
    wordle_leaderboard = [
        {'username': e['user__username'], 'wins': e['wins']}
        for e in wordle_leaderboard
    ]

    connections_leaderboard = (
        StatsConnections.objects
        .filter(completed=True)
        .values('user__username')
        .annotate(points=Sum('points'))
        .order_by('-points')[:3]
    )
    connections_leaderboard = [
        {'username': e['user__username'], 'points': e['points']}
        for e in connections_leaderboard
    ]

    framed_leaderboard = (
        StatsFramed.objects
        .values('user__username')
        .annotate(streaks=Count('id'))
        .order_by('-streaks')[:3]
    )
    framed_leaderboard = [
        {'username': e['user__username'], 'streaks': e['streaks']}
        for e in framed_leaderboard
    ]

    context = {
        'ee_user': ee_user,
        'wordle_leaderboard': wordle_leaderboard,
        'connections_leaderboard': connections_leaderboard,
        'framed_leaderboard': framed_leaderboard,
    }
    return render(request, 'home.html', context)


def login_view(request):
    ee_user = getattr(settings, 'EE_USER', '')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        captcha_ok = request.POST.get('captcha_ok', '0')

        form = AuthenticationForm(data=request.POST)

        if username == ee_user and captcha_ok != '1':
            return render(request, 'home.html', {
                'form': form,
                'captcha_error': True,
                'ee_user': ee_user,
                'show_login_modal': True,
            })

        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')

        return render(request, 'home.html', {
            'form': form,
            'ee_user': ee_user,
            'show_login_modal': True,
        })

    return render(request, 'home.html', {
        'form': AuthenticationForm(),
        'ee_user': ee_user,
    })


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")

        if not username or not password:
            return render(request, "home.html", {
                "register_error": "Username and password are required.",
                "register_username": username,
                "register_email": email,
                "show_register_modal": True
            })

        if User.objects.filter(username=username).exists():
            return render(request, "home.html", {
                "register_error": "Username already exists.",
                "register_username": username,
                "register_email": email,
                "show_register_modal": True
            })

        if len(password) < 8:
            return render(request, "home.html", {
                "register_error": "Password must be at least 8 characters.",
                "register_username": username,
                "register_email": email,
                "show_register_modal": True
            })

        if not re.search(r"\d", password):
            return render(request, "home.html", {
                "register_error": "Password must contain at least one number.",
                "register_username": username,
                "register_email": email,
                "show_register_modal": True
            })

        if not re.search(r"[A-Za-z]", password):
            return render(request, "home.html", {
                "register_error": "Password must contain at least one letter.",
                "register_username": username,
                "register_email": email,
                "show_register_modal": True
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if full_name:
            user.first_name = full_name
            user.save()

        login(request, user)
        return redirect("home")

    return redirect("home")


@login_required
def profile_view(request):
    user = request.user
    success_message = None
    error_message = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_name":
            full_name = request.POST.get("full_name", "").strip()
            user.first_name = full_name
            user.save()
            success_message = "Name updated successfully."

        elif action == "update_password":
            current_password = request.POST.get("current_password", "")
            new_password = request.POST.get("new_password", "")
            confirm_password = request.POST.get("confirm_password", "")

            if not user.check_password(current_password):
                error_message = "Current password is incorrect."
            elif new_password != confirm_password:
                error_message = "New passwords do not match."
            elif len(new_password) < 8:
                error_message = "Password must be at least 8 characters."
            elif not re.search(r"\d", new_password):
                error_message = "Password must contain at least one number."
            elif not re.search(r"[A-Za-z]", new_password):
                error_message = "Password must contain at least one letter."
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                success_message = "Password updated successfully."

    wordle_wins = StatsWordle.objects.filter(user=user, completed=True).count()
    wordle_played = StatsWordle.objects.filter(user=user).count()

    connections_wins = StatsConnections.objects.filter(user=user, completed=True).count()
    connections_played = StatsConnections.objects.filter(user=user).count()

    framed_played = StatsFramed.objects.filter(user=user).count()

    context = {
        'wordle_wins': wordle_wins,
        'wordle_played': wordle_played,
        'connections_wins': connections_wins,
        'connections_played': connections_played,
        'framed_played': framed_played,
        'success_message': success_message,
        'error_message': error_message,
    }
    return render(request, 'registration/profile.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
