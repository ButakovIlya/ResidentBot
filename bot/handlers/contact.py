from buttons.contact_problems import contact_problems_markup
from buttons.return_button import return_to_main_menu_markup
from handlers.localization import Lang, get_localized_message
from aiogram import types


async def contact_uk_handler(user_id, bot):
    await bot.send_message(user_id, Lang.strings["ru"]["contact_select_type"],
                           reply_markup=contact_problems_markup)


async def problem_about_handler(user_id, bot, problem):
    message_text = get_localized_message("ru", "choose_problem_type", problem=problem)
    await bot.send_message(user_id, message_text, reply_markup=return_to_main_menu_markup)


async def extract_problem_description(message: types.Message):
    if message.photo or message.document:
        return message.caption
    return message.text