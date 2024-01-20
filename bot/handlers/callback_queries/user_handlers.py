from utils.db_requests import ban_user_by_id, get_user_by_id
from handlers.localization import Lang
from buttons.emploee_menu import emploee_menu_markup


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
