import telebot
import os
import database
import botutils

import random

from telebot import types
from localization import LocaleExceptions, Locale, Bosses, Messages
from constants import Database, Commands, Statuses
from database import User

from typing import List

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
          #          bot.send_message(message.from_user.id, Locale.DUPLICATE_CHARACTER_NAME(user.character_name))
            # send_menu(message)
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
    send_menu(message)


def get_user_guild(message):
    guilds = database.get_all_guilds()
    bot.send_message(message.from_user.id, Locale.CHARACTER_GUILD,
                     reply_markup=botutils.create_menu_from_guilds(guilds))


def get_registration_code(user: User):
    code = random_digits()
    database.update_user(user.telegram_id,
                         Database.FIELD_REG_CODE,  code)
    bot.send_message(user.telegram_id, Locale.REGISTRATION_COMPLETE(code))
 #  bot.send_message('463808631', Locale.REGISTRATION_COMPLETE_CONFIRM(user.character_name,code))

    database.update_user(
        user.telegram_id, Database.FIELD_STATUS, Statuses.PENDING)
    keyboard = botutils.create_menu({
        #        Locale.CONFIRM: f'confirm:{user.telegram_id}',
        #        Locale.NOT_CONFIRM: f'not_confirm:{user.telegram_id}',
        #        Locale.DELETE: f'delete:{user.telegram_id}'
        Locale.CONFIRM: f'{Messages.CONFIRM}:{user.telegram_id}',
        Locale.NOT_CONFIRM: f'{Messages.NOT_CONFIRM}:{user.telegram_id}',
        Locale.DELETE: f'{Messages.DELETE}:{user.telegram_id}'
    })

    question = Locale.REGISTRATION_COMPLETE_CONFIRM(user.character_name, code)
    bot.send_message('463808631', text=question,
                     reply_markup=keyboard)


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
        #      'Добавить гильдию': 'add_guild',
        #       Locale.BOSS_AZUREGOS: 'Азурегос',
        #       Locale.BOSS_KAZZAK: 'Каззак'
        Bosses.AZUREGOS: Bosses.AZUREGOS,
        Bosses.KAZZAK: Bosses.KAZZAK,
        Bosses.EMERISS: Bosses.EMERISS,
        Bosses.LETHON: Bosses.LETHON,
        Bosses.YSONDRE: Bosses.YSONDRE,
        Bosses.TAERAR: Bosses.TAERAR
    }

    if user.subscribed == Database.DB_USER_SUBSCRIBED:
        menu[Locale.CHARACTER_UNSUBCRIPTION] = Messages.UNSUBSCRIBE
    else:
        menu[Locale.CHARACTER_SUBCRIPTION] = Messages.SUBSCRIBE

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
                                                               [Statuses.ACTIVE,
                                                                Statuses.ADMIN,
                                                                Statuses.SUPERVISOR]))
def callback_worker(call):
    if call.data == Messages.SUBSCRIBE:
        database.set_subscription(
            call.from_user.id, Database.DB_USER_SUBSCRIBED)
        bot.send_message(call.from_user.id,
                         Locale.CHARACTER_SUCCESSFUL_SUBCRIPTION)
        send_menu(call)
    elif call.data == Messages.UNSUBSCRIBE:
        database.set_subscription(
            call.from_user.id, Database.DB_USER_UNSUBSCRIBED)
        bot.send_message(call.from_user.id,
                         Locale.CHARACTER_SUCCESSFUL_UNSUBCRIPTION)
        send_menu(call)

    elif call.data == Messages.ADD_GUILD:
        bot.send_message(call.from_user.id, Locale.GUILD_NAME)
        bot.register_next_step_handler_by_chat_id(call.from_user.id, add_guild)

    elif call.data.startswith(Messages.CONFIRM):
        user_id = call.data.split(':')[1]
        database.update_user(
            user_id, Database.FIELD_STATUS, Statuses.ACTIVE)
        bot.send_message(user_id, Locale.CHARACTER_REG_SUCCESSFUL)
        ask_for_subscription_by_userid(user_id)

    elif call.data.startswith(Messages.NOT_CONFIRM):
        user_id = call.data.split(':')[1]
        database.update_user(
            user_id, Database.FIELD_STATUS, Statuses.BANNED)
        bot.send_message(user_id, Locale.CHARACTER_REG_BANNED)

    elif call.data.startswith(Messages.DELETE):
        user_id = call.data.split(':')[1]
        database.remove_user(user_id)
        bot.send_message(user_id, Locale.CHARACTER_REG_FAILED)
    elif call.data in Bosses.getList():
        notify_all(call.data, call.from_user.id)
 #       get_telegram_id_by_userid(user_id)


def notify_all(boss, by):
    user = database.get_user(by)
    if user.status >= Statuses.ACTIVE:
        subscribed = database.get_subscribed_users()

        for subscriber in subscribed:
            bot.send_message(int(subscriber.telegram_id),
                             Locale.BOSS_NOTIFICATION(user.character_name, boss))


bot.polling(none_stop=True, interval=0)
