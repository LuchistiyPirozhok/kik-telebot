class Locale:
    CHARACTER_NAME = '''Введите имя вашего основного персонажа:'''
    GUILD_NAME = '''Введите название гильдии'''
    BOT_HELP_MESSAGE = '''/start - регистрация
/menu - показать меню
                        '''
    BOT_MENU_MESSAGE = '''Меню:'''
    CHARACTER_SUBCRIPTION = '''Подписаться'''
    CHARACTER_UNSUBCRIPTION = '''Отписаться'''
    CHARACTER_GUILD = '''В какой гильдии вы состоите?'''
    CHARACTER_QUESTION_ABOUT_SUBCRIPTION = '''Вы хотите подписаться на уведомления?'''
    CHARACTER_SUCCESSFUL_SUBCRIPTION = '''Вы подписались на уведомления'''
    CHARACTER_SUCCESSFUL_UNSUBCRIPTION = '''Вы отписались от уведомлений'''
    CONFIRM = 'Подтвердить'
    NOT_CONFIRM = 'Не подтверждать'
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
