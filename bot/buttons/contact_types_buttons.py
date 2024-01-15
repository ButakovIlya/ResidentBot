from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

contact_types_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Новые заявки", callback_data="new_issues"),
    ],
    [
        InlineKeyboardButton(text="В работе", callback_data="in_progress_issues"),
    ],
    [
        InlineKeyboardButton(text="Закрытые заявки", callback_data="closed_issues")
    ],
])
