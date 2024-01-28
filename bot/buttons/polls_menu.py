from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


polls_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Создать опрос"),
        ],
        [
            KeyboardButton(text="Активные опросы"),
            KeyboardButton(text="Завершенные опросы")
        ],
        [
            KeyboardButton(text="Вернуться в меню сотрудника"),
        ]
    ]
)

return_to_polls_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Вернуться в меню опросов"),
        ]
    ]
)

