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