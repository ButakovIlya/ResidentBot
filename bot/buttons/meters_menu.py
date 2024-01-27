from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

confirm_meters_menu_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Подтвердить",),
            KeyboardButton(text="Вернуться в главное меню")
        ],
    ]
)

