import os
import json
import random
import datetime
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from django.shortcuts import render
from udltimes.models import Wordle, StatsWordle


def wordle_page(request):
    return render(request, 'wordle/index.html')


@csrf_protect
def check_guess(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        guess = data.get('guess', '').upper()

        # palabra de hoy
        word_obj = Wordle.objects.filter(date=datetime.date.today()).first()

        if not word_obj:
            return JsonResponse({"status": "error", "mssg": "La palabra de hoy no se ha generado aún."})

        secret = word_obj.word.upper()

        # Lógica de colores
        colors = ["absent"] * 5
        secret_list = list(secret)
        guess_list = list(guess)

        # Primero buscamos las correctas (Verdes)
        for i in range(5):
            if guess_list[i] == secret_list[i]:
                colors[i] = "correct"
                secret_list[i] = None  # Marcamos para no repetir
                guess_list[i] = None

        # Luego buscamos las presentes (Amarillas)
        for i in range(5):
            if guess_list[i] is not None and guess_list[i] in secret_list:
                colors[i] = "present"
                secret_list[secret_list.index(guess_list[i])] = None

        # comprobamos si ha ganado
        win = (colors == ["correct"] * 5)

        # devuelvo el resultado
        return JsonResponse({
            "status": "success",
            "colors": colors,
            "win": win
        })


@csrf_exempt
def dailyWordle(request):
    if request.method == 'POST':
        today_date = datetime.date.today()

        # lee lo del front
        try:
            data = json.loads(request.body)
            username = data.get("username")
        except json.JSONDecodeError:
            return JsonResponse({"status": "400", "mssg": "JSON inválido"})

        if not username:
            return JsonResponse({"status": "400", "mssg": "Falta el username"})

        # Buscamos usuario
        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({"status": "404", "mssg": "Usuario no encontrado"})

        # comprobamos si ya jugó hoy
        stat = StatsWordle.objects.filter(user=user, game__date=today_date).first()

        if stat and stat.completed:
            return JsonResponse({"status": "409", "mssg": "El wordle del dia ya ha sido jugado"})

        # PALABRA DEL DIA
        wordle_obj = Wordle.objects.filter(date=today_date).first()

        if wordle_obj:
            daily_word = wordle_obj.word
        else:
            file_path = os.path.join(settings.BASE_DIR, 'udltimes', 'games', 'wordle', 'words.txt')
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    words = f.read().splitlines()
                    # Filtramos para asegurar que solo haya palabras de 5 letras
                    words = [w.strip() for w in words if len(w.strip()) == 5]

                    daily_generator = random.Random(str(today_date))
                    daily_word = daily_generator.choice(words).upper()

                # guardamos la nueva palabra en la base de datos
                Wordle.objects.create(date=today_date, word=daily_word)

            except (FileNotFoundError, IndexError):
                return JsonResponse({"status": "500", "mssg": "Error interno: Archivo words.txt no encontrado o vacío"})

        # devolver respuesta
        return JsonResponse({
            "status": "200",
            "already_played": False,
            # "word": daily_word  <-- Ya lo tienes comentado para que no lo vean en la consola
        })

    return JsonResponse({"status": "405", "mssg": "Método no permitido"})