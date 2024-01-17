from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Оплата ЖКУ",),
            KeyboardButton(text="Связаться с УК")
        ],
        [
            KeyboardButton(text="Новости"),
            KeyboardButton(text="Профиль")
        ],
        [
            KeyboardButton(text="Проверить мои заявки"),
            KeyboardButton(text="Передача показаний")
        ]
    ]
)

