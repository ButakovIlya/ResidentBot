from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

return_to_main_menu_button = KeyboardButton(text="Вернуться в главное меню")

return_to_main_menu_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[return_to_main_menu_button]]
)
