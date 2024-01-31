from utils.db_requests import get_ticket_by_id, get_all_tickets, delete_ticket_by_id, close_ticket_by_id, get_user_by_id
from utils.db_requests import get_all_tickets_by_user_id
from handlers.utils.tickets import send_ticket_images_to_user, send_ticket_images_to_employer
from handlers.tickets import show_issues_handler, send_user_ticket_data_func
from handlers.localization import Lang
from buttons.emploee_menu import emploee_menu_markup
from buttons.main_menu import main_menu_markup

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.formatters import format_datetime

from datetime import datetime

async def show_unchecked_ticket_func(callback_query, state, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    tikect_id = int(callback_query.data.split("_")[1])
    ticket_item = get_ticket_by_id(tikect_id)

    if ticket_item:
        tikect_details = f"Тип заявки: {ticket_item.type}\n\nТекст: {ticket_item.details}"
        await send_ticket_images_to_user(ticket_item, bot, user_id, tikect_details, ticket_item)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["news_open_info_error"])

    await bot.delete_message(user_id, message_id)


async def check_ticket_func(callback_query, state, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    ticket_id = int(callback_query.data.split("_")[2])
    ticket_item = get_ticket_by_id(ticket_id)

    if ticket_item:
        ticket_details = f"Тип заявки: {ticket_item.type}\n\nТекст: {ticket_item.details}\n\n"
        ticket_details += f"Дата обращения: {ticket_item.date} {ticket_item.time}\n\n"
        is_solved = '✅ Обращение рассмотрено и решено.' if ticket_item.is_solved else '❔ Обращение не решено.'
        ticket_details += is_solved
        await send_ticket_images_to_employer(ticket_item, bot, user_id, ticket_details, ticket_item)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["news_open_info_error"])

    await bot.delete_message(user_id, message_id)   


async def change_ticket_page_func(callback_query, state, bot):
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


async def show_issues_details_func(callback_query, state, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    issues_id = int(callback_query.data.split("_")[1])
    issue_item = get_ticket_by_id(issues_id)

    if issue_item:
        datetime_object = datetime.strptime(f"{issue_item.date} { issue_item.time}", "%Y-%m-%d %H:%M:%S")
        formatted_datetime = datetime_object.strftime("%H:%M %d.%m.%Y")
        issue_details = (
                            f"Тип обращения: {issue_item.type}\n"
                            f"Описание обращения: {issue_item.details}\n"
                            f"Дата обращения: {formatted_datetime}\n"
                            f"Закрыта: {'Да' if issue_item.is_solved else 'Нет'}\n\n"
                            f"Автор заявки: {issue_item.tg_link}"
                        )
       
        await send_ticket_images_to_employer(issue_item, bot, user_id, issue_details, issue_item)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["ticket_open_info_error"])

    await bot.delete_message(user_id, message_id)


async def close_ticket_func(callback_query, state, bot):
    ticket_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    ticket_to_close = get_ticket_by_id(ticket_id)
    if ticket_to_close:
        close_ticket_by_id(ticket_id)
        await bot.send_message(from_user_id, f"Заявка №{ticket_to_close.ticket_id} успешно закрыта.", reply_markup=emploee_menu_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_to_ban_error"])
    
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def delete_ticket_func(callback_query, state, bot):
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


async def check_user_tickets_func(callback_query,state, bot):
    from_user_id = callback_query.from_user.id
    to_user_id = int(str(callback_query.data).split('_')[3])
    user = get_user_by_id(to_user_id)
    await state.update_data(to_user_id = to_user_id)

    all_tickets = get_all_tickets_by_user_id(to_user_id)

    if all_tickets:
        state_data = await state.get_data()
        current_page = max(0, min(state_data.get('user_tickets_page', 0), len(all_tickets) // 5))
        tickets_on_page = all_tickets[current_page*5 : (current_page+1)*5]

        buttons = []
        for ticket_item in tickets_on_page:
            is_solved = '❔' if not ticket_item.is_solved else '✅' 
            button_text = is_solved + ' ' + f"{ticket_item.details}"
            callback_data = f"check_ticket_{ticket_item.ticket_id}"
            
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
            buttons.append([button])        

        if len(all_tickets) > 5:
            buttons.append([
                InlineKeyboardButton(text="Предыдущая", callback_data="prev_user_ticket_page"),
                InlineKeyboardButton(text="Следующая", callback_data="next_user_ticket_page"),
            ])
            buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{to_user_id}")])
        else:
            buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{to_user_id}")])

        tickets_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(from_user_id, f"Заявки жителя @{user.username}", reply_markup=tickets_markup)
    else:
        buttons = []
        buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{to_user_id}")])
        tickets_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await bot.send_message(from_user_id, Lang.strings["ru"]["no_user_tickets_to_check"], reply_markup=tickets_markup)

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def change_user_ticket_page_func(callback_query, state, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    state_data = await state.get_data()
    current_page = state_data.get('user_ticket_page', 0)

    if 'to_user_id' in state_data:
        to_user_id = state_data['to_user_id']
    else:
        response_msg = "Ошибка, вы нажали неактуальную кнопку!"
        await bot.send_message(user_id, response_msg, reply_markup=emploee_menu_markup)
        return


    all_tickets = get_all_tickets_by_user_id(to_user_id)
    pages = [all_tickets[i:i + 5] for i in range(0, len(all_tickets), 5)]

    if callback_query.data == "prev_user_ticket_page" and current_page > 0:
        current_page -= 1
    elif callback_query.data == "next_user_ticket_page" and current_page + 1 < len(pages):
        current_page += 1

    await state.set_data({
        'user_ticket_page':current_page,
    })
    
    await send_user_ticket_data_func(state, bot, to_user_id)

    await bot.delete_message(user_id, message_id)