from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
emploee_menu_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Заявки жителей"),
            KeyboardButton(text="Новости")
        ],
        [
            KeyboardButton(text="Создать новость"),
            KeyboardButton(text="Создать опрос")
        ],
        [
            KeyboardButton(text="Активные опросы"),
            KeyboardButton(text="Завершенные опросы"),
        ]
    ]
)

