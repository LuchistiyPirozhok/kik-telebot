from constants import Statuses, BossMasks
from typing import List
from database import User

StatusesMap = {
    Statuses.BANNED: 'заблокирован',
    Statuses.ACTIVE: 'пользователь',
    Statuses.ADMIN: 'администратор'
}


class Locale:
    CHARACTER_NAME = 'Введите имя вашего основного персонажа:'
    GUILD_NAME = 'Введите название гильдии'
    BOT_HELP_MESSAGE = ('/start - регистрация\n'
                        '/menu - показать меню\n')
    BOT_MENU_MESSAGE = 'Главное меню'
    BOT_MENU_MESSAGE_BOSSES = 'Обнаружен мировой босс'
    BOT_MENU_MESSAGE_BOSSES_DESCRIPTION = 'Внимание! При нажатии по кнопке с боссом вы отправите сообщение всем пользователям с включенной подпиской. Кого вы обнаружили?'
    BOT_ADMIN_MENU = 'Административная часть'
    CHARACTER_SUBCRIPTION = 'Подписаться'
    CHARACTER_UNSUBCRIPTION = 'Отписаться'
    CHARACTER_GUILD = 'В какой гильдии вы состоите?'
    CHARACTER_QUESTION_ABOUT_SUBCRIPTION = 'Вы хотите подписаться на уведомления?'
    CHARACTER_SUCCESSFUL_SUBCRIPTION = 'Вы подписались на уведомления'
    CHARACTER_SUCCESSFUL_UNSUBCRIPTION = 'Вы отписались от уведомлений'
    CONFIRM = 'Зарегистрировать пользователя'
    NOT_CONFIRM = 'Забанить пользователя'
    DELETE = 'Удалить пользователя из БД'
    REGISTER_FIRST = 'Сначала необходимо завершить реигстрацию'
    CHARACTER_REG_SUCCESSFUL = 'Вам были выданы права пользователя'
    CHARACTER_REG_FAILED = 'К сожалению, вы не прошли регистрацию из-за ошибок в имени персонажа или выборе гильдии. Пожалуйста, попробуйте зарегистрироваться снова'
    CHARACTER_REG_BANNED = 'К сожалению, вы были заблокированы. По всем вопросам обращайтесь к администратору в дискорде'
    CHARACTER_REG_PENDING = 'Заявка на регистрацию уже была отправлена. Пожалуйста, ожидайте ее подтверждения'
    GO_BACK = 'Назад'
    BOSS_CHECK_EXPIRED = 'Прошло больше часа с последнего обновления. Встаньте в караул снова'

    @staticmethod
    def BOSS_NOTIFICATION(user_name, boss_name):
        return f'Внимание! {user_name} обнаружил {boss_name}'

    @staticmethod
    def DUPLICATE_CHARACTER_NAME(user_name):
        return f'Вы авторизованы как {user_name}'

    @staticmethod
    def REGISTRATION_COMPLETE(reg_code):
        return f'Для завершения регистрации вам нужно сообщить следующий код администратору в дискорде (Dorim#1317), либо представителю бота в вашей гильдии: {reg_code}'

    @staticmethod
    def REGISTRATION_COMPLETE_CONFIRM(user_name, reg_code):
        return f'Поступил запрос регистрации от пользователя {user_name} со следующим кодом {reg_code}. Подтвердить?'


class Admin:
    ALL_USERS = 'Вывести таблицу со всеми пользователями'
    ALL_GUILDS = 'Вывести таблицу со всеми гильдиями'
    ALL_PENDING_USERS = 'Вывести список ожидающих подтверждения регистрации пользователей'
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
    CHANGE_USER_STATUS_BY_ID_SUCCESSFUL = 'Статус пользователя изменен'
    CHANGE_USER_STATUS_BY_ID_ADD_ADMIN = 'Вам были выданы права администратора'
    ADD_ADMIN = 'Выдать права администратора'
    NO_PERMITTIONS = 'У вас отсутствуют права на выполнение этого действия'
    MESSAGE_TEXT = 'Введите сообщение, которое будет отправлено всем активным пользователям с включенной подпиской.'
    MESSAGE_TO_ALL_TITLE = 'Сообщение всем подписчикам'

    @staticmethod
    def MESSAGE_TO_ALL(user_name, message_to_all):
        return f'Администратор {user_name} сообщает: "{message_to_all}"'

    @staticmethod
    def ADMIN_NOTIFICATION(admin_name, user_name, user_id, user_status):
        return f'Администратор {admin_name} изменил права аккаунта с именем {user_name} (ID: {user_id}). Новые права: {StatusesMap[user_status]}'

    @staticmethod
    def ADMIN_NOTIFICATION_DELETE_USER(admin_name, user_name, user_id):
        return f'Администратор {admin_name} удалил пользователя {user_name} (ID: {user_id}).'


class LocaleExceptions:
    ENVIRONMENT_API_KEY_NOT_FOUND = '''Environment variable KIK_TELEBOT_API_KEY aren't present'''


class Bosses:
    AZUREGOS = 'Азурегоса'
    KAZZAK = 'Каззака'
    EMERISS = 'Эмирисса'
    LETHON = 'Летона'
    YSONDRE = 'Исондру'
    TAERAR = 'Таэрара'
    ALL = 'Всех'
    NONE = 'Никого'

    @staticmethod
    def getList():
        return [Bosses.AZUREGOS, Bosses.KAZZAK, Bosses.EMERISS, Bosses.LETHON, Bosses.YSONDRE, Bosses.TAERAR]


BossMaskMap = {
    BossMasks.AZUREGOS: Bosses.AZUREGOS,
    BossMasks.KAZZAK: Bosses.KAZZAK,
    BossMasks.EMERISS: Bosses.EMERISS,
    BossMasks.LETHON: Bosses.LETHON,
    BossMasks.YSONDRE: Bosses.YSONDRE,
    BossMasks.TAERAR: Bosses.TAERAR,
    BossMasks.ALL: Bosses.ALL,
    BossMasks.NONE: Bosses.NONE
}


class BossCheck:
    BEGIN_CHECKING = 'Встать в караул'
    CHECK_LIST = 'Кто в карауле'
    WILL_NOTIFY = 'Я буду оповещать о появлении босса(ов)'

    @staticmethod
    def NOBODY(boss_name: str):
        return f'Похоже никто не следит за появлением {boss_name}'

    @staticmethod
    def CHECK(boss_mask: int, users: List[User]):
        user_count = len(users)
        if(user_count == 0):
            return BossCheck.NOBODY(BossMaskMap[boss_mask])

        separator = ", "
        more = f'... +{user_count-10}' if(user_count > 10) else ''
        user_names = map(lambda u: u.character_name, users[:10])
        user_list = f'`{separator.join(user_names)}`'

        return f'За появлением {BossMaskMap[boss_mask]} следит(ят):\n{user_list}`{more}`'


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
    ALL_PENDING_USERS = 'all_pending_users'
    ALL_BANNED_USERS = 'all_banned_users'
    CHANGE_USER_STATUS = 'change_user_status'
    DELETE_USER = 'delete_user'
    ALL_ADMINS = 'all_admins'
    MESSAGE_TO_ALL = 'message_to_all'
    ADD_ADMIN = 'add_admin'
    CHECK = 'check_boss'
    WORLD_BOSSES = 'world_bosses'

    @staticmethod
    def BOSS_CHECK(boss: str):
        return f'boss_check:{boss}'
