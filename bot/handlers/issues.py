from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db.db_config import *
from aiogram.enums import ParseMode
from handlers.localization import Lang
from utils.db_requests import get_all_tickets

async def show_issues_handler(bot, query, state):
    issues = get_all_tickets()

    if issues:
        current_page = max(0, min(await state.get_state() or 0, len(issues) // 5))
        news_on_page = issues[current_page*5 : (current_page+1)*5]

        buttons = [[InlineKeyboardButton(text=news_item.details, callback_data=f"issues_{news_item.ticket_id}")] for news_item in news_on_page]

        if len(issues) > 5:
            buttons.append([
                InlineKeyboardButton(text="Предыдущая", callback_data="prev_ticket_page"),
                InlineKeyboardButton(text="Следующая", callback_data="next_ticket_page")
            ])

        news_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(query.from_user.id, Lang.strings["ru"]["ticket_select_reply"], reply_markup=news_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(query.from_user.id, Lang.strings["ru"]["ticket_select_error"])
