
import sqlite3
import os

from threading import RLock

from constants import DatabaseQueries

dbConnection = sqlite3.connect('users.db', uri=True, check_same_thread=False)

c = dbConnection.cursor()
c.execute(DatabaseQueries.CREATE_USERS_TABLE)
c.execute(DatabaseQueries.CREATE_GUILDS_TABLE)


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


def map_tuples_to_users(rows):
    res = list()

    for row in rows:
        res.append(User(row))

    return res


def create_user(telegram_id):
    with dbLock:
        #       c.execute('''DELETE FROM users WHERE telegram_id="%s"''' % (telegram_id))
        c.execute(DatabaseQueries.DELETE_USER_BY_ID(telegram_id))
#       c.execute('''INSERT INTO users (telegram_id) VALUES ("%s")''' % (telegram_id))
        c.execute(DatabaseQueries.CREATE_USER_WITH_ID(telegram_id))
        dbConnection.commit()


def update_user(telegram_id, field, value):

    with dbLock:
        #       c.execute('''UPDATE users SET %s="%s" WHERE telegram_id="%s"''' % (field, value, telegram_id))
        c.execute(DatabaseQueries.UPDATE_USER_FIELD(
            field, value, telegram_id))
        dbConnection.commit()


def insert_guild(guild_name):

    with dbLock:
        #       c.execute('''UPDATE users SET %s="%s" WHERE telegram_id="%s"''' % (field, value, telegram_id))
        c.execute(DatabaseQueries.ADD_GUILD_WITH_NAME(guild_name))
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
        c.execute(DatabaseQueries.UPDATE_USER_SUBSCRIPTION_FLAG(
            isSubscribed, telegram_id))
        dbConnection.commit()


def get_subscribed_users():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_SUBSCRIBED_USERS)

        rows = c.fetchall()
        return map_tuples_to_users(rows)


def get_user(telegram_id):
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE telegram_id="%s"''' % (telegram_id))
        c.execute(
            DatabaseQueries.SELECT_USER_BY_TELEGRAM_ID(telegram_id))
        user = c.fetchone()

        if(user is None):
            return user

        return User(user)


def remove_user(telegram_id):
    with dbLock:
        #       c.execute('''DELETE FROM users WHERE telegram_id="%s"''' % (telegram_id))
        c.execute(DatabaseQueries.DELETE_USER_BY_ID(telegram_id))

        dbConnection.commit()


def get_all_users():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_USERS)

        rows = c.fetchall()
        return map_tuples_to_users(rows)


def get_all_pending_users():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_USERS_WHERE_STATUS_PENDING)
        # проверить на наличие
        rows = c.fetchall()
        return map_tuples_to_users(rows)


def get_all_banned_users():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_USERS_WHERE_STATUS_BANNED)

        rows = c.fetchall()
        return map_tuples_to_users(rows)


def get_all_admins():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_USERS_WHERE_STATUS_ADMIN)

        rows = c.fetchall()
        return map_tuples_to_users(rows)

def get_all_subscribed_admins():
    with dbLock:
        #       c.execute('''SELECT * FROM users WHERE subscribed=%d''' % (Database.DB_USER_SUBSCRIBED))
        c.execute(DatabaseQueries.SELECT_ALL_USERS_WHERE_STATUS_ADMIN_AND_SUBSCRIBED)

        rows = c.fetchall()
        res = list()

        for row in rows:
            res.append(User(row))
        return res

def toggle_user_mask(boss_mask: int, telegram_id: str):
    with dbLock:
        c.execute(DatabaseQueries.TOGGLE_BOSSES_BY_MASK(
            telegram_id, boss_mask))
        dbConnection.commit()


def get_users_by_mask(boss_mask: int):
    with dbLock:
        c.execute(DatabaseQueries.SELECT_USERS_BY_MASK(boss_mask))

        rows = c.fetchall()
        return map_tuples_to_users(rows)


def get_users_page(page: int):
    with dbLock:
        c.execute(DatabaseQueries.SELECT_PAGE_OF_USERS(page))

        rows = c.fetchall()
        return map_tuples_to_users(rows)


def get_users_count():
    with dbLock:
        c.execute(DatabaseQueries.SELECT_USERS_COUNT)

        row = c.fetchone()
        return int(row[0])
