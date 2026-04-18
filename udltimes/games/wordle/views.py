import os
import json
import random
import datetime
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.contrib.auth.models import User
from django.shortcuts import render
from udltimes.models import Wordle, StatsWordle

@ensure_csrf_cookie
def wordle_page(request):
    return render(request, 'wordle/index.html')


@csrf_protect
def check_guess(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "401", "mssg": "Debes iniciar sesión para jugar."})

    if request.method == 'POST':
        data = json.loads(request.body)
        guess = data.get('guess', '').upper()
        attempt = data.get('attempt', 1)
        time_taken = data.get('time', 0)

        # Validar longitud antes de cualquier otra cosa
        if len(guess) != 5:
            return JsonResponse({"status": "invalid_word", "mssg": "La palabra debe tener 5 letras"})

        # Validar que la palabra exista en el diccionario
        diccionario_path = os.path.join(settings.BASE_DIR, 'udltimes', 'games', 'wordle', 'diccionario.txt')
        try:
            with open(diccionario_path, "r", encoding="utf-8") as f:
                palabras_validas = {w.strip().upper() for w in f}
        except FileNotFoundError:
            return JsonResponse({"status": "500", "mssg": "Error interno: diccionario.txt no encontrado"})

        if guess not in palabras_validas:
            return JsonResponse({"status": "invalid_word", "mssg": "La palabra no existe"})

        # Obtener la palabra del día
        word_obj = Wordle.objects.filter(date=datetime.date.today()).first()
        if not word_obj:
            return JsonResponse({"status": "error", "mssg": "La palabra de hoy no se ha generado aún."})

        secret = word_obj.word.upper()

        # Lógica de colores
        colors = ["absent"] * 5
        secret_list = list(secret)
        guess_list = list(guess)

        for i in range(5):
            if guess_list[i] == secret_list[i]:
                colors[i] = "correct"
                secret_list[i] = None
                guess_list[i] = None

        for i in range(5):
            if guess_list[i] is not None and guess_list[i] in secret_list:
                colors[i] = "present"
                secret_list[secret_list.index(guess_list[i])] = None

        win = (colors == ["correct"] * 5)

        stat, created = StatsWordle.objects.get_or_create(user=request.user, game=word_obj)

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
            file_path = os.path.join(settings.BASE_DIR, 'udltimes', 'games', 'wordle', 'words.txt')
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    words = f.read().splitlines()
                    words = [w.strip() for w in words if len(w.strip()) == 5]

                    daily_generator = random.Random(today_date.toordinal())
                    daily_word = daily_generator.choice(words).upper()

                Wordle.objects.create(date=today_date, word=daily_word)

            except (FileNotFoundError, IndexError):
                return JsonResponse({"status": "500", "mssg": "Error interno: Archivo words.txt no encontrado o vacío"})

        return JsonResponse({
            "status": "200",
            "already_played": False,
            #"word": daily_word #SOLO PARA DEBUG
        })

    return JsonResponse({"status": "405", "mssg": "Método no permitido"})
