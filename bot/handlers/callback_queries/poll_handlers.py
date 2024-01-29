from utils.db_requests import get_poll_by_id
from handlers.polls import send_poll_to_all_users, send_poll_to_user

from handlers.localization import Lang
from db.db_config import logger

async def show_poll_details_func(callback_query, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    poll_id = int(callback_query.data.split("_")[1])
    poll_item = get_poll_by_id(poll_id)

    if poll_item:
        await send_poll_to_user(bot, poll_item, poll_id, user_id, logger)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["news_open_info_error"])

    await bot.delete_message(user_id, message_id)
