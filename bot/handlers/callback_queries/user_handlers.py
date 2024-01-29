from utils.db_requests import ban_user_by_id, unban_user_by_id, get_user_by_id, get_all_users
from handlers.localization import Lang
from handlers.users import send_all_users_by_complex_id
from handlers.profile import user_profile_for_employer_handler
from buttons.emploee_menu import emploee_menu_markup
from buttons.users_menu import users_markup

from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

from db.db_config import logger

async def ban_user_func(callback_query, bot):
    user_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    user_to_ban = get_user_by_id(user_id)
    if user_to_ban:
        ban_user_by_id(user_id)
        await bot.send_message(from_user_id, f"Польватель {user_to_ban.username} успешно заблокирован.", reply_markup=users_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_to_unban_error"])

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

async def unban_user_func(callback_query, bot):
    user_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    user_to_ban = get_user_by_id(user_id)
    if user_to_ban:
        unban_user_by_id(user_id)
        await bot.send_message(from_user_id, f"Польватель {user_to_ban.username} успешно разблокирован.", reply_markup=users_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_to_ban_error"])

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def user_profile_to_employer_func(callback_query, bot):
    user_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    user_profile = await user_profile_for_employer_handler(user_id, logger)
    user = get_user_by_id(user_id)

    user_buttons = []
    if user.is_banned:
        ban_user_button = InlineKeyboardButton(text=f"Разблокировать {user.username}", callback_data=f"unban_user_{user_id}")
    else:
        ban_user_button = InlineKeyboardButton(text=f"Заблокировать {user.username}", callback_data=f"ban_user_{user_id}")

    check_meters_button = InlineKeyboardButton(text=f"Посмотреть показания", callback_data=f"check_user_meters_{user_id}")
    check_tickets_button = InlineKeyboardButton(text=f"Посмотреть заявки", callback_data=f"check_user_tickets_{user_id}")

    user_buttons.append([check_meters_button])
    user_buttons.append([check_tickets_button])
    user_buttons.append([ban_user_button])
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=user_buttons)

    if user_profile:
        await bot.send_message(from_user_id, user_profile, reply_markup=keyboard_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_profile_error"])

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def change_user_page_func(callback_query, state, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    current_page = await state.get_state() or 0
    all_news = get_all_users()
    pages = [all_news[i:i + 5] for i in range(0, len(all_news), 5)]

    if callback_query.data == "user_prev_page" and current_page > 0:
        current_page -= 1
    elif callback_query.data == "user_next_page" and current_page + 1 < len(pages):
        current_page += 1

    await state.set_state(current_page)

    await send_all_users_by_complex_id(user_id, bot, state)

    await bot.delete_message(user_id, message_id)


async def ban_user_func(callback_query, bot):
    user_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    user_to_ban = get_user_by_id(user_id)
    if user_to_ban:
        ban_user_by_id(user_id)
        await bot.send_message(from_user_id, f"Польватель {user_to_ban.username} успешно заблокирован.", reply_markup=users_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_to_unban_error"])

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    