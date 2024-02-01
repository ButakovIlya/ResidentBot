from aiogram.fsm.context import FSMContext
from utils.db_requests import get_meter_by_id, get_all_meters_by_user, aprove_meter_by_id, decline_meter_by_id, is_employer, get_user_by_id
from handlers.meters import send_user_meters_data_func, get_meter_data, get_meter_data_for_employer, send_meters_data_func
from handlers.localization import Lang
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode
from buttons.emploee_menu import emploee_menu_markup
from buttons.meters_menu import meters_markup
from buttons.users_menu import users_markup

from handlers.utils.users import user_profile_to_employer

from utils.formatters import format_datetime

async def change_all_meters_page_func(callback_query, state:FSMContext, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    state_data = await state.get_data()

    current_page = state_data.get('meters_page', 0)
    all_meters = get_all_meters_by_user(user_id)
    pages = [all_meters[i:i + 5] for i in range(0, len(all_meters), 5)]

    if callback_query.data == "prev_meter_page" and current_page > 0:
        current_page -= 1
    elif callback_query.data == "next_meter_page" and current_page + 1 < len(pages):
        current_page += 1


    await state.set_data({
        'meters_page':current_page
    })

    await send_meters_data_func(state, bot, user_id)

    await bot.delete_message(user_id, message_id)


async def send_meter_by_user_func(callback_query, bot, logger):
    meter_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    meter = get_meter_by_id(meter_id)

    if meter:
        if is_employer(from_user_id):
            meter_buttons = []
            aprove_meter_button = InlineKeyboardButton(text=f"Одобрить ✅", callback_data=f"aprove_meter_{meter.meter_readings_id}")
            decline_meter_button = InlineKeyboardButton(text=f"Отклонить ❌", callback_data=f"decline_meter_{meter.meter_readings_id}")
            return_to_user_button = InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{meter.user_id}")
            return_to_meter_button = InlineKeyboardButton(text="Вернуться к показаниям", callback_data=f"check_user_meters_{meter.user_id}")
            
            if not meter.has_dependence: meter_buttons.append([decline_meter_button])
            if not meter.has_dependence: meter_buttons.append([aprove_meter_button]) 

            meter_buttons.append([return_to_user_button])
            meter_buttons.append([return_to_meter_button])
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


async def send_meter_by_type_func(callback_query, bot, logger):
    meters_type = str(callback_query.data).split('_')[0] or 'all'
    meter_id = int(str(callback_query.data).split('_')[1])
    from_user_id = callback_query.from_user.id
    meter = get_meter_by_id(meter_id)

    if meter:
        if is_employer(from_user_id):
            meter_buttons = []
            aprove_meter_button = InlineKeyboardButton(text=f"Одобрить ✅", callback_data=f"aprove_meter_{meter.meter_readings_id}")
            decline_meter_button = InlineKeyboardButton(text=f"Отклонить ❌", callback_data=f"decline_meter_{meter.meter_readings_id}")
            return_to_user_button = InlineKeyboardButton(text="Перейти к жителю", callback_data=f"return_to_user_{meter.user_id}")
            
            if meters_type == 'unchecked':
                return_to_meter_button = InlineKeyboardButton(text="Вернуться к показаниям", callback_data=f"return_unchecked_meters")
            elif meters_type == 'checked':
                return_to_meter_button = InlineKeyboardButton(text="Вернуться к показаниям", callback_data=f"return_checked_meters")
            else:
                return_to_meter_button = InlineKeyboardButton(text="Вернуться к показаниям", callback_data=f"return_all_meters")

            if not meter.has_dependence: meter_buttons.append([decline_meter_button])
            if not meter.has_dependence: meter_buttons.append([aprove_meter_button]) 

            meter_buttons.append([return_to_user_button])
            meter_buttons.append([return_to_meter_button])
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
    meter = get_meter_by_id(meter_id)
    to_user_id = meter.user_id

    if meter:
        meter_buttons = []
        return_to_user_button = InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{meter.user_id}")
        return_to_meter_button = InlineKeyboardButton(text="Вернуться к показаниям", callback_data=f"check_user_meters_{meter.user_id}")
        meter_buttons.append([return_to_user_button])
        meter_buttons.append([return_to_meter_button])
        if aprove_meter_by_id(meter_id, to_user_id):
            if meter.is_checked:
                new_text = '\n✅ Показания успешно подтверждены'
            else:
                new_text = '\n\n\n✅ Показания успешно подтверждены'

            old_text  = callback_query.message.text.split('\n')
            old_text = old_text[:-1]
            result_text = '\n'.join(old_text) + new_text

            meters_markup = InlineKeyboardMarkup(inline_keyboard=meter_buttons)
            await callback_query.bot.edit_message_text(result_text, callback_query.message.chat.id,
                                                       callback_query.message.message_id, reply_markup=meters_markup)
            
            await bot.send_message(to_user_id, f"👍 Ваши показания от {format_datetime(meter.datetime)} были подтвержены.", reply_markup=users_markup)
        else:
            await bot.send_message(from_user_id, f"Произошла ошибка при подтверждении показаний!", reply_markup=emploee_menu_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_profile_error"])

    # await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def decline_meter_func(callback_query, bot):
    meter_id = int(str(callback_query.data).split('_')[2])
    from_user_id = callback_query.from_user.id
    meter = get_meter_by_id(meter_id)
    to_user_id = meter.user_id

    if meter:
        meter_buttons = []
        return_to_user_button = InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{meter.user_id}")
        return_to_meter_button = InlineKeyboardButton(text="Вернуться к показаниям", callback_data=f"check_user_meters_{meter.user_id}")
        meter_buttons.append([return_to_user_button])
        meter_buttons.append([return_to_meter_button])
        if decline_meter_by_id(meter_id):
            if meter.is_checked:
                new_text = '\n❌ Показания отклонены!'
            else:
                new_text = '\n\n\n❌ Показания отклонены!'

            old_text  = callback_query.message.text.split('\n')
            old_text = old_text[:-1]
            result_text = '\n'.join(old_text) + new_text

            meters_markup = InlineKeyboardMarkup(inline_keyboard=meter_buttons)
            await callback_query.bot.edit_message_text(result_text, callback_query.message.chat.id,
                                                       callback_query.message.message_id, reply_markup=meters_markup)
            
            check_meter_btn = []
            check_meter_btn.append([InlineKeyboardButton(text="Проверить показания", callback_data=f"meter_{meter.meter_readings_id}")]) 
            check_meter_markup = InlineKeyboardMarkup(inline_keyboard=check_meter_btn)
            await bot.send_message(to_user_id, f"👎 Ваши показания от {format_datetime(meter.datetime)} были отклонены! Подайте показания корректно или свяжитесь с УК/ТСЖ",
                                    reply_markup=check_meter_markup, parse_mode=ParseMode.MARKDOWN)
        else:
            await bot.send_message(from_user_id, f"Произошла ошибка при подтверждении показаний!", reply_markup=emploee_menu_markup)
    else:
        await bot.send_message(from_user_id, Lang.strings["ru"]["user_profile_error"])

    # await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def check_user_meters_func(callback_query, state, bot):
    from_user_id = callback_query.from_user.id
    to_user_id = int(str(callback_query.data).split('_')[3])
    user = get_user_by_id(to_user_id)
    await state.update_data(to_user_id = to_user_id)
    all_meters = get_all_meters_by_user(to_user_id)

    if all_meters:
        state_data = await state.get_data()
        current_page = max(0, min(state_data.get('user_meters_page', 0), len(all_meters) // 5))
        meters_on_page = all_meters[current_page*5 : (current_page+1)*5]

        buttons = []
        for meter_item in meters_on_page:
            is_checked = '❔' if not meter_item.is_checked else '👍' if meter_item.is_approved else '👎'
            button_text = is_checked + ' ' + f"Показания от {format_datetime(meter_item.datetime)}"
            callback_data = f"user_meter_{meter_item.meter_readings_id}"
            
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
            buttons.append([button])        

        if len(all_meters) > 5:
            buttons.append([
                InlineKeyboardButton(text="Предыдущая", callback_data="prev_user_meter_page"),
                InlineKeyboardButton(text="Следующая", callback_data="next_user_meter_page"),
            ])
            buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{to_user_id}")])
        else:
            buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{to_user_id}")])

        meters_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await state.set_data({'to_user_id':to_user_id})
        await bot.send_message(from_user_id, f"Показания по счетчикам @{user.username}", reply_markup=meters_markup)
    else:
        buttons = []
        buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{to_user_id}")])
        meters_markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await bot.send_message(from_user_id, Lang.strings["ru"]["no_user_meters_to_check"], reply_markup=meters_markup)

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def change_user_meter_page_func(callback_query, state:FSMContext, bot):
    user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    state_data = await state.get_data()
    current_page = state_data.get('user_meters_page', 0)

    if 'to_user_id' in state_data:
        to_user_id = state_data['to_user_id']
    else:
        response_msg = "Ошибка, вы нажали неактуальную кнопку!"
        await bot.send_message(user_id, response_msg, reply_markup=emploee_menu_markup)
        return


    all_meters = get_all_meters_by_user(to_user_id)
    pages = [all_meters[i:i + 5] for i in range(0, len(all_meters), 5)]

    if callback_query.data == "prev_user_meter_page" and current_page > 0:
        current_page -= 1
    elif callback_query.data == "next_user_meter_page" and current_page + 1 < len(pages):
        current_page += 1

    await state.set_data({
        'user_meters_page':current_page,
    })

    state_data = await state.get_data()

    await send_user_meters_data_func(state, bot, to_user_id)

    await bot.delete_message(user_id, message_id)



async def return_to_user_func(callback_query, state:FSMContext, bot):
    from_user_id = callback_query.from_user.id
    message_id = callback_query.message.message_id

    to_user_id = int(str(callback_query.data).split('_')[3])

    await user_profile_to_employer(callback_query, bot, to_user_id)
    await state.clear()
    # await bot.delete_message(from_user_id, message_id)
