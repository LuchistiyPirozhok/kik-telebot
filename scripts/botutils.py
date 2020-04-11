from database import Guild, User
from localization import Bosses, BossMaskMap, Messages, Locale
from constants import BossMasks
from typing import Callable, List, Dict
from database import Guild, User
from telebot import types
from bot_common import get_timestamp


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


def create_page_menu(page: int, page_count: int):
    keyboard = types.InlineKeyboardMarkup(5)
    buttons = (
        types.InlineKeyboardButton(
            text='<<', callback_data=f'{Messages.ALL_USERS}:{0}'),
        types.InlineKeyboardButton(
            text='<', callback_data=f'{Messages.ALL_USERS}:{max(page-1,0)}'),
        types.InlineKeyboardButton(
            text=f'{page+1}/{page_count}', callback_data=f'{Messages.ALL_USERS}:{page}'),
        types.InlineKeyboardButton(
            text='>', callback_data=f'{Messages.ALL_USERS}:{min(page+1,page_count-1)}'),  # using page_count-1 because it
                                                                                          # should be index, which,
                                                                                          # obviously, starts from 0
        types.InlineKeyboardButton(
            text='>>', callback_data=f'{Messages.ALL_USERS}:{page_count-1}')  # same there
    )
    keyboard.add(*buttons)

    keyboard.add(
        types.InlineKeyboardButton(
            text=Locale.GO_BACK, callback_data=Messages.ADMIN
        )
    )

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
        current = get_timestamp()

        return (f"`{set_lng('Персонаж: ',12)}`{user.character_name}\n"
                f"`{set_lng('ID: ',12)}`{user.telegram_id}\n"
                f"`{set_lng('Подписка: ',12)}`{user.subscribed}\n"
                f"`{set_lng('Гильдия: ',12)}`{user.guild_name}\n"
                f"`{set_lng('Код: ',12)}`{user.reg_code}\n"
                f"`{set_lng('Статус: ',12)}`{user.status}\n"
                f"`{set_lng('Чекает: ',12)}`{user.boss_mask}\n"
                f"`{set_lng('В карауле: ',12)}`{f'{current - user.last_update}  мин' if user.boss_mask > 0 else '-'}"
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
    return boss_mask > 0 and (boss_mask & user.boss_mask == boss_mask)


def format_boss_check_button_text(boss_mask: int, user: User):
    text = BossMaskMap[boss_mask]
    return f'{set_lng(text,15)}{"✓" if is_user_checking_boss(boss_mask,user) else ""}'
