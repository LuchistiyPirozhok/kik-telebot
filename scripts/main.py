from typing import List
from database import User
from constants import Database, Commands, Statuses, BossMasks
from localization import LocaleExceptions, Locale, Bosses, Messages, BossCheck, Admin

import telebot
import os
import database
import botutils

import random

from telebot import types

TELEBOT_ENV_VARIABLE = 'KIK_TELEBOT_API_KEY'

api_key = os.environ[TELEBOT_ENV_VARIABLE]

if(api_key == None):
    raise Exception(LocaleExceptions.ENVIRONMENT_API_KEY_NOT_FOUND)

bot = telebot.TeleBot(api_key)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == Commands.START:
        user = database.get_user(message.from_user.id)
        if(user == None):
            get_telegram_id(message)
        else:
            handle_user_status(user)
    elif message.text == Commands.HELP:
        bot.send_message(message.from_user.id, Locale.BOT_HELP_MESSAGE)
    elif message.text == Commands.MENU:
        send_menu(message)


def handle_user_status(user: User):
    if(user.status == Statuses.UNREGISTERED):
        get_registration_code(user)
    elif(user.status == Statuses.BANNED):
        bot.send_message(user.telegram_id, Locale.CHARACTER_REG_BANNED)
    elif (user.status == Statuses.PENDING):
        bot.send_message(user.telegram_id, Locale.CHARACTER_REG_PENDING)
    else:
        send_menu_by_user(user)


def get_telegram_id_by_userid(telegram_id: str):
    bot.send_message(telegram_id, Locale.CHARACTER_NAME)
    database.create_user(telegram_id)
    database.get_user(telegram_id)
    bot.register_next_step_handler_by_chat_id(telegram_id, get_user_nickname)


def get_telegram_id(message):
    get_telegram_id_by_userid(message.from_user.id)


def get_user_nickname(message):
    print(f'Get user: {message.text}')
    nickname = message.text
    database.update_user(message.from_user.id,
                         Database.FIELD_CHARACTER_NAME, message.text)
    get_user_guild(message)


def add_guild(message):
    guild_name = message.text
    database.insert_guild(message.text)
#    send_menu(message)


def get_user_guild(message):
    guilds = database.get_all_guilds()
    bot.send_message(message.from_user.id, Locale.CHARACTER_GUILD,
                     reply_markup=botutils.create_menu_from_guilds(guilds))


def get_registration_code(user: User):
    code = random_digits()
    admins = database.get_all_admins()
    database.update_user(user.telegram_id,
                         Database.FIELD_REG_CODE,  code)
    bot.send_message(user.telegram_id, Locale.REGISTRATION_COMPLETE(code))
    database.update_user(
        user.telegram_id, Database.FIELD_STATUS, Statuses.PENDING)
    keyboard = create_confirm_user_menu(user)

    question = Locale.REGISTRATION_COMPLETE_CONFIRM(user.character_name, code)
#   bot.send_message('463808631', text=question,reply_markup=keyboard)

    for admin in admins:
        if(admin.subscribed==Database.USER_SUBSCRIBED):
            bot.send_message(admin.telegram_id,text=question,reply_markup=keyboard)



def random_digits():
    return str(random.randrange(100000, 1000000))


def ask_for_subscription_by_userid(user_id: str):
    keyboard = botutils.create_menu({
        Locale.CHARACTER_SUBCRIPTION: Messages.SUBSCRIBE,
        Locale.CHARACTER_UNSUBCRIPTION: Messages.UNSUBSCRIBE
    })

    question = Locale.CHARACTER_QUESTION_ABOUT_SUBCRIPTION
    bot.send_message(user_id, text=question,
                     reply_markup=keyboard)


def ask_for_subscription(message):
    ask_for_subscription_by_userid(message.from_user.id)


def send_menu(message):
    user = database.get_user(message.from_user.id)
    send_menu_by_user(user)


def send_menu_by_user(user):
    menu = {
        Bosses.AZUREGOS: Bosses.AZUREGOS,
        Bosses.KAZZAK: Bosses.KAZZAK,
        Bosses.EMERISS: Bosses.EMERISS,
        Bosses.LETHON: Bosses.LETHON,
        Bosses.YSONDRE: Bosses.YSONDRE,
        Bosses.TAERAR: Bosses.TAERAR,
        BossCheck.BEGIN_CHECKING: BossCheck.BEGIN_CHECKING,
        BossCheck.CHECK_LIST:  BossCheck.CHECK_LIST
    }

    if user.subscribed == Database.USER_SUBSCRIBED:
        menu[Locale.CHARACTER_UNSUBCRIPTION] = Messages.UNSUBSCRIBE
    else:
        menu[Locale.CHARACTER_SUBCRIPTION] = Messages.SUBSCRIBE

    if user.status >= Statuses.ADMIN:
        menu[Locale.BOT_ADMIN_MENU] = Messages.ADMIN

    question = Locale.BOT_MENU_MESSAGE
    bot.send_message(user.telegram_id, text=question,
                     reply_markup=botutils.create_menu(menu))


def check_permission(user_id: str, permissions: List[int]):
    user = database.get_user(user_id)

    return user != None and user.status in permissions


@bot.callback_query_handler(func=lambda call:  check_permission(call.from_user.id, [Statuses.BANNED]))
def handle_banned_click(call):
    bot.send_message(call.from_user.id, Locale.CHARACTER_REG_BANNED)


@bot.callback_query_handler(func=lambda call: database.get_user(call.from_user.id) == None or check_permission(call.from_user.id, [Statuses.UNREGISTERED]))
def handle_unregistered_click(call):
    user = database.get_user(call.from_user.id)
    if user != None and call.data.startswith(Messages.GUILD):
        guild_name = call.data.split(':')[1]
        database.update_user(
            call.from_user.id, Database.FIELD_GUILD_NAME, guild_name)

        handle_user_status(user)
    else:
        bot.send_message(call.from_user.id, Locale.REGISTER_FIRST)


@bot.callback_query_handler(func=lambda call:  check_permission(call.from_user.id, [Statuses.PENDING]))
def handle_unregistered_click(call):
    bot.send_message(call.from_user.id, Locale.REGISTER_FIRST)


@bot.callback_query_handler(func=lambda call: check_permission(call.from_user.id,
                                                               [Statuses.ADMIN,
                                                                Statuses.SUPERVISOR]))
def handle_admin_click(call):
    if call.data == Messages.ADMIN:
        menu = {
            Admin.ALL_USERS: Messages.ALL_USERS,
            Admin.ALL_GUILDS: Messages.ALL_GUILDS,
            Admin.ALL_PENDUNG_USERS: Messages.ALL_PENDUNG_USERS,
            Admin.ALL_BANNED_USERS: Messages.ALL_BANNED_USERS,
            Admin.ALL_ADMINS: Messages.ALL_ADMINS,
            Admin.CHANGE_USER_STATUS: Messages.CHANGE_USER_STATUS,
            Admin.ADD_GUILD: Messages.ADD_GUILD,
            Admin.MESSAGE_TO_ALL_TITLE: Messages.MESSAGE_TO_ALL
        }

        question = Locale.BOT_ADMIN_MENU
        bot.send_message(call.from_user.id, text=question,
                         reply_markup=botutils.create_menu(menu))

    elif call.data == Messages.ALL_USERS:
        users = database.get_all_users()
        bot.send_message(chat_id=call.from_user.id, text=botutils.format_users_as_table(
            users), parse_mode='Markdown')

    elif call.data == Messages.ALL_GUILDS:
        guilds = database.get_all_guilds()
        bot.send_message(chat_id=call.from_user.id, text=botutils.format_guilds_as_table(
            guilds), parse_mode='Markdown')

    elif call.data == Messages.ALL_PENDUNG_USERS:
        pending_users = database.get_all_pending_users()
        if len(pending_users) == 0:
            bot.send_message(call.from_user.id, Admin.USERS_EMPTY)
        else:
            bot.send_message(chat_id=call.from_user.id, text=botutils.format_users_as_table(
                pending_users), parse_mode='Markdown')

    elif call.data == Messages.ALL_BANNED_USERS:
        banned_users = database.get_all_banned_users()
        if len(banned_users) == 0:
            bot.send_message(call.from_user.id, Admin.USERS_EMPTY)
        else:
            bot.send_message(chat_id=call.from_user.id, text=botutils.format_users_as_table(
                banned_users), parse_mode='Markdown')

    elif call.data == Messages.ALL_ADMINS:
        all_admins = database.get_all_admins()
        if len(all_admins) == 0:
            bot.send_message(call.from_user.id, Admin.USERS_EMPTY)
        else:
            bot.send_message(chat_id=call.from_user.id, text=botutils.format_users_as_table(
                all_admins), parse_mode='Markdown')

    elif call.data == Messages.ADD_GUILD:
        bot.send_message(call.from_user.id, Locale.GUILD_NAME)
        bot.register_next_step_handler_by_chat_id(call.from_user.id, add_guild)

###
    elif call.data == Messages.MESSAGE_TO_ALL:
        bot.send_message(call.from_user.id, Admin.MESSAGE_TEXT)
        bot.register_next_step_handler_by_chat_id(
            call.from_user.id, message_to_subcribed_users)

###
    elif call.data == Messages.CHANGE_USER_STATUS:
        bot.send_message(call.from_user.id, Admin.SELECT_USER_STATUS_BY_ID)
        bot.register_next_step_handler_by_chat_id(
            call.from_user.id, user_id_exists)

    elif call.data.startswith(Messages.ADD_ADMIN):
        user_id = call.data.split(':')[1]
        database.update_user(
            user_id, Database.FIELD_STATUS, Statuses.ADMIN)
        bot.send_message(user_id, Admin.CHANGE_USER_STATUS_BY_ID_ADD_ADMIN)
        bot.send_message(call.from_user.id,
                         Admin.CHANGE_USER_STATUS_BY_ID_SUCCESSFUL)
        notify_all_admins(call.from_user.id, user_id)

    elif call.data.startswith(Messages.CONFIRM):
        user_id = call.data.split(':')[1]
        database.update_user(
            user_id, Database.FIELD_STATUS, Statuses.ACTIVE)
        bot.send_message(user_id, Locale.CHARACTER_REG_SUCCESSFUL)
        ask_for_subscription_by_userid(user_id)
        bot.send_message(call.from_user.id,
                         Admin.CHANGE_USER_STATUS_BY_ID_SUCCESSFUL)
        notify_all_admins(call.from_user.id, user_id)

    elif call.data.startswith(Messages.NOT_CONFIRM):
        user_id = call.data.split(':')[1]
        database.update_user(
            user_id, Database.FIELD_STATUS, Statuses.BANNED)
        bot.send_message(user_id, Locale.CHARACTER_REG_BANNED)
        bot.send_message(call.from_user.id,
                         Admin.CHANGE_USER_STATUS_BY_ID_SUCCESSFUL)
        notify_all_admins(call.from_user.id, user_id)

    elif call.data.startswith(Messages.DELETE):
        user_id = call.data.split(':')[1]
        notify_all_admins_about_delete(call.from_user.id, user_id)
        database.remove_user(user_id)
        bot.send_message(user_id, Locale.CHARACTER_REG_FAILED)

    elif call.data == Messages.ADMIN:
        database.set_subscription(
            call.from_user.id, Database.DB_USER_SUBSCRIBED)
        bot.send_message(call.from_user.id,
                         Locale.CHARACTER_SUCCESSFUL_SUBCRIPTION)

    else:
        callback_worker(call)


def message_to_subcribed_users(message):
    message_to_all = message.text
    user = database.get_user(message.from_user.id)
    if user.status in [Statuses.ACTIVE, Statuses.ADMIN, Statuses.SUPERVISOR]:
        subscribed = database.get_subscribed_users()
        for subscriber in subscribed:
            bot.send_message(int(subscriber.telegram_id),
                             Admin.MESSAGE_TO_ALL(user.character_name, message_to_all))


def user_id_exists(message):
    user_id = message.text
    user = database.get_user(user_id)
    admin_user = database.get_user(message.from_user.id)

    if user == None:
        bot.send_message(message.from_user.id,
                         Admin.SELECT_USER_STATUS_BY_ID_FAILED)
    elif admin_user.status == Statuses.ADMIN and user.status in [Statuses.ACTIVE, Statuses.BANNED, Statuses.PENDING]:
        keyboard = create_confirm_user_menu(user)
        bot.send_message(message.from_user.id, Admin.SELECT_USER_STATUS_BY_ID_SUCCESSFUL,
                         reply_markup=keyboard)
    elif admin_user.status == Statuses.SUPERVISOR:

        keyboard = create_confirm_user_menu(user)
        botutils.add_keys(keyboard, {
            Admin.ADD_ADMIN: f'{Messages.ADD_ADMIN}:{user.telegram_id}',
        })
        bot.send_message(message.from_user.id, Admin.SELECT_USER_STATUS_BY_ID_SUCCESSFUL,
                         reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, Admin.NO_PERMITTIONS)


def create_confirm_user_menu(user: User):
    return botutils.create_menu({
        Locale.CONFIRM: f'{Messages.CONFIRM}:{user.telegram_id}',
        Locale.NOT_CONFIRM: f'{Messages.NOT_CONFIRM}:{user.telegram_id}',
        Locale.DELETE: f'{Messages.DELETE}:{user.telegram_id}'
    })


@bot.callback_query_handler(func=lambda call: check_permission(call.from_user.id, [Statuses.ACTIVE]))
def callback_worker(call):
    if call.data == Messages.SUBSCRIBE:
        database.set_subscription(
            call.from_user.id, Database.USER_SUBSCRIBED)
        bot.send_message(call.from_user.id,
                         Locale.CHARACTER_SUCCESSFUL_SUBCRIPTION)
        send_menu(call)
    elif call.data == Messages.UNSUBSCRIBE:
        database.set_subscription(
            call.from_user.id, Database.USER_UNSUBSCRIBED)
        bot.send_message(call.from_user.id,
                         Locale.CHARACTER_SUCCESSFUL_UNSUBCRIPTION)
        send_menu(call)

    elif call.data in Bosses.getList():
        notify_all(call.data, call.from_user.id)
    elif call.data == BossCheck.BEGIN_CHECKING:
        send_check_menu(call.from_user.id)

    elif call.data == BossCheck.CHECK_LIST:
        text = ''
        for boss_mask in BossMasks.boss_list():
            text += f'{BossCheck.CHECK(boss_mask,database.get_users_by_mask(boss_mask))}\n\n'

        bot.send_message(call.from_user.id, text)

    elif call.data.startswith(Messages.CHECK):
        boss_mask = int(call.data.split(':')[1])
        if(boss_mask in [BossMasks.ALL, BossMasks.NONE]):
            database.update_user(
                call.from_user.id, Database.FIELD_BOSS_MASK, boss_mask)
        else:
            database.toggle_user_mask(boss_mask, call.from_user.id)
        send_check_menu(call.from_user.id)


def notify_all(boss, by):
    user = database.get_user(by)
    if user.status >= Statuses.ACTIVE:
        subscribed = database.get_subscribed_users()

        for subscriber in subscribed:
            bot.send_message(int(subscriber.telegram_id),
                             Locale.BOSS_NOTIFICATION(user.character_name, boss))

#################


def send_check_menu(telegram_id: str):
    user = database.get_user(telegram_id)
    keyboard = {}

    for boss_mask in BossMasks.get_list():
        btn_text = botutils.format_boss_check_button_text(boss_mask, user)
        keyboard[btn_text] = f'{Messages.CHECK}:{boss_mask}'

    bot.send_message(telegram_id, BossCheck.WILL_NOTIFY,
                     reply_markup=botutils.create_menu(keyboard))


def notify_all_admins(admin_id, user_id):
    user = database.get_user(user_id)
    admin = database.get_user(admin_id)
    if admin.status in [Statuses.ADMIN, Statuses.SUPERVISOR]:
        subscribed = database.get_subscribed_users()

        for subscriber in subscribed:
            bot.send_message(int(subscriber.telegram_id),
                             Admin.ADMIN_NOTIFICATION(admin.character_name,
                                                      user.character_name,
                                                      user.telegram_id,
                                                      user.status))


def notify_all_admins_about_delete(admin_id, user_id):
    user = database.get_user(user_id)
    admin = database.get_user(admin_id)
    if admin.status in [Statuses.ADMIN, Statuses.SUPERVISOR]:
        subscribed = database.get_subscribed_users()

        for subscriber in subscribed:
            bot.send_message(int(subscriber.telegram_id),
                             Admin.ADMIN_NOTIFICATION_DELETE_USER(admin.character_name,
                                                                  user.character_name,
                                                                  user.telegram_id))

bot.polling(none_stop=True, interval=0)
