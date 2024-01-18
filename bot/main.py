import asyncio
import json
import os
from typing import List, Optional

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, LabeledPrice, Poll as AioPoll, PollOption

from dotenv import load_dotenv

from StateGroups.NewsState import *
from StateGroups.ProblemState import *
from buttons.emploee_menu import emploee_menu_markup
from buttons.main_menu import main_menu_markup
from buttons.registration import select_role_markup
from buttons.empl_back_to_menu import *
from db.db_config import *
from dict.issues_status import *
from dict.problems_dict import problem_texts
from handlers.contact import contact_uk_handler, extract_problem_description, problem_about_handler
from handlers.issues import show_issues_handler
from handlers.localization import Lang, get_localized_message
from handlers.meter_data import meter_router
from handlers.news import *
from handlers.check_tikects import *
from handlers.registration import registration_router
from handlers.user_profile import *
from middleware.album import MediaGroupMiddleware
from middleware.employer_verif import EmployeeMiddleware
from middleware.message_log import MessagesLog
from middleware.throttling import AntiSpamMiddleware
from middleware.verification import RegistrationMiddleware
from utils.all_employees_messenger import all_employees_messenger
from utils.all_users_messenger import all_confirmed_users_messenger
from utils.date_time import get_current_date_and_time
from utils.db_image_loader import send_ticket_images_to_user, send_news_images_to_user, send_ticket_images_to_employer
from utils.db_requests import *
from utils.media_processing import media_processing
from utils.folders_checking import create_directories


logging.basicConfig(level=logging.INFO)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

main_router = Router()
employer_router = Router()
last_router = Router()

main_router.message.middleware.register(RegistrationMiddleware())
employer_router.message.middleware.register(EmployeeMiddleware())
dp.message.middleware.register(AntiSpamMiddleware())
dp.message.middleware.register(MessagesLog())
dp.message.middleware.register(MediaGroupMiddleware())

dp.include_router(registration_router)
dp.include_router(meter_router)
dp.include_router(employer_router)
dp.include_router(main_router)
dp.include_router(last_router)

class PollState(StatesGroup):
    WaitingForPoll = State()

@dp.message(CommandStart())
async def on_start_command(message: types.Message):
    tg_id = message.from_user.id
    User.set_session(Session())

    if not User.exists(tg_id):
        await message.answer(Lang.strings["ru"]["start_message"], reply_markup=select_role_markup)
    else:
        user: User = User.get_user_by_id(tg_id)
        if user.is_confirmed:
            await message.answer("Вы находитесь в главном меню", reply_markup=main_menu_markup)
        else:
            message_text = "Ожидайте верификации" if user.residential_complex else "Продолжайте регистрацию"
            await message.answer(message_text)
    User.close_session()


@main_router.message(lambda message: message.text == "Вернуться в главное меню")
async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(Lang.strings["ru"]["return_to_main_menu"], reply_markup=main_menu_markup)


@main_router.message(lambda message: message.text == "Связаться с УК")
async def contact_uk(message: types.Message):
    await contact_uk_handler(message.from_user.id, bot)


@main_router.callback_query(lambda query: query.data in problem_texts.keys())
async def contact_select_problem_type(query: CallbackQuery, state: FSMContext):
    problem_type = problem_texts.get(query.data)
    if problem_type:
        await state.update_data(problem_type=problem_type)
        await state.set_state(ProblemState.problem_type)
        await bot.delete_message(query.message.chat.id, query.message.message_id)
        await problem_about_handler(query.from_user.id, bot, problem_type)
        # Добавить else(Exception)

@main_router.message(ProblemState.problem_type)
async def save_description(
    message: types.Message, state: FSMContext, album: Optional[List[Message]] = None
):
    problem_description = await extract_problem_description(message)
    files_id, caption = await media_processing(problem_description, album, message, bot)

    if problem_description:
        if len(problem_description) <= 10:
            await message.answer(
                "Описание проблемы должно содержать более 10 символов. Пожалуйста, уточните проблему и, при необходимости, повторно приложите фото."
            )
            return
    else:
        await message.answer(
                "Нужно добавить описание проблемы!"
            )
        return
    # fix with not photo


    await all_employees_messenger(files_id, caption, bot)

    response_msg = get_localized_message("ru", "send_issue_success")
    await bot.send_message(message.from_user.id, response_msg, reply_markup=main_menu_markup)

    user_data = await state.get_data()
    problem_type = user_data.get("problem_type")

    await state.clear()
    
    current_date, current_time = get_current_date_and_time()

    ticket_type_id = get_id_by_ticket_type_name(problem_type)

    images = {f"image{i+1}": f"{file_id}" for i, file_id in enumerate(files_id)} if files_id else None
    
    dict_images = []
    if not images == None:
        for k, v in images.items():
            dict_images.append({k: v})
        dict_images = json.dumps(dict_images, ensure_ascii=False)

    new_ticket = {
        "user_id": message.from_user.id,
        "ticket_type_id": ticket_type_id,
        "is_solved": False,
        "date": current_date,
        "time": current_time,
        "details": problem_description,
        "images": dict_images,
    }
    create_ticket(new_ticket)


@main_router.message(lambda message: message.text == "Профиль")
async def user_profile(message: types.Message):
    user_profile = await user_profile_handler(message.from_user.id)
    if user_profile:
        await bot.send_message(message.from_user.id, user_profile)
    else:
        response_msg = get_localized_message("ru", "profile_error")
        await bot.send_message(message.from_user.id, response_msg)


@main_router.message(lambda message: message.text == "Новости")
async def get_news(message: types.Message, state: FSMContext):
    await get_news_handler(message.from_user.id, bot, state)


@main_router.callback_query(lambda c: c.data in ["prev_page", "next_page"])
async def change_news_page(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    current_page = await state.get_state() or 0
    all_news = News.get_all()
    pages = [all_news[i:i + 5] for i in range(0, len(all_news), 5)]

    if callback_query.data == "prev_page" and current_page > 0:
        current_page -= 1
    elif callback_query.data == "next_page" and current_page + 1 < len(pages):
        current_page += 1

    await state.set_state(current_page)

    await get_news_handler(user_id, bot, state)

    await bot.delete_message(user_id, message_id)


@main_router.callback_query(lambda c: c.data.startswith("news_"))
async def show_news_details(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    news_id = int(callback_query.data.split("_")[1])
    news_item = News.get_by_id(news_id)

    # fix only photo 

    if news_item:
        news_details = f"Заголовок: {news_item.topic}\n\n{news_item.body}"

        await send_news_images_to_user(news_item, bot, user_id, news_details)
       
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["news_open_info_error"])

    await bot.delete_message(user_id, message_id)


@main_router.message(lambda message: message.text == "Проверить мои заявки")
async def check_tikects(message: types.Message, state: FSMContext):
    await check_tikects_handler(message.from_user.id, bot, state)

@main_router.callback_query(lambda c: c.data.startswith("ticket_"))
async def show_unchecked_tikects(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    tikect_id = int(callback_query.data.split("_")[1])
    tikect_item = get_ticket_by_id(tikect_id)

    if tikect_item:
        tikect_details = f"Тип заявки: {tikect_item.type}\n\nТекст: {tikect_item.details}"
        await send_ticket_images_to_user(tikect_item, bot, user_id, tikect_details, tikect_item)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["news_open_info_error"])

    await bot.delete_message(user_id, message_id)


@main_router.message(lambda message: message.text == "Оплата ЖКУ")
async def create_invoice(message: types.Message):
    PRICE = LabeledPrice(label="Квитанция на оплату", amount=500 * 100)
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Квитанция №1",
        description="Гор. вода 1 - 45.243\nГор. вода 2 - 32.987\nХол. вода 1 - 78.543",
        provider_token=PAYMENT_TOKEN,
        currency="rub",
        prices=[PRICE],
        start_parameter="some",
        payload="test-invoice"
    )


@main_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# @main_router.message(SuccessfulPayment)
# async def successful_payment(message: types.Message):
#     await bot.send_message(message.from_user.id,
#                            f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно !")

# Delete in future
@employer_router.message(lambda message: message.text == "Сотрудник")
async def development_mode(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы вошли в меню разработки Сотрудника",
                           reply_markup=emploee_menu_markup)

@employer_router.message(lambda message: message.text == "Вернуться назад")
async def return_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(Lang.strings["ru"]["return_to_employer_menu"], reply_markup=emploee_menu_markup)

@employer_router.message(lambda message: message.text == "Статистика")
async def show_house_statistics(message: types.Message):
    with open('fake_data/house_stat.json', 'r') as file:
        statistics_data = json.load(file)

    statistics_message = (
        "Статистика дома ул. Пермская, д. 18\n\n"
        f"Общее количество жителей: {statistics_data['residents_total']}\n"
        f"Зарегистрированные жители: {statistics_data['registered_residents']}\n"
        f"Новые жители за текущий месяц: {statistics_data['new_residents_this_month']}\n"
        f"Всего выставлено счетов за месяц: {statistics_data['total_invoices_this_month']}\n"
        f"Оплаченные счета за месяц: {statistics_data['paid_invoices_this_month']}\n"
        f"Неоплаченные счета за месяц: {statistics_data['unpaid_invoices_this_month']}\n"
        f"Количество сотрудников в системе: {statistics_data['employees_total']}\n"
    )


    await message.answer(statistics_message)


@employer_router.message(lambda message: message.text == "Создать новость")
async def start_create_news(message: types.Message, state: FSMContext):
    await message.answer("Введите заголовок новости: ", reply_markup=return_back_button_markup)
    await state.set_state(NewsStates.InputTopic)


@employer_router.message(NewsStates.InputTopic)
async def create_news_select_topic(message: types.Message, state: FSMContext):
    topic = message.text
    if len(topic) < 5 or len(topic) > 30:
        await message.answer('Заголовок новости должен содержать от 5 до 30 символов. Введите заголовок заново:', reply_markup=return_back_button_markup)
        return

    await message.answer('Теперь введите текст новости: ', reply_markup=return_back_button_markup)
    await state.update_data({"topic": message.text})
    await state.set_state(NewsStates.InputMessage)


@employer_router.message(NewsStates.InputMessage)
async def process_message(message: types.Message, state: FSMContext,
                          album: Optional[List[Message]] = None):
    news_text = await extract_problem_description(message)
    files_id, caption = await media_processing(news_text, album, message, bot)

    if len(caption) < 5 or len(caption) > 500:
        await message.answer('Текст новости должен содержать от 5 до 500 символов. Введите текст заново:')
        return

    images = {f"image{i+1}": f"{file_id}" for i, file_id in enumerate(files_id)} if files_id else None

    dict_images = []
    if not images == None:
        for k, v in images.items():
            dict_images.append({k: v})
        dict_images = json.dumps(dict_images, ensure_ascii=False)

    data = await state.get_data()
    topic = data['topic']
    news_data = {
        "topic": topic,
        "date": datetime.date.today(),
        "time": datetime.datetime.now().time(),
        "body": news_text,
        "tags": "test",
        "images": dict_images
    }
    create_new_news(news_data)

    message_text = f'Появилась новость: <b>{topic}</b>\n{caption}'
    await all_confirmed_users_messenger(files_id, message_text, bot)

    await state.clear()
    await message.answer("Новость успешно отправлена всем жителям!")


@employer_router.message(lambda message: message.text == "Заявки жителей")
async def show_issues(message: types.Message, state: FSMContext):
    tickets_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
            [
                KeyboardButton(text="Все заявки"),
                KeyboardButton(text="Закрытые заявки"),
                KeyboardButton(text="Открытые заявки"),
            ],
            [
                KeyboardButton(text="Вернуться назад"),
            ],
        ]
    )   

    await bot.send_message(message.chat.id, "Выберите категорию заявок:", reply_markup=tickets_markup)

@employer_router.message(lambda message: message.text in ["Все заявки", "Закрытые заявки", "Открытые заявки"])
async def show_issues_by_status(message: types.Message, state: FSMContext):
    await show_issues_handler(bot, message, state, message.text.split(' ')[0])


@employer_router.callback_query(lambda c: c.data in ["prev_ticket_page", "next_ticket_page"])
async def change_ticket_page(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    current_page = await state.get_state() or 0
    all_tickets = get_all_tickets()
    pages = [all_tickets[i:i + 5] for i in range(0, len(all_tickets), 5)]

    if callback_query.data == "prev_ticket_page" and current_page > 0:
        current_page -= 1
    elif callback_query.data == "next_ticket_page" and current_page + 1 < len(pages):
        current_page += 1

    await state.set_state(current_page)

    await show_issues_handler(bot, callback_query, state)

    await bot.delete_message(user_id, message_id)


@employer_router.callback_query(lambda c: c.data.startswith("issues_"))
async def show_news_details(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    issues_id = int(callback_query.data.split("_")[1])
    issue_item = get_ticket_by_id(issues_id)

    if issue_item:
        issue_details = f"Тип обращения: {issue_item.type}\nОписание обращения: {issue_item.details}\nДата обращения: {issue_item.date} {issue_item.time}\nЗакрыта: {issue_item.is_solved}\n\nАвтор заявки: {issue_item.tg_link}"
       
        await send_ticket_images_to_employer(issue_item, bot, user_id, issue_details, issue_item)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["ticket_open_info_error"])

    await bot.delete_message(user_id, message_id)


@employer_router.message(lambda message: message.text == "Создать опрос")
async def set_poll(message: types.Message, state:FSMContext):
    await state.set_state(PollState.WaitingForPoll)
    await bot.send_message(message.from_user.id, "Создайте и отправьте ваш опрос. Используйте кнопку прикрепить(в нижнем левом углу) -> Опрос",reply_markup=return_back_button_markup)


@employer_router.message(PollState.WaitingForPoll)
async def start_command(message: types.Message, state:FSMContext):
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
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ошибка, Вы прикрепили не опрос!",
            reply_markup=emploee_menu_markup
        )
        return

@employer_router.message(lambda message: message.text == "Активные опросы")
async def look_all_active_polls(message: types.Message):
    all_polls = get_all_active_polls(message.from_user.id)
    if list(all_polls):
        keyboard_buttons = []

        for poll in all_polls[:6]:
            poll_button = types.InlineKeyboardButton(text=poll.tittle, callback_data=f"poll_{poll.poll_tg_id}")
            keyboard_buttons.append([poll_button])
        
        keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await bot.send_message(message.from_user.id, "Выберите нужный вам опрос.\n\nЧтобы закрыть опрос, откройте информацию о нем и нажмите кнопку 'Закрыть опрос'", reply_markup=keyboard_markup)
    else:
        await bot.send_message(message.from_user.id, "К сожалению, активных опросов нет")
    
@employer_router.message(lambda message: message.text == "Завершенные опросы")
async def look_all_inactive_polls(message: types.Message):
    all_polls = get_all_inactive_polls(message.from_user.id)
    if list(all_polls):
        keyboard_buttons = []

        for poll in all_polls[:6]:
            poll_button = types.InlineKeyboardButton(text=poll.tittle, callback_data=f"poll_{poll.poll_tg_id}")
            keyboard_buttons.append([poll_button])
        
        keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        await bot.send_message(message.from_user.id, "Выберите нужный вам опрос.\n\nЧтобы закрыть опрос, откройте информацию о нем и нажмите кнопку 'Закрыть опрос'", reply_markup=keyboard_markup)
    else:
        await bot.send_message(message.from_user.id, "К сожалению, завершенных опросов нет")

@last_router.message()
async def unknown_message(message: types.Message):
    await message.answer("Неизвестная команда!")


@employer_router.callback_query(lambda c: c.data.startswith("poll"))
async def show_poll_details(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    poll_id = int(callback_query.data.split("_")[1])
    poll_item = get_poll_by_id(poll_id)

    # keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=[types.InlineKeyboardButton(text="Закрыть опрос", callback_data=f"closepoll_{poll_id}")])

    if poll_item:
        try:
            await bot.forward_message(
                    chat_id=user_id,
                    from_chat_id=user_id,
                    message_id=poll_item.message_id,
            )
        except Exception:
            await bot.send_message(chat_id=user_id,
                                   text="Опрос был удален.")
            Poll.delete_by_id(poll_id)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["news_open_info_error"])

    await bot.delete_message(user_id, message_id)



@employer_router.callback_query(lambda c: c.data.startswith("ban_user_"))
async def ban_user(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    user_to_ban = get_user_by_id(user_id)
    if user_to_ban:
        ban_user_by_id(user_id)
        await bot.send_message(from_user_id, f"Польватель {user_to_ban.username} успешно заблокирован.", reply_markup=emploee_menu_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_to_ban_error"])

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

@employer_router.callback_query(lambda c: c.data.startswith("close_ticket_"))
async def close_ticket(callback_query: types.CallbackQuery, state: FSMContext):
    ticket_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    ticket_to_close = get_ticket_by_id(ticket_id)
    if ticket_to_close:
        close_ticket_by_id(ticket_id)
        await bot.send_message(from_user_id, f"Заявка №{ticket_to_close.ticket_id} успешно закрыта.", reply_markup=emploee_menu_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_to_ban_error"])
    
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@employer_router.callback_query(lambda c: c.data.startswith("delete_ticket_"))
async def delete_ticket(callback_query: types.CallbackQuery, state: FSMContext):
    ticket_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    ticket_to_delete = get_ticket_by_id(ticket_id)
    if ticket_to_delete:
        if delete_ticket_by_id(ticket_id):
            await bot.send_message(from_user_id, f"Заявка №{ticket_to_delete.ticket_id} успешно отменена.", reply_markup=main_menu_markup)
        else: 
            await bot.send_message(from_user_id, Lang.strings["ru"]["cancel_ticket_error"])
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["cancel_ticket_error"])

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

async def main():
    # await get_payment_notification(bot) Допилить
    create_directories()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
