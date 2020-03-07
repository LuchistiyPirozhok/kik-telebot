from telebot import types

from database import Guild,User

from typing import Callable, List, Dict


class DialogElement:
    def __init__(user, message: str, responseHandler: Callable[[object], None]):
        user.message = message
        user.responseHandler = responseHandler


def create_menu(buttons: Dict[str, str]):
    keyboard = types.InlineKeyboardMarkup()

    return add_keys(keyboard,buttons)

def add_keys(keyboard,buttons:Dict[str,str]):
    for text, data in buttons.items():
        keyboard_key = types.InlineKeyboardButton(
            text=text, callback_data=data
        )

        keyboard.add(keyboard_key)

    return keyboard


def create_menu_from_guilds(guilds: List[Guild]):
    keyboard = types.InlineKeyboardMarkup()
    for guild in guilds:
        key = types.InlineKeyboardButton(
            text=guild.guild_name, callback_data=f'guild:{guild.guild_name}'
        )
        keyboard.add(key)
    return keyboard

def set_lng(value,n:int):
    if(value==None):
        return ' '*n

    text = str(value)
    txt_len = len(text) 

    if txt_len < n:
       diff = n - txt_len
       text_with_space = text+' '*diff
       return text_with_space
    
    return text

def format_users_as_table(users:List[User]):
    def map_user_to_table_string(user:User):
        return f'''
            `{set_lng('Персонаж:',25)}`{user.character_name}
            `{set_lng('ID:',25)}`{user.telegram_id}
            `{set_lng('Подписка:',25)}`{user.subscribed}
            `{set_lng('Гильдия:',25)}`{user.guild_name}
            `{set_lng('Код регистрации:',25)}`{user.reg_code}
            `{set_lng('Статус:',25)}`{user.status}    
        '''

    users_as_table_rows = map(lambda u: map_user_to_table_string(u), users)
    users_as_str = "\n".join(users_as_table_rows)
    return users_as_str

def format_guilds_as_table(guilds:List[Guild]):
 
    def map_guild_to_table_string(guild:Guild):
        return f'''
            `{set_lng('Гильдия:',25)}`{guild.guild_name}
        '''

    guilds_as_table_rows = map(lambda u: map_guild_to_table_string(u), guilds)
    guilds_as_str = "\n".join(guilds_as_table_rows)
    return guilds_as_str