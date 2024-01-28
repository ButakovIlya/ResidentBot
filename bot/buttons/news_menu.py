from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


news_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Новости"),
            KeyboardButton(text="Создать новость"),
        ],
        [
            KeyboardButton(text="Вернуться в меню сотрудника")
        ],
    ]
)

