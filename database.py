import sqlite3, os

from flask import current_app, g
from werkzeug.local import LocalProxy

databaseFile = os.getenv("DATABASE_FILE")

# Opens a new database connection if there is none yet for the current application context
def get_db():
    if 'db' not in g:
        g.db_conn = sqlite3.connect(databaseFile)
        g.db_conn.row_factory = sqlite3.Row
        g.db = g.db_conn.cursor()
    return g.db


def get_db_conn():
    if 'db_conn' not in g:
        get_db()
    return g.db_conn
    

db = LocalProxy(get_db)
db_conn = LocalProxy(get_db_conn)


# Closes the database again at the end of the request
def close_db(error):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        db_conn.close()


def add_user_by_discord_id(discordId):
    db.execute('INSERT INTO user (discord_id) VALUES (?)', (discordId,))
    db_conn.commit()


def get_user_id_by_discord_id(discordId):
    result = db.execute('SELECT id FROM user WHERE discord_id = ?', (discordId,)).fetchone()

    if result is None:
        add_user_by_discord_id(discordId)
        get_user_id_by_discord_id(discordId)

    return result['id']





