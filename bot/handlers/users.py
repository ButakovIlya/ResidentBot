from aiogram import types
from aiogram.enums import ParseMode
from handlers.localization import Lang
from buttons.emploee_menu import emploee_menu_markup
from utils.db_requests import get_all_users


async def send_all_users_by_complex_id(employer_id, bot, state):
    all_users = get_all_users()
    if all_users:
        current_page = max(0, min(await state.get_state() or 0, len(all_users) // 5))
        users_on_page = all_users[current_page*5 : (current_page+1)*5]

        buttons = [[types.InlineKeyboardButton(text=users_item.first_name + ' ' + users_item.last_name,
                                               callback_data=f"profile_user_{users_item.telegram_id}")] for users_item in users_on_page]
     
        if len(all_users) > 5:
            buttons.append([
                types.InlineKeyboardButton(text="Предыдущая", callback_data="user_prev_page"),
                types.InlineKeyboardButton(text="Следующая", callback_data="user_next_page")
            ])

        users_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(employer_id, Lang.strings["ru"]["user_select_reply"], reply_markup=users_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(employer_id, Lang.strings["ru"]["user_select_error"])
