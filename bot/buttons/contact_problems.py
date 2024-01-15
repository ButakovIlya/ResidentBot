from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

contact_problems_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Технические проблемы", callback_data="tech_problems"),
    ],
    [
        InlineKeyboardButton(text="Санитарные проблемы", callback_data="sanitary_problems"),
    ],
    [ 
        InlineKeyboardButton(text="Безопасность и охрана", callback_data="security_problems"),
    ],
    [
        InlineKeyboardButton(text="Другое", callback_data="other_problems"),
    ]
])
