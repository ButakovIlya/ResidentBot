from aiogram import types
from aiogram.enums import ParseMode
from handlers.localization import Lang
from utils.db_requests import get_all_by_user_id_and_status


async def check_tikects_handler(user_id, bot, state):
 
    all_tickets = get_all_by_user_id_and_status(user_id, 0)

    if all_tickets:
        current_page = max(0, min(await state.get_state() or 0, len(all_tickets) // 5))
        tickets_on_page = all_tickets[current_page*5 : (current_page+1)*5]

        buttons = [[types.InlineKeyboardButton(text=ticket_item.details, callback_data=f"ticket_{ticket_item.ticket_id}")] for ticket_item in tickets_on_page]

        if len(all_tickets) > 5:
            buttons.append([
                types.InlineKeyboardButton(text="Предыдущая", callback_data="prev_ticket_page"),
                types.InlineKeyboardButton(text="Следующая", callback_data="next_ticket_page")
            ])

        news_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(user_id, Lang.strings["ru"]["ticket_select_reply"], reply_markup=news_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["ticket_select_error"])
