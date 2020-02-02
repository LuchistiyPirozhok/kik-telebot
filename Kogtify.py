import telebot

import database

import consts

from database import *
from telebot import types

USER_SUBSCIRBED = 1
USER_UNSUBSCRIBED = 0

bot = telebot.TeleBot('1022712943:AAH-svQMnwb-J94mtcqydxnNsm786L3x0Wk')


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
    create_user(message.from_user.id)
    bot.register_next_step_handler(message, get_user_nickname)


def get_user_nickname(message):
    nickname = message.text
    update_user(message.from_user.id, 'real_name', message.text)
    # ask_for_phone(message)
    ask_for_subscription(message)


# def ask_for_phone(message):
#    keyboard = types.InlineKeyboardMarkup()
#    key_add = types.InlineKeyboardButton(
#        text="Хочу", callback_data='add_number')
#    key_skip = types.InlineKeyboardButton(
#        text='Не хочу', callback_data='skip_number')
#    keyboard.add(key_skip)
#
#    question = 'Если хочешь, укажи номер телефона'
#    bot.send_message(message.from_user.id, text=question,
#                     reply_markup=keyboard)


def get_subscribe(message):
    phone = message.text
    update_user(message.from_user.id, 'phone', message.text)
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
    user = get_user(message.from_user.id)

    keyboard = types.InlineKeyboardMarkup()
    key_azur = types.InlineKeyboardButton(
        text='!!! Азурегос !!!', callback_data='Азурегос'
    )
    keyboard.add(key_azur)
    key_kazzak = types.InlineKeyboardButton(
        text='!!! Каззак !!!', callback_data='Каззак')
    keyboard.add(key_kazzak)

    if user.subscribed == consts.DB_USER_SUBSCRIBED:
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
    # if call.data == "skip_number":
    #    ask_for_subscription(call)
    # elif call.data == "add_number":
    #    bot.send_message(call.from_user.id,"Введите номер в формате (8 123 456 78 90)")
    #    bot.register_next_step_handler(message, get_subscribe)
    if call.data == "subscribe":
        set_subscription(call.from_user.id, consts.DB_USER_SUBSCRIBED)
        bot.send_message(call.from_user.id,
                         "Я тебя запомнил, уебок")
        send_menu(call)
    elif call.data == "unsubscribe":
        set_subscription(call.from_user.id, consts.DB_USER_UNSUBSCRIBED)
        bot.send_message(call.from_user.id,
                         "Я тебя запомнил, уебок")
        send_menu(call)
    elif call.data == 'Азурегос' or call.data == 'Каззак':
        notify_all(call.data, call.from_user.id)


def notify_all(boss, by):
    user = get_user(by)
    subscribed = get_subscribed_users()

    for subscriber in subscribed:
        bot.send_message(int(subscriber.name), '''%s обнаружил %s''' %
                         (user.real_name, boss))


bot.polling(none_stop=True, interval=0)
