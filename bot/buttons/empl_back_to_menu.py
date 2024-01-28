from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

return_back_button = KeyboardButton(text="Вернуться в меню новостей")

return_back_button_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[return_back_button]]
)
