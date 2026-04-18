import re
import json
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Count, Q
from django.utils import timezone
from udltimes.models import (
    Connections,
    Framed,
    FramedConcept,
    StatsWordle,
    StatsFramed,
    StatsConnections,
    Wordle,
)
from django.conf import settings


def wordle_view(request):
    return render(request, 'wordle.html')


def connections_view(request):
    return render(request, 'connections.html')


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
        .annotate(points=Count('id'))
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


def _json_error(message, status=400):
    return JsonResponse({'error': message}, status=status)


def _parse_json_body(request):
    if not request.body:
        return {}

    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


def _get_today_wordle():
    return Wordle.objects.filter(date=timezone.localdate()).first()


def _get_today_connections():
    return Connections.objects.filter(date=timezone.localdate()).first()


def _get_today_framed():
    return Framed.objects.select_related('concept').prefetch_related('concept__images').filter(
        date=timezone.localdate()
    ).first()


def _wordle_completed(user, game):
    if not user.is_authenticated:
        return False
    return StatsWordle.objects.filter(user=user, game=game, completed=True).exists()


def _connections_completed(user, game):
    if not user.is_authenticated:
        return False
    return StatsConnections.objects.filter(user=user, game=game, completed=True).exists()


def _framed_completed(user, game):
    if not user.is_authenticated:
        return False
    return StatsFramed.objects.filter(user=user, game=game, guessed=True).exists()


def _wordle_feedback(solution, guess):
    result = ['gray'] * len(solution)
    remaining = {}

    for index, char in enumerate(solution):
        if guess[index] == char:
            result[index] = 'green'
        else:
            remaining[char] = remaining.get(char, 0) + 1

    for index, char in enumerate(guess):
        if result[index] == 'green':
            continue
        if remaining.get(char, 0) > 0:
            result[index] = 'yellow'
            remaining[char] -= 1

    return result


def wordle_today_api(request):
    if request.method != 'GET':
        return _json_error('Method not allowed.', status=405)

    game = _get_today_wordle()
    if not game:
        return _json_error('No Wordle is configured for today.', status=404)

    return JsonResponse({
        'date': game.date.isoformat(),
        'length': len(game.word),
        'already_completed': _wordle_completed(request.user, game),
    })


def wordle_check_api(request):
    if request.method != 'POST':
        return _json_error('Method not allowed.', status=405)
    if not request.user.is_authenticated:
        return _json_error('Authentication required.', status=401)

    game = _get_today_wordle()
    if not game:
        return _json_error('No Wordle is configured for today.', status=404)
    if _wordle_completed(request.user, game):
        return JsonResponse({'already_completed': True}, status=409)

    payload = _parse_json_body(request)
    if payload is None:
        return _json_error('Invalid JSON body.')

    guess = str(payload.get('guess', '')).strip().lower()
    solution = game.word.strip().lower()

    if len(guess) != len(solution):
        return _json_error(f'Guess must be {len(solution)} letters long.')

    result = _wordle_feedback(solution, guess)
    correct = guess == solution

    if correct:
        StatsWordle.objects.update_or_create(
            user=request.user,
            game=game,
            defaults={'completed': True},
        )

    return JsonResponse({
        'date': game.date.isoformat(),
        'result': result,
        'correct': correct,
        'already_completed': False,
    })


def connections_today_api(request):
    if request.method != 'GET':
        return _json_error('Method not allowed.', status=405)

    game = _get_today_connections()
    if not game:
        return _json_error('No Connections game is configured for today.', status=404)

    words = list(
        game.categories
        .prefetch_related('connectionsword_set')
        .values_list('connectionsword__word', flat=True)
    )
    random.shuffle(words)

    return JsonResponse({
        'date': game.date.isoformat(),
        'words': words,
        'already_completed': _connections_completed(request.user, game),
    })


def connections_check_api(request):
    if request.method != 'POST':
        return _json_error('Method not allowed.', status=405)
    if not request.user.is_authenticated:
        return _json_error('Authentication required.', status=401)

    game = _get_today_connections()
    if not game:
        return _json_error('No Connections game is configured for today.', status=404)
    if _connections_completed(request.user, game):
        return JsonResponse({'already_completed': True}, status=409)

    payload = _parse_json_body(request)
    if payload is None:
        return _json_error('Invalid JSON body.')

    selected_words = payload.get('words', [])
    if not isinstance(selected_words, list) or len(selected_words) != 4:
        return _json_error('You must send exactly 4 words.')

    normalized_selection = {str(word).strip().lower() for word in selected_words}
    if len(normalized_selection) != 4:
        return _json_error('Selected words must be unique.')

    for category in game.categories.prefetch_related('connectionsword_set').all():
        category_words = {
            word.strip().lower()
            for word in category.connectionsword_set.values_list('word', flat=True)
        }
        if normalized_selection == category_words:
            return JsonResponse({
                'correct': True,
                'category': category.name,
                'already_completed': False,
            })

    return JsonResponse({
        'correct': False,
        'already_completed': False,
    })


def connections_complete_api(request):
    if request.method != 'POST':
        return _json_error('Method not allowed.', status=405)
    if not request.user.is_authenticated:
        return _json_error('Authentication required.', status=401)

    game = _get_today_connections()
    if not game:
        return _json_error('No Connections game is configured for today.', status=404)
    if _connections_completed(request.user, game):
        return JsonResponse({'already_completed': True}, status=409)

    payload = _parse_json_body(request)
    if payload is None:
        return _json_error('Invalid JSON body.')

    solved_count = payload.get('solved_count')
    solved_categories = payload.get('solved_categories', [])
    total_categories = game.categories.count()

    valid_by_count = solved_count == total_categories
    valid_by_categories = isinstance(solved_categories, list) and set(solved_categories) == set(
        game.categories.values_list('name', flat=True)
    )

    if not valid_by_count and not valid_by_categories:
        return _json_error('Connections game is not marked as fully solved yet.')

    StatsConnections.objects.update_or_create(
        user=request.user,
        game=game,
        defaults={'completed': True},
    )

    return JsonResponse({
        'saved': True,
        'already_completed': False,
    })


def framed_today_api(request):
    if request.method != 'GET':
        return _json_error('Method not allowed.', status=405)

    game = _get_today_framed()
    if not game:
        return _json_error('No Framed game is configured for today.', status=404)

    options = list(FramedConcept.objects.order_by('concept').values_list('concept', flat=True))
    images = [image.image_url for image in game.concept.images.all()]

    return JsonResponse({
        'date': game.date.isoformat(),
        'images': images,
        'options': options,
        'already_completed': _framed_completed(request.user, game),
    })


def framed_check_api(request):
    if request.method != 'POST':
        return _json_error('Method not allowed.', status=405)
    if not request.user.is_authenticated:
        return _json_error('Authentication required.', status=401)

    game = _get_today_framed()
    if not game:
        return _json_error('No Framed game is configured for today.', status=404)
    if _framed_completed(request.user, game):
        return JsonResponse({'already_completed': True}, status=409)

    payload = _parse_json_body(request)
    if payload is None:
        return _json_error('Invalid JSON body.')

    guess = str(payload.get('guess', '')).strip().lower()
    images_needed = payload.get('images_needed')
    concept = game.concept.concept.strip().lower()
    correct = guess == concept

    if correct:
        defaults = {'guessed': True}
        if isinstance(images_needed, int) and images_needed > 0:
            defaults['images_needed'] = images_needed
        StatsFramed.objects.update_or_create(
            user=request.user,
            game=game,
            defaults=defaults,
        )

    return JsonResponse({
        'correct': correct,
        'already_completed': False,
    })
