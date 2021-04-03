import app.common.database as database

db = database.Sqlite3Database()


def get_user_id(email):
    row = db.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()

    if row == None:
        print("no users found")
        return None
    else:
        return row['id']


def get_user_password_hash(userId):
    passwordHash = db.execute('SELECT password_hash FROM user WHERE id = ?', (userId,)).fetchone()['password_hash']
    return passwordHash


def register_user(email, passwordHash):
    db.execute('INSERT INTO user (email, password_hash) VALUES (?, ?)', (email, passwordHash))
    db.commit()
    return db.last_row_id()








def add_user_by_discord_id(discordId):
    db.execute('INSERT INTO user (discord_id) VALUES (?)', (discordId,))
    db.commit()


def get_user_id_by_discord_id(discordId):
    result = db.execute('SELECT id FROM user WHERE discord_id = ?', (discordId,)).fetchone()

    if result is None:
        add_user_by_discord_id(discordId)
        userId = get_user_id_by_discord_id(discordId)
        return userId
    else:
        return result['id']