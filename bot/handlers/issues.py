from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.db_config import *
from aiogram.enums import ParseMode
from handlers.localization import Lang
from utils.db_requests import get_all_tickets, get_solved_tickets, get_unsolved_tickets

async def show_issues_handler(bot, query, state, tickets_status="Все"):
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

        buttons = [[InlineKeyboardButton(text=issue_item.details, callback_data=f"issues_{issue_item.ticket_id}")] for issue_item in issues_on_page]

        if len(issues) > 5:
            buttons.append([
                InlineKeyboardButton(text="Предыдущая", callback_data="prev_ticket_page"),
                InlineKeyboardButton(text="Следующая", callback_data="next_ticket_page")
            ])

        issues_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(query.from_user.id, Lang.strings["ru"]["ticket_select_reply"], reply_markup=issues_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(query.from_user.id, Lang.strings["ru"]["ticket_select_error"])
