from database import Guild, User
from localization import Bosses
from constants import BossMasks
from typing import Callable, List, Dict
from database import Guild, User
from telebot import types


def create_menu(buttons: Dict[str, str]):
    keyboard = types.InlineKeyboardMarkup()

    return add_keys(keyboard, buttons)


def add_keys(keyboard, buttons: Dict[str, str]):
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


def set_lng(value, n: int):
    if(value == None):
        return ' '*n

    text = str(value)
    txt_len = len(text)

    if txt_len < n:
        diff = n - txt_len
        text_with_space = text+' '*diff
        return text_with_space

    return text


def format_users_as_table(users: List[User]):
    def map_user_to_table_string(user: User):
        return (f"`{set_lng('Персонаж: ',12)}`{user.character_name}\n"
                f"`{set_lng('ID: ',12)}`{user.telegram_id}\n"
                f"`{set_lng('Подписка: ',12)}`{user.subscribed}\n"
                f"`{set_lng('Гильдия: ',12)}`{user.guild_name}\n"
                f"`{set_lng('Код: ',12)}`{user.reg_code}\n"
                f"`{set_lng('Статус: ',12)}`{user.status}\n"
                )

    users_as_table_rows = map(lambda u: map_user_to_table_string(u), users)
    users_as_str = "\n".join(users_as_table_rows)
    return users_as_str


def format_guilds_as_table(guilds: List[Guild]):

    def map_guild_to_table_string(guild: Guild):
        return f'''
            `{set_lng('Гильдия:',25)}`{guild.guild_name}
        '''

    guilds_as_table_rows = map(lambda u: map_guild_to_table_string(u), guilds)
    guilds_as_str = "\n".join(guilds_as_table_rows)
    return guilds_as_str


def is_user_checking_boss(boss_mask: int, user: User):
    return boss_mask & user.boss_mask == boss_mask


def format_boss_check_button_text(boss_mask: int, user: User):
    #  AZUREGOS = 0b000001
    # KAZZAK = 0b000010
    # EMERISS = 0b000100
    # LETHON = 0b001000
    # YSONDRE = 0b010000
    # TAERAR = 0b100000
    text = Bosses.TAERAR
