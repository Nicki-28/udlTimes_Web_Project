import os
import json
import random
import datetime
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render
from udltimes.models import Wordle, StatsWordle

def wordle_page(request):
    return render(request, 'wordle/index.html')

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

        #Buscamos usuario
        user = User.objects.filter(username=username).first()
        if not user:
            return JsonResponse({"status": "404", "mssg": "Usuario no encontrado"})

        #comprobamos si ya jugó hoy
        stat = StatsWordle.objects.filter(user=user, game__date=today_date).first()

        if stat and stat.completed:
            return JsonResponse({"status": "409", "mssg": "El wordle del dia ya ha sido jugado"})

        #PALABRA DEL DIA
        wordle_obj = Wordle.objects.filter(date=today_date).first()

        if wordle_obj:
            daily_word = wordle_obj.word
        else:
            file_path = os.path.join(settings.BASE_DIR, 'udltimes', 'games', 'wordle', 'words.txt')
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    words = f.read().splitlines()
                    daily_generator = random.Random(str(today_date))
                    daily_word = daily_generator.choice(words)

                # guardamos la nueva palabra en la base de datos
                Wordle.objects.create(date=today_date, word=daily_word)

            except FileNotFoundError:
                return JsonResponse({"status": "500", "mssg": "Error interno: Archivo words.txt no encontrado"})

        # devolver respuesta ---------> just debbuging

        return JsonResponse({
            "status": "200",
            "already_played": False,
            "word": daily_word
        })

    return JsonResponse({"status": "405", "mssg": "Método no permitido"})