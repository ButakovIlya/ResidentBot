from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


meters_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Непроверенные показания",),
            KeyboardButton(text="Проверенные показания")
        ],
        [
            KeyboardButton(text="Все показания",),
            KeyboardButton(text="Вернуться в меню жителей")
        ],
    ]
)




confirm_meters_menu_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Подтвердить",),
            KeyboardButton(text="Вернуться в главное меню")
        ],
    ]
)

