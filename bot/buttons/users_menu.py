from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


users_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Мои жители"),
        ],
        [
            KeyboardButton(text="Заявки жителей"),
            KeyboardButton(text="Показания жителей")
        ],
        [
            KeyboardButton(text="Вернуться в меню сотрудника"),
        ]
    ]
)

