
class Database:
    DB_USER_SUBSCRIBED = 1
    DB_USER_UNSUBSCRIBED = 0
    FIELD_TELEGRAM_ID = 'telegram_id'
    FIELD_CHARACTER_NAME = 'character_name'
    FIELD_PHONE = 'phone'
    FIELD_SUBSCRIBED = 'subscribed'
    FIELD_GUILD_NAME = 'guild_name'


class DatabaseQueries:
    CREATE_TABLE_USERS_IF_NOT_EXISTS = '''CREATE TABLE IF NOT EXISTS users
             (telegram_id text PRIMARY KEY,
              character_name text,
              phone text,
              subscribed int,
              guild_name text)'''

    CREATE_TABLE_GUILDS_IF_NOT_EXISTS = '''CREATE TABLE IF NOT EXISTS guilds
             (guild_name text PRIMARY KEY)'''

    SELECT_ALL_FROM_USERS_WHERE_SUBSCRIBED = f'SELECT * FROM users WHERE subscribed={Database.DB_USER_SUBSCRIBED}'

    SELECT_ALL_FROM_GUILDS = 'SELECT * FROM guilds'

    @staticmethod
    def DELETE_FROM_USERS_WHERE_TELEGRAM_ID(telegram_id: str):
        return f'DELETE FROM users WHERE telegram_id="{telegram_id}"'

    @staticmethod
    def INSERT_INTO_USERS_WHERE_TELEGRAM_ID(telegram_id: str):
        return f'INSERT INTO users (telegram_id) VALUES ("{telegram_id}")'

    @staticmethod
    def UPDATE_USERS_SET_WHERE_TELEGRAM_ID(field: str, value, telegram_id: str):
        return f'UPDATE users SET {field}="{value}" WHERE telegram_id="{telegram_id}"'

    @staticmethod
    def UPDATE_USERS_SET_SUBSCRIBED_WHERE_TELEGRAM_ID(isSubscribed, telegram_id: str):
        return f'UPDATE users set subscribed={isSubscribed} WHERE telegram_id="{telegram_id}"'

    @staticmethod
    def SELECT_ALL_FROM_USERS_WHERE_TELEGRAM_ID(telegram_id: str):
        return f'SELECT * FROM users WHERE telegram_id="{telegram_id}"'

    @staticmethod
    def INSERT_INTO_GUILDS_SET_WHERE_GUILD_NAME(guild_name: str):
        return f'INSERT INTO guilds (guild_name) VALUES ("{guild_name}")'


class Commands:
    START = "/start"
    HELP = "/help"
    MENU = "/menu"
    ADD_GUILD = "/add_guild"
