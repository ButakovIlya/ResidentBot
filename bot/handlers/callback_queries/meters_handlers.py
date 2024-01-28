from utils.db_requests import get_meter_by_id, get_all_meters_by_user, aprove_meter_by_id, decline_meter_by_id, is_employer
from handlers.meter_data import send_meter_data_func, get_meter_data, get_meter_data_for_employer
from handlers.localization import Lang
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from buttons.emploee_menu import emploee_menu_markup

async def change_meter_page_func(callback_query, state, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    current_page = await state.get_state() or 0
    all_meters = get_all_meters_by_user(user_id)
    pages = [all_meters[i:i + 5] for i in range(0, len(all_meters), 5)]

    if callback_query.data == "prev_meter_page" and current_page > 0:
        current_page -= 1
    elif callback_query.data == "next_meter_page" and current_page + 1 < len(pages):
        current_page += 1

    await state.set_state(current_page)

    await send_meter_data_func(state, bot, user_id)

    await bot.delete_message(user_id, message_id)


async def show_meter_by_id_func(callback_query, bot, logger):
    meter_id = int(str(callback_query.data).split('_')[1])
    from_user_id = callback_query.from_user.id
    meter = get_meter_by_id(meter_id)

    if meter:
        if is_employer(from_user_id):
            meter_buttons = []
            aprove_meter_button = InlineKeyboardButton(text=f"Одобрить ✅", callback_data=f"aprove_meter_{meter.meter_readings_id}")
            decline_meter_button = InlineKeyboardButton(text=f"Отклонить ❌", callback_data=f"decline_meter_{meter.meter_readings_id}")
            meter_buttons.append([decline_meter_button])
            meter_buttons.append([aprove_meter_button])
            keyboard_markup = InlineKeyboardMarkup(inline_keyboard=meter_buttons)

            meter_data = await get_meter_data_for_employer(meter_id, logger)
            if meter_data:
                await bot.send_message(from_user_id, meter_data, reply_markup=keyboard_markup)
            else:
                await bot.send_message(from_user_id, Lang.strings["ru"]["user_profile_error"])

        else:
            meter_data = await get_meter_data(meter_id, logger)
            if meter_data:
                await bot.send_message(from_user_id, meter_data)
            else:
                await bot.send_message(from_user_id, Lang.strings["ru"]["user_profile_error"])

        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def aprove_meter_func(callback_query, bot):
    meter_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    meter_data = get_meter_by_id(meter_id)

    if meter_data:
        if aprove_meter_by_id(meter_id):
            await bot.send_message(from_user_id, f"Показания от {meter_data.datetime} подтвержены.", reply_markup=emploee_menu_markup)
        else:
            await bot.send_message(from_user_id, f"Произошла ошибка при подтверждении показаний!", reply_markup=emploee_menu_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_profile_error"])

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def decline_meter_func(callback_query, bot):
    meter_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    meter_data = get_meter_by_id(meter_id)

    if meter_data:
        if decline_meter_by_id(meter_id):
            await bot.send_message(from_user_id, f"Показания от {meter_data.datetime} отклонены.", reply_markup=emploee_menu_markup)
        else:
            await bot.send_message(from_user_id, f"Произошла ошибка при отклонении показаний!", reply_markup=emploee_menu_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_profile_error"])

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

