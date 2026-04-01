import sqlite3

conn = sqlite3.connect("udl_games.db")
cursor = conn.cursor()

# games
conn.execute('''
            CREATE TABLE games(
                id_game INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            ''')

# users
conn.execute('''
            CREATE TABLE users(
                id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR (10) NOT NULL
            )

            ''')
# user_games
conn.execute('''
            CREATE TABLE users_games(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                id_user INTEGER NOT NULL,
                id_game INTEGER NOT NULL,
                id_wordle_word INTEGER NOT NULL,
                score INTEGER, 
                status TEXT NOT NULL,
                FOREIGN KEY (id_user) REFERENCES users (id_user),
                FOREIGN KEY (id_wordle_word) REFERENCES daily_wordle (id_wordle_word),
                FOREIGN KEY (id_game) REFERENCES games (id_game)

            )
            ''')
# wordle
conn.execute('''
            CREATE TABLE daily_wordle(
                id_wordle_word INTEGER PRIMARY KEY AUTOINCREMENT,
                id_game INTEGER NOT NULL,
                date DATE UNIQUE NOT NULL,
                word VARCHAR(5) NOT NULL,
                FOREIGN KEY (id_game) REFERENCES games(id_game)
            )
            ''')
conn.commit()
conn.close()

