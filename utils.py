from telebot import types

from typing import Callable, List, Dict


class DialogElement:
    def __init__(self: DialogElement, message: str, responseHandler: Callable[[object]]):
        self.message = message
        self.responseHandler = responseHandler


def create_menu(buttons: Dict[str, str]):
    keyboard = types.InlineKeyboardMarkup()

    for text, data in buttons:
        keyboard_key = types.InlineKeyboardButton(
            text=text, callback_data=data
        )

        keyboard.add(keyboard_key)

    return keyboard


def map_dialog_element(bot, dialog_element: DialogElement, nextHandler: Callable[[object]]):
    def handler(message):
        if dialog_element.message != None:
            bot.send_message(message.from_user.id, dialog_element.message)
        if callable(dialog_element.responseHandler):
            dialog_element.responseHandler(message)
        if(callable(nextHandler)):
            bot.register_next_step_handler_by_chat_id(
                message.from_user.id, nextHandler)
    return handler


def create_dialog(dialog_elements: List[DialogElement], bot):
    dialog_length = len(dialog_elements)
    current_function = map_dialog_element(
        bot, dialog_elements[dialog_length-1])

    for i in reversed(range(dialog_length-1)):
        current_function = map_dialog_element(
            bot, dialog_elements[i], current_function)

    return current_function
