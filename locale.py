class Locale:
    CHARACTER_NAME = '''Введите имя вашего основного персонажа'''
    BOT_HELP_MESSAGE = '''/start - регистрация
                        /menu - показать меню
                        '''
    BOT_MENU_MESSAGE = '''Меню:'''
    CHARACTER_SUBCRIPTION = '''Подписаться'''
    CHARACTER_UNSUBCRIPTION = '''Отписаться'''
    CHARACTER_QUESTION_ABOUT_SUBCRIPTION = '''Вы хотите подписаться на уведомления?'''
    CHARACTER_SUCCESSFUL_SUBCRIPTION = '''Вы подписались на уведомления'''
    CHARACTER_SUCCESSFUL_UNSUBCRIPTION = '''Вы отписались от уведомлений'''
    BOSS_AZUREGOS = '!!! Азурегос !!!'
    BOSS_KAZZAK = '!!! Каззак !!!'

    def BOSS_NOTIFICATION(user_name, boss_name):
        return '''%s обнаружил %s''' %
        (user_name, boss_name)


class LocaleExeptions:
    ENVIRONMENT_API_KEY_NOT_FOUND = '''Environment variable KIK_TELEBOT_API_KEY aren't present'''
