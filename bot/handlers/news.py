from aiogram import types
from aiogram.enums import ParseMode
from handlers.localization import Lang
from utils.db_requests import get_all_news, get_employer_by_id


async def get_news_for_user(user_id, bot, state):
    all_news = get_all_news()
    is_employer = get_employer_by_id(user_id)
    if all_news:
        current_page = max(0, min(await state.get_state() or 0, len(all_news) // 5))
        news_on_page = all_news[current_page*5 : (current_page+1)*5]

        if not is_employer:
            buttons = [[types.InlineKeyboardButton(text=news_item.topic, callback_data=f"news_{news_item.news_id}")] for news_item in news_on_page]
        else: 
            buttons = [[types.InlineKeyboardButton(text=news_item.topic, callback_data=f"edit_news_{news_item.news_id}")] for news_item in news_on_page]

        if len(all_news) > 5:
            buttons.append([
                types.InlineKeyboardButton(text="Предыдущая", callback_data="prev_page"),
                types.InlineKeyboardButton(text="Следующая", callback_data="next_page")
            ])

        news_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(user_id, Lang.strings["ru"]["news_select_reply"], reply_markup=news_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["news_select_error"])
