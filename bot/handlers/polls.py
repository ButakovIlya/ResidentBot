from utils.db_requests import get_all_users_ids, get_user, update_user_by_id, delete_poll_by_id
from buttons.polls_menu import return_to_polls_menu
from utils.db_requests import create_poll, get_all_active_polls, get_all_inactive_polls

from buttons.polls_menu import polls_markup
from buttons.emploee_menu import emploee_menu_markup

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_poll_handler(bot, message, logger):
    await bot.send_message(message.from_user.id, "Создайте и отправьте ваш опрос. Используйте кнопку прикрепить(в нижнем левом углу) -> Опрос",reply_markup=return_to_polls_menu)


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


async def create_new_poll_handler(message, state, bot, logger):
    if message.poll:
        all_options = message.poll.options
        options = []
        for option in all_options:
            options.append(option.text)
        question = message.poll.question

        poll = await bot.send_poll(
            chat_id=message.from_user.id,
            question=question,  
            options=options,  
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Пожалуйста, не удаляйте сообщение с опросом, иначе он перестанет быть доступным для остальных пользователей!"
        )

        # print(poll.__dict__)
        if poll:
            await send_poll_to_all_users(bot, poll, logger)

            poll_data = {
                'user_id': message.from_user.id,
                'poll_tg_id':poll.poll.id,
                'message_id': poll.message_id,
                'tittle': poll.poll.question,
                'is_closed': 0,
            }
            
            create_poll(poll_data)

        await state.clear()
    else:
        if message.text == 'Вернуться в меню опросов':
            await bot.send_message(message.chat.id, "Вы перенаправлены в управление опросами.", reply_markup=polls_markup)
            await state.clear()
            return

        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка, Вы прикрепили не опрос!",
            reply_markup=emploee_menu_markup
        )
        return


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


async def send_all_active_polls(bot, message):
    all_polls = get_all_active_polls(message.from_user.id)
    if list(all_polls):
        keyboard_buttons = []

        for poll in all_polls[:6]:
            poll_button = InlineKeyboardButton(text=poll.tittle, callback_data=f"poll_{poll.poll_tg_id}")
            keyboard_buttons.append([poll_button])
        
        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await bot.send_message(message.from_user.id, "Выберите нужный вам опрос.\n\nЧтобы закрыть опрос, откройте информацию о нем и нажмите кнопку 'Закрыть опрос'", reply_markup=keyboard_markup)
    else:
        await bot.send_message(message.from_user.id, "К сожалению, активных опросов нет")


async def send_all_inactive_polls(bot, message):
    all_polls = get_all_inactive_polls(message.from_user.id)
    if list(all_polls):
        keyboard_buttons = []

        for poll in all_polls[:6]:
            poll_button = InlineKeyboardButton(text=poll.tittle, callback_data=f"poll_{poll.poll_tg_id}")
            keyboard_buttons.append([poll_button])
        
        keyboard_markup = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await bot.send_message(message.from_user.id, "Выберите нужный вам опрос.\n\nЧтобы закрыть опрос, откройте информацию о нем и нажмите кнопку 'Закрыть опрос'", reply_markup=keyboard_markup)
    else:
        await bot.send_message(message.from_user.id, "К сожалению, завершенных опросов нет")
