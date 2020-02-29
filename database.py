
import sqlite3

from constants import Database

from threading import RLock


dbConnection = sqlite3.connect('users.db', check_same_thread=False)

c = dbConnection.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (name text PRIMARY KEY,real_name text ,phone text, subscribed int)''')

dbConnection.commit()


dbLock = RLock()


class User:
    def __init__(self, tpl):
        super().__init__()

        self.name = tpl[0]
        self.real_name = tpl[1]
        self.phone = tpl[2]
        self.subscribed = tpl[3]


def create_user(name):
    with dbLock:
        c.execute('''DELETE FROM users WHERE name="%s"''' % (name))
        c.execute(
            '''INSERT INTO users (name) VALUES ("%s")''' % (name))
        dbConnection.commit()


def update_user(name, field, value):

    with dbLock:
        c.execute(
            '''UPDATE users SET %s="%s" WHERE name="%s"''' % (
                field, value, name)
        )
        dbConnection.commit()


def set_subscription(name, isSubscribed):
    with dbLock:
        c.execute(
            '''UPDATE users set subscribed=%d WHERE name="%s"''' % (
                isSubscribed, name)
        )
        dbConnection.commit()


def get_subscribed_users():
    with dbLock:
        c.execute(
            '''SELECT * FROM users WHERE subscribed=%d''' % (
                Database.DB_USER_SUBSCRIBED)
        )
        rows = c.fetchall()
        res = list()

        for row in rows:
            res.append(User(row))
        return res


def get_user(name):
    with dbLock:
        c.execute('''SELECT * FROM users WHERE name="%s"''' % (name))
        user = c.fetchone()

        return User(user)


def remove_user(name):
    with dbLock:
        c.execute(
            '''DELETE FROM users WHERE name="%s"''' % (name)
        )
        dbConnection.commit()
