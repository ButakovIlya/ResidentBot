from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_pay_invoice_keyboard(user_id):
    pay_button_markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Оплатить квитанцию", callback_data=f"pay_invoice_{user_id}")
        ]
    ])
    return pay_button_markup
