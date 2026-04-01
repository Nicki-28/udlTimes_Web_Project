from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import datetime
import sqlite3
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Me conecto con la db
def db_connection():
    conn = sqlite3.connect('udl_games.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/dailyWordle', methods=['POST'])
def dailyWordle():
    today_date = str(datetime.date.today())
    data = request.get_json(force=True)
    username = data.get("username")

    if not username:
        return jsonify({"status": "400", "mssg": "falta el username"})

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_user from users WHERE username = ?", (username,))
    user_row = cursor.fetchone()

    if not user_row:
        conn.close()
        return jsonify({"status": "404", "mssg": "Usuario no encontrado"})

    id_user = user_row['id_user']

    cursor.execute("SELECT status from users_game WHERE id_user=? AND date=?", (id_user, today_date))
    status_row = cursor.fetchone()

    if status_row and status_row['status'] == 'PLAYED':
        conn.close()
        return jsonify({"status": "409", "mssg": "El wordle del dia ya ha sido jugado"})

    cursor.execute("SELECT word from daily_wordle WHERE date = ?", (today_date,))
    wordle_row = cursor.fetchone()

    if wordle_row:
        daily_word = wordle_row['word']
    else:
        with open("words.txt", "r") as f:
            words = f.read().splitlines()
            daily_generator = random.Random(today_date)
            daily_word = daily_generator.choice(words)

        cursor.execute("INSERT INTO daily_wordle (date, word) VALUES (?,?)", (today_date, daily_word))
        conn.commit()

    conn.close()

    return jsonify({"status": "200", "already_played": False, "word": daily_word})