import telebot
import os
import database


from telebot import types
from localization import LocaleExeptions, Locale
from constants import Database, Commands

TELEBOT_ENV_VARIABLE = 'KIK_TELEBOT_API_KEY'

api_key = os.environ[TELEBOT_ENV_VARIABLE]

if(api_key == None):
    raise Exception(LocaleExeptions.ENVIRONMENT_API_KEY_NOT_FOUND)

bot = telebot.TeleBot(api_key)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == Commands.START:
        ask_nickname(message)
    elif message.text == Commands.HELP:
        bot.send_message(message.from_user.id, Locale.BOT_HELP_MESSAGE)
    elif message.text == Commands.MENU:
        send_menu(message)


def ask_nickname(message):
    bot.send_message(message.from_user.id, Locale.CHARACTER_NAME)
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
        text=Locale.CHARACTER_SUBCRIPTION, callback_data='subscribe'
    )
    keyboard.add(key_accept)
    key_skip = types.InlineKeyboardButton(
        text=Locale.CHARACTER_UNSUBCRIPTION, callback_data='unsubscribe')
    keyboard.add(key_skip)

    question = Locale.CHARACTER_QUESTION_ABOUT_SUBCRIPTION
    bot.send_message(message.from_user.id, text=question,
                     reply_markup=keyboard)


def send_menu(message):
    user = database.get_user(message.from_user.id)

    keyboard = types.InlineKeyboardMarkup()
    key_azur = types.InlineKeyboardButton(
        text=Locale.BOSS_AZUREGOS, callback_data='Азурегос'
    )
    keyboard.add(key_azur)
    key_kazzak = types.InlineKeyboardButton(
        text=Locale.BOSS_KAZZAK, callback_data='Каззак')
    keyboard.add(key_kazzak)

    if user.subscribed == Database.DB_USER_SUBSCRIBED:
        unsubscribe_btn = types.InlineKeyboardButton(
            text=Locale.CHARACTER_UNSUBCRIPTION, callback_data="unsubscribe")
        keyboard.add(unsubscribe_btn)
    else:
        subscribe_btn = types.InlineKeyboardButton(
            text=Locale.CHARACTER_SUBCRIPTION, callback_data="subscribe")
        keyboard.add(subscribe_btn)

    question = Locale.BOT_MENU_MESSAGE
    bot.send_message(message.from_user.id, text=question,
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "subscribe":
        database.set_subscription(
            call.from_user.id, Database.DB_USER_SUBSCRIBED)
        bot.send_message(call.from_user.id,
                         Locale.CHARACTER_SUCCESSFUL_SUBCRIPTION)
        send_menu(call)
    elif call.data == "unsubscribe":
        database.set_subscription(
            call.from_user.id, Database.DB_USER_UNSUBSCRIBED)
        bot.send_message(call.from_user.id,
                         Locale.CHARACTER_SUCCESSFUL_UNSUBCRIPTION)
        send_menu(call)
    elif call.data == 'Азурегос' or call.data == 'Каззак':
        notify_all(call.data, call.from_user.id)


def notify_all(boss, by):
    user = database.get_user(by)
    subscribed = database.get_subscribed_users()

    for subscriber in subscribed:
        bot.send_message(int(subscriber.name),
                         Locale.BOSS_NOTIFICATION(user.real_name, boss))


bot.polling(none_stop=True, interval=0)
