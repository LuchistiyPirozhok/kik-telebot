class Locale:
    CHARACTER_NAME = '''Введите имя вашего основного персонажа:'''
    GUILD_NAME = '''Введите название гильдии'''
    BOT_HELP_MESSAGE = '''/start - регистрация
/menu - показать меню
                        '''
    BOT_MENU_MESSAGE = '''Меню Kik-Notify:'''
    BOT_ADMIN_MENU = '''Административная часть'''
    CHARACTER_SUBCRIPTION = '''Подписаться'''
    CHARACTER_UNSUBCRIPTION = '''Отписаться'''
    CHARACTER_GUILD = '''В какой гильдии вы состоите?'''
    CHARACTER_QUESTION_ABOUT_SUBCRIPTION = '''Вы хотите подписаться на уведомления?'''
    CHARACTER_SUCCESSFUL_SUBCRIPTION = '''Вы подписались на уведомления'''
    CHARACTER_SUCCESSFUL_UNSUBCRIPTION = '''Вы отписались от уведомлений'''
    CONFIRM = 'Зарегистрировать пользователя'
    NOT_CONFIRM = 'Забанить пользователя'
    DELETE = 'Удалить пользователя из БД'
    REGISTER_FIRST = 'Сначала необходимо завершить реигстрацию'
    CHARACTER_REG_SUCCESSFUL = '''Регистрация успешно подтверждена'''
    CHARACTER_REG_FAILED = '''К сожалению, вы не прошли регистрацию из-за ошибок в имени персонажа или выборе гильдии. Пожалуйста, попробуйте зарегистрироваться снова'''
    CHARACTER_REG_BANNED = '''К сожалению, вы были заблокированы. По всем вопросам обращайтесь к администратору в дискорде'''
    CHARACTER_REG_PENDING = '''Заявка на регистрацию уже была отправлена. Пожалуйста, ожидайте ее подтверждения'''

    @staticmethod
    def BOSS_NOTIFICATION(user_name, boss_name):
        return f'{user_name} обнаружил {boss_name}'

    @staticmethod
    def DUPLICATE_CHARACTER_NAME(user_name):
        return f'Вы авторизованы как {user_name}'

    @staticmethod
    def REGISTRATION_COMPLETE(reg_code):
        return f'Для завершения регистрации вам нужно сообщить следующий код администратору в дискорде (Dorim#1317): {reg_code}'

    @staticmethod
    def REGISTRATION_COMPLETE_CONFIRM(user_name, reg_code):
        return f'Поступил запрос регистрации от пользователя {user_name} со следующим кодом {reg_code}. Подтвердить?'

class Admin:
    ALL_USERS = 'Вывести таблицу со всеми пользователями'
    ALL_GUILDS = 'Вывести таблицу со всеми гильдиями'
    ALL_PENDUNG_USERS = 'Вывести список ожидающих подтверждения регистрации пользователей'
    ALL_BANNED_USERS = 'Вывести список забаненных пользователей'
    CHANGE_USER_STATUS = 'Изменить статус пользователя по ID'
    DELETE_USER = 'Удалить пользователя из БД по ID'
    ALL_ADMINS = 'Вывести список администраторов'
    MESSAGE_TO_ALL = 'Отправить сообщение всем пользователем'
    ADD_GUILD = 'Добавить гильдию'
    USERS_EMPTY = 'Такие пользователи отсутствуют'
    SELECT_USER_STATUS_BY_ID = 'Введите ID пользователя:'
    SELECT_USER_STATUS_BY_ID_FAILED = 'Пользователь с таким ID не найден'
    SELECT_USER_STATUS_BY_ID_SUCCESSFUL = 'Пользователь с таким ID найден'
    CHANGE_USER_STATUS_BY_ID = '''Введите новый статус пользователя:
"-1" - забанить
"2" - активировать
                        '''
    CHANGE_USER_STATUS_BY_ID_SUCCESSFUL = 'Статус пользователя изменен'        
    CHANGE_USER_STATUS_BY_ID_ADD_ADMIN = 'Вам были выданы права администратора'  
    ADD_ADMIN = 'Добавить админа'
    NO_PERMITTIONS = 'У вас отсутствуют права на выполнение этого действия'
    MESSAGE_TEXT = 'Введите сообщение, которое будет отправлено всем активным пользователям с включенной подпиской'
    MESSAGE_TO_ALL_TITLE = 'Сообщение всем подписчикам'

    @staticmethod
    def MESSAGE_TO_ALL(user_name, message_to_all):
        return f'Администратор {user_name} сообщает: "{message_to_all}"'

class LocaleExceptions:
    ENVIRONMENT_API_KEY_NOT_FOUND = '''Environment variable KIK_TELEBOT_API_KEY aren't present'''


class Bosses:
    AZUREGOS = 'Азурегоса'
    KAZZAK = 'Каззака'
    EMERISS = 'Эмирисса'
    LETHON = 'Летона'
    YSONDRE = 'Исондру'
    TAERAR = 'Таэрара'

    @staticmethod
    def getList():
        return [Bosses.AZUREGOS, Bosses.KAZZAK, Bosses.EMERISS, Bosses.LETHON, Bosses.YSONDRE, Bosses.TAERAR]


class Messages:
    SUBSCRIBE = 'subscribe'
    UNSUBSCRIBE = 'unsubscribe'
    ADD_GUILD = 'add_guild'
    GUILD = 'guild'
    CONFIRM = 'confirm'
    NOT_CONFIRM = 'not_confirm'
    DELETE = 'delete'
    ADMIN = 'admin'
    ALL_USERS = 'all_users'
    ALL_GUILDS = 'all_guilds'
    ALL_PENDUNG_USERS = 'all_pending_users'
    ALL_BANNED_USERS = 'all_banned_users'
    CHANGE_USER_STATUS = 'change_user_status'
    DELETE_USER = 'delete_user'
    ALL_ADMINS = 'all_admins'
    MESSAGE_TO_ALL = 'message_to_all'
    ADD_ADMIN = 'add_admin'