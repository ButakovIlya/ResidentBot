from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
emploee_menu_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Меню жителей"),
            KeyboardButton(text="Аккаунт"),
        ],
        [
            KeyboardButton(text="Меню новостей"),
            KeyboardButton(text="Меню опросов")
        ]
    ]
)

