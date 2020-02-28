import telebot
import os
import database

import constants

from telebot import types

TELEBOT_ENV_VARIABLE = 'KIK_TELEBOT_API_KEY'

api_key = os.environ[TELEBOT_ENV_VARIABLE]

if(api_key == None):
    raise Exception(
        '''Environment variable KIK_TELEBOT_API_KEY aren't present''')

bot = telebot.TeleBot(api_key)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        ask_nickname(message)
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                         '''/start - (пере) регистрация
                            /menu - показать меню
                         ''')
    elif message.text == "/menu":
        send_menu(message)


def ask_nickname(message):
    bot.send_message(message.from_user.id,
                     "Привет, давай я тебя запишу. Какой у тебя никнейм?")
    database.create_user(message.from_user.id)
    bot.register_next_step_handler(message, get_user_nickname)


def get_user_nickname(message):
    nickname = message.text
    database.update_user(message.from_user.id, 'real_name', message.text)
    ask_for_subscription(message)


def get_subscribe(message):
    phone = message.text
    database.update_user(message.from_user.id, 'phone', message.text)
    ask_for_subscription(message)


def ask_for_subscription(message):
    keyboard = types.InlineKeyboardMarkup()
    key_accept = types.InlineKeyboardButton(
        text='Подписаться', callback_data='subscribe'
    )
    keyboard.add(key_accept)
    key_skip = types.InlineKeyboardButton(
        text='Не хочу', callback_data='unsubscribe')
    keyboard.add(key_skip)

    question = 'Подписаться на уведомления?'
    bot.send_message(message.from_user.id, text=question,
                     reply_markup=keyboard)


def send_menu(message):
    user = database.get_user(message.from_user.id)

    keyboard = types.InlineKeyboardMarkup()
    key_azur = types.InlineKeyboardButton(
        text='!!! Азурегос !!!', callback_data='Азурегос'
    )
    keyboard.add(key_azur)
    key_kazzak = types.InlineKeyboardButton(
        text='!!! Каззак !!!', callback_data='Каззак')
    keyboard.add(key_kazzak)

    if user.subscribed == constants.DB_USER_SUBSCRIBED:
        unsubscribe_btn = types.InlineKeyboardButton(
            text="Отписаться", callback_data="unsubscribe")
        keyboard.add(unsubscribe_btn)
    else:
        subscribe_btn = types.InlineKeyboardButton(
            text="Подписаться", callback_data="subscribe")
        keyboard.add(subscribe_btn)

    question = 'Меню:'
    bot.send_message(message.from_user.id, text=question,
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "subscribe":
        database.set_subscription(
            call.from_user.id, constants.DB_USER_SUBSCRIBED)
        bot.send_message(call.from_user.id,
                         "Я тебя запомнил, уебок")
        send_menu(call)
    elif call.data == "unsubscribe":
        database.set_subscription(
            call.from_user.id, constants.DB_USER_UNSUBSCRIBED)
        bot.send_message(call.from_user.id,
                         "Я тебя запомнил, уебок")
        send_menu(call)
    elif call.data == 'Азурегос' or call.data == 'Каззак':
        notify_all(call.data, call.from_user.id)


def notify_all(boss, by):
    user = database.get_user(by)
    subscribed = database.get_subscribed_users()

    for subscriber in subscribed:
        bot.send_message(int(subscriber.name), '''%s обнаружил %s''' %
                         (user.real_name, boss))


bot.polling(none_stop=True, interval=0)
