from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.db_config import *
from aiogram.enums import ParseMode
from handlers.localization import Lang
from utils.db_requests import get_all_tickets, get_solved_tickets, get_unsolved_tickets, get_all_by_user_id_and_status
from utils.db_requests import get_all_tickets_by_user_id, get_user_by_id

async def show_issues_handler(bot, message, state, tickets_status="Все"):
    if tickets_status == "Все":
        issues = get_all_tickets()
    elif tickets_status == "Закрытые":
        issues = get_solved_tickets()
    elif tickets_status == "Открытые":
        issues = get_unsolved_tickets()
    else:
        issues = get_all_tickets()
        


    if issues:
        current_page = max(0, min(await state.get_state() or 0, len(issues) // 5))
        issues_on_page = issues[current_page*5 : (current_page+1)*5]

        buttons = [[InlineKeyboardButton(text=issue_item.details, callback_data=f"check_ticket_{issue_item.ticket_id}")] for issue_item in issues_on_page]

        if len(issues) > 5:
            buttons.append([
                InlineKeyboardButton(text="Предыдущая", callback_data="prev_ticket_page"),
                InlineKeyboardButton(text="Следующая", callback_data="next_ticket_page")
            ])

        issues_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(message.from_user.id, Lang.strings["ru"]["ticket_select_reply"], reply_markup=issues_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(message.from_user.id, Lang.strings["ru"]["ticket_select_error"])


async def check_tikects_handler(user_id, bot, state):
 
    all_tickets = get_all_by_user_id_and_status(user_id, 0)

    if all_tickets:
        current_page = max(0, min(await state.get_state() or 0, len(all_tickets) // 5))
        tickets_on_page = all_tickets[current_page*5 : (current_page+1)*5]

        buttons = [[InlineKeyboardButton(text=ticket_item.details, callback_data=f"ticket_{ticket_item.ticket_id}")] for ticket_item in tickets_on_page]

        if len(all_tickets) > 5:
            buttons.append([
                InlineKeyboardButton(text="Предыдущая", callback_data="prev_ticket_page"),
                InlineKeyboardButton(text="Следующая", callback_data="next_ticket_page")
            ])

        news_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(user_id, Lang.strings["ru"]["ticket_select_reply"], reply_markup=news_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["ticket_select_error"])


async def send_user_ticket_data_func(state, bot, user_id):
    all_tickets = get_all_tickets_by_user_id(user_id)
    user = get_user_by_id(user_id)

    if all_tickets:
        state_data = await state.get_data()
        current_page = max(0, min(state_data.get('user_ticket_page', 0), len(all_tickets) // 5))
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
            buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{user_id}")])
        else:
            buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{user_id}")])

        tickets_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await state.set_data({'to_user_id':user_id})
        await bot.send_message(user_id, f"Заявки жителя @{user.username}", reply_markup=tickets_markup)
    else:
        buttons = []
        buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{user_id}")])
        tickets_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await bot.send_message(user_id, Lang.strings["ru"]["no_user_tickets_to_check"], reply_markup=tickets_markup)

