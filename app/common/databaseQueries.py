from app.common.databaseInterface import DatabaseInterface


class DatabaseQueries(DatabaseInterface):

    def test(self):
        self.execute(
            'INSERT INTO test (name) VALUES ("test");'
        )


    def get_user_id(self, email):
        row = self.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()

        if row is not None:
            return row['id']

        print("no users found")
        return None


    def get_user_password_hash(self, userId):
        return self.execute(
            'SELECT password_hash FROM user WHERE id = ?', (userId,)
        ).fetchone()['password_hash']


    def register_user(self, email, passwordHash):
        self.execute('INSERT INTO user (email, password_hash) VALUES (?, ?)', (email, passwordHash))
        self.commit()
        return self.last_row_id()








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