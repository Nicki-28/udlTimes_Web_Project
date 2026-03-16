from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import datetime
import sqlite3
import os

app = Flask(__name__)  # levanto el servidor
CORS(app, supports_credentials=True)  # para comunicarme con el frontend


# Me conecto con la db
def db_connection():
    conn = sqlite3.connect('udl_games.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/dailyWordle', methods=['POST'])  # establezco la ruta para pasarla al front
def dailyWordle():
    today_date = str(datetime.date.today())

    data = request.get_json(force=True)
    username = data.get("username")

    if not username:
        return jsonify({"status": "400", "mssg": "falta el username"})

    conn = db_connection()
    try:
        cursor = conn.cursor()

        # Verificaremos si la partida del dia ya fue jugada
        # busco la id del jugador
        cursor.execute("SELECT id_user from users WHERE username =? ", (username,))
        id_users_rows = cursor.fetchone()
        if id_users_rows is None:
            return jsonify({"status": "404", "mssg": "usuario no encontrado"})
        id_user = id_users_rows['id_user']

        cursor.execute("SELECT status from users_game WHERE id_user=? ", (id_user,))
        status_rows = cursor.fetchone()
        status_game = status_rows['status'] if status_rows is not None else None

        if status_game == 'PLAYED':
            return jsonify({"status": "409", "mssg": "El wordle del dia ya ha sido jugado"})
        else:
            # No ha jugado
            # caso 1 - no esta cargada
            cursor.execute("SELECT word from daily_wordle WHERE date =?", (today_date,))
            wordle_row = cursor.fetchone()

            if wordle_row is not None:
                daily_word = wordle_row['word']
            else:  # cargo del txt
                # try to find words.txt relative to this file
                script_dir = os.path.dirname(__file__)
                words_path = os.path.join(script_dir, "words.txt")
                try:
                    with open(words_path, "r") as f:
                        words = f.read().splitlines()
                except FileNotFoundError:
                    return jsonify({"status": "500", "mssg": "words.txt no encontrado en el servidor"})

                if not words:
                    return jsonify({"status": "500", "mssg": "no hay palabras disponibles"})

                daily_generator = random.Random(today_date)
                daily_word = daily_generator.choice(words)
                print(daily_word)
                cursor.execute("INSERT INTO daily_wordle (date, word) VALUES (?,?)",
                               (today_date, daily_word))  # ya queda guardada en la bd
                conn.commit()

            return jsonify({"status": "200", "already_played": False, "word": daily_word})
    finally:
        conn.close()
