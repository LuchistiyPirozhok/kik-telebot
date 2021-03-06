from bot_common import get_timestamp


class Database:
    USER_SUBSCRIBED = 1
    USER_UNSUBSCRIBED = 0
    FIELD_TELEGRAM_ID = 'telegram_id'
    FIELD_CHARACTER_NAME = 'character_name'
    FIELD_PHONE = 'phone'
    FIELD_SUBSCRIBED = 'subscribed'
    FIELD_GUILD_NAME = 'guild_name'
    FIELD_REG_CODE = 'reg_code'
    FIELD_STATUS = 'status'
    FIELD_BOSS_MASK = 'boss_mask'
    FIELD_LAST_UPDATE = 'last_update'
    PAGE_SIZE = 10
    MAX_CHECK_DURATION = 60


class Statuses:
    BANNED = -1
    UNREGISTERED = 0
    PENDING = 1
    ACTIVE = 2
    ADMIN = 3
    SUPERVISOR = 4


class BossMasks:
    AZUREGOS = 0b000001
    KAZZAK = 0b000010
    FERALAS = 0b000100
    DUSKWOOD = 0b001000
    HINTERLANDS = 0b010000
    ASHENVALE = 0b100000
    ALL = 0b111111
    NONE = 0b000000

    @staticmethod
    def boss_list():
        return [
            BossMasks.AZUREGOS,
            BossMasks.KAZZAK,
            BossMasks.FERALAS,
            BossMasks.DUSKWOOD,
            BossMasks.HINTERLANDS,
            BossMasks.ASHENVALE
        ]

    @staticmethod
    def get_list():
        return [
            BossMasks.AZUREGOS,
            BossMasks.KAZZAK,
            BossMasks.FERALAS,
            BossMasks.DUSKWOOD,
            BossMasks.HINTERLANDS,
            BossMasks.ASHENVALE,
            BossMasks.ALL,
            BossMasks.NONE
        ]


class DatabaseQueries:
    CREATE_USERS_TABLE = f'''CREATE TABLE IF NOT EXISTS users
            (
              telegram_id text PRIMARY KEY,
              character_name text,
              phone text,
              subscribed int,
              guild_name text,
              reg_code text,
              status int default {Statuses.UNREGISTERED},
              boss_mask int default {BossMasks.NONE},
              last_update int default 0
            )'''

    CREATE_GUILDS_TABLE = '''CREATE TABLE IF NOT EXISTS guilds
             (guild_name text PRIMARY KEY)'''

    SELECT_ALL_USERS = 'SELECT * FROM users'
    SELECT_ALL_SUBSCRIBED_USERS = f'SELECT * FROM users WHERE subscribed={Database.USER_SUBSCRIBED} and status>={Statuses.ACTIVE}'

    SELECT_ALL_FROM_GUILDS = 'SELECT * FROM guilds'
    SELECT_ALL_USERS_WHERE_STATUS_PENDING = f'SELECT * FROM users WHERE status="{Statuses.PENDING}"'
    SELECT_ALL_USERS_WHERE_STATUS_BANNED = f'SELECT * FROM users WHERE status="{Statuses.BANNED}"'
    SELECT_ALL_USERS_WHERE_STATUS_ADMIN = f'SELECT * FROM users WHERE status>={Statuses.ADMIN}'
    SELECT_ALL_USERS_WHERE_STATUS_ADMIN_AND_SUBSCRIBED = f'SELECT * FROM users WHERE status>={Statuses.ADMIN} and subscribed={Database.USER_SUBSCRIBED}'

    SELECT_USERS_COUNT = f'SELECT count(*) FROM users'

    @staticmethod
    def GET_USERS_WITH_EXPIRED_CHECK_STAMP():
        return f'''SELECT * FROM users 
            WHERE {Database.FIELD_BOSS_MASK}>0 AND
                  {Database.FIELD_LAST_UPDATE}<={get_timestamp()-Database.MAX_CHECK_DURATION}'''

    @staticmethod
    def DELETE_USER_BY_ID(telegram_id: str):
        return f'DELETE FROM users WHERE telegram_id="{telegram_id}"'

    @staticmethod
    def CREATE_USER_WITH_ID(telegram_id: str):
        return f'INSERT INTO users (telegram_id) VALUES ("{telegram_id}")'

    @staticmethod
    def UPDATE_USER_FIELD(field: str, value, telegram_id: str):
        return f'UPDATE users SET {field}="{value}" WHERE telegram_id="{telegram_id}"'

    @staticmethod
    def UPDATE_USER_SUBSCRIPTION_FLAG(isSubscribed, telegram_id: str):
        return f'UPDATE users set subscribed={isSubscribed} WHERE telegram_id="{telegram_id}"'

    @staticmethod
    def SELECT_USER_BY_TELEGRAM_ID(telegram_id: str):
        return f'SELECT * FROM users WHERE telegram_id="{telegram_id}"'

    @staticmethod
    def ADD_GUILD_WITH_NAME(guild_name: str):
        return f'INSERT INTO guilds (guild_name) VALUES ("{guild_name}")'

    @staticmethod
    def TOGGLE_BOSSES_BY_MASK(telegram_id: str, boss_mask: int):
        '''
        We are using xor operation here to toggle bits by mask.

        e.g boss_mask = 0b001
            user.boss_mask = 0b100

           new_mask = user.boss_mask xor boss_mask = 0b101

        if we xor new mask again
            new_mask xor boss_mask = 0b101 xor 0b001 = 0b001

        Since sqlite3 doesn't support a xor operation we emulate it
        with (a or b) - (a and b) (a.k.a (a | b)-(a & b)) 
        '''

        return f'''UPDATE users SET 
                {Database.FIELD_BOSS_MASK}=
                    ({Database.FIELD_BOSS_MASK}|{boss_mask})-
                    ({Database.FIELD_BOSS_MASK}&{boss_mask}),
                {Database.FIELD_LAST_UPDATE}={get_timestamp()}
            WHERE {Database.FIELD_TELEGRAM_ID}={telegram_id}
        '''

    @staticmethod
    def SELECT_USERS_BY_MASK(boss_mask: int):
        '''
        Wes use bitwise and to find users with needed boss bit setted up
        '''
        return f' SELECT * FROM users WHERE boss_mask & {boss_mask}'

    @staticmethod
    def SELECT_PAGE_OF_USERS(page: int):
        return f'SELECT * FROM users limit {Database.PAGE_SIZE} offset {Database.PAGE_SIZE * page}'


class Commands:
    START = "/start"
    HELP = "/help"
    MENU = "/menu"
    ADD_GUILD = "/add_guild"
