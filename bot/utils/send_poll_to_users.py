from utils.db_requests import get_all_users_ids, get_user, update_user_by_id, delete_poll_by_id


async def send_poll_to_all_users(bot, poll, logger):
    for user_id in get_all_users_ids():
        try:
            if get_user(user_id).is_active:
                await bot.send_message(
                    chat_id=user_id,
                    text="Пожалуйста, примите участие в опросе, Ваше мнение капец как важно для нас!"
                )
                await bot.forward_message(
                    chat_id=user_id,
                    from_chat_id=poll.chat.id,
                    message_id=poll.message_id
                )
        except Exception:
            update_user_by_id(user_id, {'is_active':0})
            logger.warning(f"Чат с id={user_id} недоступен")


async def send_poll_to_user(bot, poll, poll_id, user_id, logger):
    try:
        if get_user(user_id).is_active:
            await bot.forward_message(
                    chat_id=user_id,
                    from_chat_id=user_id,
                    message_id=poll.message_id,
                )
    except Exception:
        await bot.send_message(chat_id=user_id,
                                text="Опрос был удален.")
        delete_poll_by_id(poll_id)
        logger.info(f"Опрос с id={poll_id} был удален")