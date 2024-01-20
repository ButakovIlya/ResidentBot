from utils.db_requests import get_ticket_by_id, get_all_tickets, delete_ticket_by_id, close_ticket_by_id
from utils.db_image_loader import send_ticket_images_to_user, send_ticket_images_to_employer
from handlers.issues import show_issues_handler
from handlers.localization import Lang
from buttons.emploee_menu import emploee_menu_markup
from buttons.main_menu import main_menu_markup

from datetime import datetime

async def show_unchecked_tikect_func(callback_query, state, bot):
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