from utils.db_requests import get_user_by_id
from handlers.localization import Lang
from handlers.profile import user_profile_for_employer_handler
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton

from db.db_config import logger


async def user_profile_to_employer(callback_query, bot, user_id):
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

