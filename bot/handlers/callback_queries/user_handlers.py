from utils.db_requests import ban_user_by_id, get_user_by_id, get_all_users
from handlers.localization import Lang
from handlers.users import send_all_users_by_complex_id
from handlers.profile import user_profile_for_employer_handler
from buttons.emploee_menu import emploee_menu_markup

from db.db_config import logger

async def ban_user_func(callback_query, bot):
    user_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    user_to_ban = get_user_by_id(user_id)
    if user_to_ban:
        ban_user_by_id(user_id)
        await bot.send_message(from_user_id, f"Польватель {user_to_ban.username} успешно заблокирован.", reply_markup=emploee_menu_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_to_ban_error"])

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def user_profile_to_employer_func(callback_query, bot):
    user_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    user_profile = await user_profile_for_employer_handler(user_id, logger)

    # добавить кнопки заблокировать или разблокировать

    if user_profile:
        await bot.send_message(from_user_id, user_profile)
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

