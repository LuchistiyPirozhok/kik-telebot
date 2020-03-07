
import sqlite3
import os

from constants import Database

from threading import RLock

from constants import Database, Commands, DatabaseQueries

dbConnection = sqlite3.connect('users.db', uri=True, check_same_thread=False)

c = dbConnection.cursor()
c.execute(DatabaseQueries.CREATE_TABLE_USERS_IF_NOT_EXISTS)
c.execute(DatabaseQueries.CREATE_TABLE_GUILDS_IF_NOT_EXISTS)

dbConnection.commit()


dbLock = RLock()


class User:
    def __init__(self, tpl):
        super().__init__()

        self.telegram_id = tpl[0]
        self.character_name = tpl[1]
        self.phone = tpl[2]
        self.subscribed = tpl[3]
        self.guild_name = tpl[4]
        self.reg_code = tpl[5]
        self.status = tpl[6]
        self.boss_mask = tpl[7]


class Guild:
    def __init__(self, tpl):
        super().__init__()

        self.guild_name = tpl[0]


def create_user(telegram_id):
    with dbLock:
        #       c.execute('''DELETE FROM users WHERE telegram_id="%s"''' % (telegram_id))
        c.execute(DatabaseQueries.DELETE_FROM_USERS_WHERE_TELEGRAM_ID(telegram_id))
#       c.execute('''INSERT INTO users (telegram_id) VALUES ("%s")''' % (telegram_id))
        c.execute(DatabaseQueries.INSERT_INTO_USERS_WHERE_TELEGRAM_ID(telegram_id))
        dbConnection.commit()


def update_user(telegram_id, field, value):

    with dbLock:
        #       c.execute('''UPDATE users SET %s="%s" WHERE telegram_id="%s"''' % (field, value, telegram_id))
        c.execute(DatabaseQueries.UPDATE_USERS_SET_WHERE_TELEGRAM_ID(
            field, value, telegram_id))
        dbConnection.commit()


def insert_guild(guild_name):

    with dbLock:
        #       c.execute('''UPDATE users SET %s="%s" WHERE telegram_id="%s"''' % (field, value, telegram_id))
        c.execute(DatabaseQueries.INSERT_INTO_GUILDS_SET_WHERE_GUILD_NAME(
            guild_name))
        dbConnection.commit()


def get_all_guilds():

    with dbLock:
        #       c.execute('''UPDATE users SET %s="%s" WHERE telegram_id="%s"''' % (field, value, telegram_id))
        c.execute(DatabaseQueries.SELECT_ALL_FROM_GUILDS)

        rows = c.fetchall()
        res = list()

        for row in rows:
            res.append(Guild(row))
        return res


def set_subscription(telegram_id, isSubscribed):
    with dbLock:
        #       c.execute('''UPDATE users set subscribed=%d WHERE telegram_id="%s"''' % (isSubscribed, telegram_id))
        c.execute(DatabaseQueries.UPDATE_USERS_SET_SUBSCRIBED_WHERE_TELEGRAM_ID(
            isSubscribed, telegram_id))
        dbConnection.commit()


def get_subscribed_users():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_FROM_USERS_WHERE_SUBSCRIBED)

        rows = c.fetchall()
        res = list()

        for row in rows:
            res.append(User(row))
        return res


def get_user(telegram_id):
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE telegram_id="%s"''' % (telegram_id))
        c.execute(
            DatabaseQueries.SELECT_ALL_FROM_USERS_WHERE_TELEGRAM_ID(telegram_id))
        user = c.fetchone()

        if(user is None):
            return user

        return User(user)


def remove_user(telegram_id):
    with dbLock:
        #       c.execute('''DELETE FROM users WHERE telegram_id="%s"''' % (telegram_id))
        c.execute(DatabaseQueries.DELETE_FROM_USERS_WHERE_TELEGRAM_ID(telegram_id))

        dbConnection.commit()

def get_all_users():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_FROM_USERS)

        rows = c.fetchall()
        res = list()

        for row in rows:
            res.append(User(row))
        return res

def get_all_pending_users():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_FROM_USERS_WHERE_STATUS_PENDING)
#проверить на наличие
        rows = c.fetchall()
        res = list()

        for row in rows:
            res.append(User(row))
        return res

def get_all_banned_users():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_FROM_USERS_WHERE_STATUS_BANNED)

        rows = c.fetchall()
        res = list()

        for row in rows:
            res.append(User(row))
        return res

def get_all_admins():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_FROM_USERS_WHERE_STATUS_ADMIN)

        rows = c.fetchall()
        res = list()

        for row in rows:
            res.append(User(row))
        return res