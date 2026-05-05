import json
import random
import re
import unicodedata

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Count, Sum
from udltimes.models import (
    Connections,
    Framed,
    FramedGameData,
    StatsConnections,
    StatsFramed,
    StatsWordle,
    Wordle,
)
from django.conf import settings


@login_required
def wordle_view(request):
    return render(request, 'wordle/index.html')

@login_required
def connections_view(request):
    color_palette = ["#e9c46a", "#f4a261", "#e76f51", "#c1440e"]
    puzzle_today = (
        Connections.objects
        .filter(date=timezone.localdate())
        .prefetch_related("categories__connectionsword_set")
        .first()
    )
    stats = None
    solutions = []

    if puzzle_today:
        stats = StatsConnections.objects.filter(user=request.user, game=puzzle_today).first()
        for index, category in enumerate(puzzle_today.categories.all()[:4]):
            solutions.append(
                {
                    "titulo": category.name,
                    "palabras": list(category.connectionsword_set.values_list("word", flat=True)),
                    "color": color_palette[index % len(color_palette)],
                }
            )

    return render(
        request,
        'connections/connections.html',
        {
            "soluciones_json": json.dumps(solutions),
            "ha_jugado": stats is not None,
            "puntos_obtenidos": stats.points if stats else 0,
            "hay_puzzle": puzzle_today is not None,
        },
    )


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
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')[:3]
    )
    wordle_leaderboard = [
        {'username': e['user__username'], 'total_score': e['total_score']}
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
        .filter(completed=True)
        .values('user__username')
        .annotate(points=Sum('points'))
        .order_by('-points')[:3]
    )
    framed_leaderboard = [
        {'username': e['user__username'], 'points': e['points']}
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

    framed_played = StatsFramed.objects.filter(user=user, completed=True).count()

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


def _today():
    return timezone.localdate()


def _normalize_text(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(char for char in value if not unicodedata.combining(char))
    return value.strip().upper()


def _json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def _completed_for_user(request, stat_model, game):
    if not request.user.is_authenticated:
        return False
    query = stat_model.objects.filter(user=request.user, game=game)
    if stat_model is StatsWordle:
        return query.filter(completed=True).exists()
    return query.exists()


def _already_completed_response(game_type):
    return JsonResponse(
        {
            "error": "already_completed",
            "message": f"You have already completed today's {game_type}.",
        },
        status=409,
    )


def _today_game_or_error(model):
    try:
        return model.objects.get(date=_today()), None
    except model.DoesNotExist:
        return None, JsonResponse({"error": "no_game_today"}, status=404)


def _score_wordle_guess(answer, guess):
    answer = _normalize_text(answer)
    guess = _normalize_text(guess)
    colors = ["gray"] * len(answer)
    remaining = {}

    for index, answer_letter in enumerate(answer):
        if index < len(guess) and guess[index] == answer_letter:
            colors[index] = "green"
        else:
            remaining[answer_letter] = remaining.get(answer_letter, 0) + 1

    for index, guess_letter in enumerate(guess[:len(answer)]):
        if colors[index] == "green":
            continue
        if remaining.get(guess_letter, 0) > 0:
            colors[index] = "yellow"
            remaining[guess_letter] -= 1

    return colors


@require_GET
def api_wordle_today(request):
    game, error = _today_game_or_error(Wordle)
    if error:
        return error
    return JsonResponse(
        {
            "date": game.date.isoformat(),
            "length": len(_normalize_text(game.word)),
            "already_completed": _completed_for_user(request, StatsWordle, game),
        }
    )


@csrf_exempt
@require_POST
def api_wordle_guess(request):
    game, error = _today_game_or_error(Wordle)
    if error:
        return error
    if _completed_for_user(request, StatsWordle, game):
        return _already_completed_response("wordle")

    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "invalid_json"}, status=400)

    guess = _normalize_text(data.get("guess"))
    answer = _normalize_text(game.word)
    if len(guess) != len(answer):
        return JsonResponse(
            {
                "error": "invalid_length",
                "expected_length": len(answer),
            },
            status=400,
        )

    colors = _score_wordle_guess(answer, guess)
    correct = guess == answer
    if correct and request.user.is_authenticated:
        stat, _ = StatsWordle.objects.get_or_create(
            user=request.user,
            game=game,
        )
        if not stat.completed:
            stat.completed = True
            stat.save()

    return JsonResponse(
        {
            "date": game.date.isoformat(),
            "guess": guess,
            "colors": colors,
            "correct": correct,
            "completed_saved": correct and request.user.is_authenticated,
        }
    )


def _connections_payload(game):
    categories = []
    words = []
    for category in game.categories.prefetch_related("connectionsword_set").all():
        category_words = list(category.connectionsword_set.values_list("word", flat=True))
        categories.append(
            {
                "name": category.name,
                "words": category_words,
            }
        )
        words.extend(category_words)

    random.Random(game.date.isoformat()).shuffle(words)
    return categories, words


@require_GET
def api_connections_today(request):
    game, error = _today_game_or_error(Connections)
    if error:
        return error
    categories, words = _connections_payload(game)
    return JsonResponse(
        {
            "date": game.date.isoformat(),
            "words": words,
            "group_count": len(categories),
            "already_completed": _completed_for_user(request, StatsConnections, game),
        }
    )


@csrf_exempt
@require_POST
def api_connections_guess(request):
    game, error = _today_game_or_error(Connections)
    if error:
        return error
    if _completed_for_user(request, StatsConnections, game):
        return _already_completed_response("connections")

    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "invalid_json"}, status=400)

    selected_words = data.get("words", [])
    if not isinstance(selected_words, list) or len(selected_words) != 4:
        return JsonResponse({"error": "select_exactly_4_words"}, status=400)

    selected = {_normalize_text(word) for word in selected_words}
    categories, _ = _connections_payload(game)

    for category in categories:
        category_words = {_normalize_text(word) for word in category["words"]}
        if selected == category_words:
            completed = bool(data.get("completed"))
            if completed and request.user.is_authenticated:
                StatsConnections.objects.get_or_create(
                    user=request.user,
                    game=game,
                    defaults={"completed": True},
                )
            return JsonResponse(
                {
                    "correct": True,
                    "category": category["name"],
                    "words": category["words"],
                    "completed_saved": completed and request.user.is_authenticated,
                }
            )

    return JsonResponse({"correct": False})


@csrf_exempt
@require_POST
def api_connections_complete(request):
    game, error = _today_game_or_error(Connections)
    if error:
        return error
    if _completed_for_user(request, StatsConnections, game):
        return _already_completed_response("connections")
    if not request.user.is_authenticated:
        return JsonResponse({"error": "login_required"}, status=401)

    StatsConnections.objects.create(user=request.user, game=game, completed=True)
    return JsonResponse({"completed_saved": True, "date": game.date.isoformat()})


@require_GET
def api_framed_today(request):
    game, error = _today_game_or_error(Framed)
    if error:
        return error
    frames = list(
        FramedGameData.objects
        .filter(game=game)
        .order_by("order")
        .values("order", "image")
    )
    answers = list(Framed.objects.order_by("paraula").values_list("paraula", flat=True))
    return JsonResponse(
        {
            "date": game.date.isoformat(),
            "frames": frames,
            "max_attempts": len(frames),
            "answers": answers,
            "already_completed": _completed_for_user(request, StatsFramed, game),
        }
    )


@csrf_exempt
@require_POST
def api_framed_guess(request):
    game, error = _today_game_or_error(Framed)
    if error:
        return error
    if _completed_for_user(request, StatsFramed, game):
        return _already_completed_response("framed")

    data = _json_body(request)
    if data is None:
        return JsonResponse({"error": "invalid_json"}, status=400)

    guess = data.get("guess", "")
    try:
        attempts = max(1, int(data.get("attempts") or 1))
    except (TypeError, ValueError):
        attempts = 1
    completed = bool(data.get("completed"))
    correct = _normalize_text(guess) == _normalize_text(game.paraula)
    if request.user.is_authenticated and (correct or completed):
        points = max(0, 60 - ((attempts - 1) * 10)) if correct else 0
        StatsFramed.objects.get_or_create(
            user=request.user,
            game=game,
            defaults={
                "value": str(guess).strip(),
                "completed": True,
                "guessed": correct,
                "attempts": attempts,
                "points": points,
            },
        )

    return JsonResponse(
        {
            "date": game.date.isoformat(),
            "correct": correct,
            "answer": game.paraula if completed and not correct else None,
            "completed_saved": request.user.is_authenticated and (correct or completed),
        }
    )
