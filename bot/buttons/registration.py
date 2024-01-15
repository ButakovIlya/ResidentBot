from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from dict.role_dict import empl_roles

# Выбор роли
select_role_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Житель", callback_data="resident"),
        InlineKeyboardButton(text="Сотрудник УК", callback_data="uk_staff"),
    ]
])

# Отправка номера телефона
share_phone_number_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Поделиться номером 📞", request_contact=True)
        ]
    ]
)


# Верификация жителей
async def get_verif_markup(unconfirmed_user_tg_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"verif-approve-{unconfirmed_user_tg_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"verif-reject-{unconfirmed_user_tg_id}"),
        ]
    ])

# Верификация сотрудников
async def get_empl_verif_markup(unconfirmed_empl_tg_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"empl-verif-approve-{unconfirmed_empl_tg_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"empl-verif-reject-{unconfirmed_empl_tg_id}"),
        ]
    ])


# Выбор должности (для сотрудников УК)
empl_roles_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=role_name, callback_data=role_name) for role_name in empl_roles]
])
