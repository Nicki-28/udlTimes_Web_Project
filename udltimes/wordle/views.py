import os
import json
import random
import datetime
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.contrib.auth.models import User
from django.shortcuts import render
from udltimes.models import Wordle, StatsWordle
from django.db.models import Sum

@ensure_csrf_cookie
def wordle_page(request):
    return render(request, 'wordle/index.html')


def palabra_existe_en_rae(word: str) -> bool:
    """
    Verifica si una palabra existe usando la API de la RAE.
    """

    try:
        response = requests.get(
            f"https://rae-api.com/api/words/{word.lower()}",
            timeout=5
        )

        if response.status_code != 200:
            return False

        data = response.json()

        return data.get("ok", False)

    except requests.RequestException:
        return False


def palabra_existe_en_dictionaryapi(word: str) -> bool:
    """
    Verifica si una palabra existe en inglés usando DictionaryAPI.
    """

    try:
        response = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}",
            timeout=5
        )

        # 200 = existe
        return response.status_code == 200

    except requests.RequestException:
        return False


def palabra_existe_db(word):
    return Wordle.objects.filter(
        word__iexact=word
    ).exists()

@csrf_protect
def check_guess(request):

    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "401",
            "mssg": "Debes iniciar sesión para jugar."
        })

    if request.method != 'POST':
        return JsonResponse({
            "status": "405",
            "mssg": "Método no permitido"
        })

    try:
        data = json.loads(request.body)

        guess = data.get('guess', '').upper().strip()
        attempt = data.get('attempt', 1)
        time_taken = data.get('time', 0)

        # Validar longitud
        if len(guess) != 5:
            return JsonResponse({
                "status": "invalid_word",
                "mssg": "La palabra debe tener 5 letras"
            })

        # Validar existencia en RAE
        if not (palabra_existe_en_rae(guess) or palabra_existe_en_dictionaryapi(guess) or palabra_existe_db(guess)):
            return JsonResponse({
                "status": "invalid_word",
                "mssg": "La palabra no existe"
            })

        # Obtener palabra del día
        word_obj = Wordle.objects.filter(
            date=datetime.date.today()
        ).first()

        if not word_obj:
            return JsonResponse({
                "status": "error",
                "mssg": "La palabra de hoy no se ha generado aún."
            })

        secret = word_obj.word.upper()

        # Lógica Wordle
        colors = ["absent"] * 5

        secret_list = list(secret)
        guess_list = list(guess)

        # Letras correctas
        for i in range(5):
            if guess_list[i] == secret_list[i]:
                colors[i] = "correct"
                secret_list[i] = None
                guess_list[i] = None

        # Letras presentes
        for i in range(5):
            if (
                guess_list[i] is not None
                and guess_list[i] in secret_list
            ):
                colors[i] = "present"
                secret_list[secret_list.index(guess_list[i])] = None

        win = colors == ["correct"] * 5

        # Guardar estadísticas
        stat, created = StatsWordle.objects.get_or_create(
            user=request.user,
            game=word_obj
        )

        if win or attempt == 6:
            stat.completed = True
            stat.attempts = attempt
            stat.time_taken = time_taken
            stat.score = 100 - ((attempt - 1) * 10) if win else 0
            stat.save()

        response_data = {
            "status": "success",
            "colors": colors,
            "win": win
        }

        if not win and attempt == 6:
            response_data["word"] = secret

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({
            "status": "error",
            "mssg": "JSON inválido"
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "mssg": str(e)
        }, status=500)


@csrf_exempt
def dailyWordle(request):
    # Verificamos que el usuario haya iniciado sesión
    if not request.user.is_authenticated:
         return JsonResponse({"status": "401", "mssg": "Debes iniciar sesión para jugar."})

    if request.method == 'POST':
        today_date = datetime.date.today()
        user = request.user

        # Comprobamos si ya jugó hoy
        stat = StatsWordle.objects.filter(user=user, game__date=today_date).first()

        if stat and stat.completed:
            return JsonResponse({
                "status": "409",
                "mssg": "El wordle del dia ya ha sido jugado",
                "stats": {
                    "attempts": getattr(stat, 'attempts', 0),
                    "score": getattr(stat, 'score', 0),
                    "time": getattr(stat, 'time_taken', 0)
                }
            })

        # Generar o recuperar la palabra del día
        wordle_obj = Wordle.objects.filter(date=today_date).first()

        if wordle_obj:
            daily_word = wordle_obj.word
        else:
            return JsonResponse({"status": "error", "mssg": "La palabra de hoy no se ha generado aún."})


        return JsonResponse({
            "status": "200",
            "already_played": False,
            #"word": daily_word #SOLO PARA DEBUG
        })

    return JsonResponse({"status": "405", "mssg": "Método no permitido"})
