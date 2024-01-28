from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tickets_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
            [
                KeyboardButton(text="Все заявки"),
                KeyboardButton(text="Закрытые заявки"),
                KeyboardButton(text="Открытые заявки"),
            ],
            [
                KeyboardButton(text="Вернуться в меню жителей"),
            ],
        ]
    )   
