from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from buttons.main_menu import main_menu_markup
from buttons.meters_menu import confirm_meters_menu_markup
from buttons.return_button import return_to_main_menu_markup
from StateGroups.MeterDataState import *

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.enums import ParseMode
from handlers.localization import Lang

from utils.db_requests import get_last_meters_by_user, get_all_meters_by_user, get_meter_by_id, get_all_meters
from utils.db_requests import get_all_checked_meters, get_all_unchecked_meters, get_user_by_id
from utils.save_meters import save_meter_readings

from datetime import datetime
meter_router = Router()


@meter_router.message(MeterDataState.cold_water_sent)
async def hot_water_sent(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        hot_water = data.get('hot_water')
        
        if message.text == 'Вернуться в главное меню':
            await state.clear()
            await message.answer('Вы вернулись в главное меню.', reply_markup=main_menu_markup)
            return
    
        if message.text == 'Подтвердить' and data.get('hot_water_unconfirmed'):
            await state.clear()
            save_meter_readings(data.get('cold_water_confirmed'), data.get('hot_water_unconfirmed'), message.from_user.id)
            await message.answer("✅ Данные сохранены", reply_markup=main_menu_markup)
            return
        
        data_to_check = float(message.text.replace(',', '.'))  # ValueError возникнет, если введено не число
        if data_to_check <= 0:                # или data < 0
            raise ValueError
    except ValueError:
        await message.answer("Некорретные данные.\nГорячая вода. Введите показания прибота учёта в кубических метрах:")
        return


    if int(message.text) < hot_water:
        await message.answer(f"Ваши текущие показания меньше предыдущих, Вы уверены что указали все верно?\nОтправьте показания заново или нажмите кнопку 'Подтвердить'.", reply_markup=confirm_meters_menu_markup)
        await state.update_data(hot_water_unconfirmed=message.text)
        return
    else:
        save_meter_readings(data.get('cold_water_confirmed'), message.text, message.from_user.id)
        await state.clear()
        await message.answer("✅ Данные сохранены", reply_markup=main_menu_markup)
        await message.answer('Вы вернулись в главное меню.', reply_markup=main_menu_markup)
        return


@meter_router.message(MeterDataState.started)
async def cold_water_sent(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        hot_water = data.get('hot_water')
        cold_water = data.get('cold_water')

        if message.text == 'Вернуться в главное меню':
            await state.clear()
            await message.answer('Вы вернулись в главное меню.', reply_markup=main_menu_markup)
            return
        
        if message.text == 'Подтвердить' and data.get('cold_water_unconfirmed'):
            await state.set_state(MeterDataState.cold_water_sent)
            await state.update_data(cold_water_confirmed=data.get('cold_water_unconfirmed'))
            await message.answer(f"Ваши последние показания по горячей воде: {hot_water}м³")
            await message.answer("Горячая вода. Введите текущие показания прибота учёта в кубических метрах:")
            return
        
        data = float(message.text.replace(',', '.'))
        if data <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Некорретные данные.\nХолодная вода. Введите показания прибота учёта в кубических метрах:")
        return


    if int(message.text) < cold_water:
        await message.answer(f"Ваши текущие показания меньше предыдущих, Вы уверены что указали все верно?\nОтправьте показания заново или нажмите кнопку 'Подтвердить'.", reply_markup=confirm_meters_menu_markup)
        await state.update_data(cold_water_unconfirmed=message.text)
        return
    else:
        await state.set_state(MeterDataState.cold_water_sent)
        await state.update_data(cold_water_confirmed=message.text)
        await message.answer(f"Ваши последние показания по горячей воде: {hot_water}м³")
        await message.answer("Горячая вода. Введите текущие показания прибота учёта в кубических метрах:")



@meter_router.message(lambda message: message.text == "Передача показаний")
async def send_meter_data(message: types.Message, state: FSMContext):
    await state.set_state(MeterDataState.started)
    user_id = message.from_user.id
    last_meters = get_last_meters_by_user(user_id)

    await state.update_data(hot_water=last_meters.hot_water)
    await state.update_data(cold_water=last_meters.cold_water)

    await message.answer(f"Ваши последние показания по холодной воде: {last_meters.cold_water}м³")
    await message.answer("Холодная вода. Введите текущие показания прибота учёта в кубических метрах:", reply_markup=return_to_main_menu_markup)





async def send_meter_data_func(state: FSMContext, bot, user_id):
    all_meters = get_all_meters_by_user(user_id)
    user = get_user_by_id(user_id)
    if all_meters:
        current_page = max(0, min(await state.get_state() or 0, len(all_meters) // 5))
        meters_on_page = all_meters[current_page*5 : (current_page+1)*5]

        buttons = [[types.InlineKeyboardButton(text="Показания от " + str(meter_item.datetime), callback_data=f"meter_{meter_item.meter_readings_id}")] for meter_item in meters_on_page]

        if len(all_meters) > 5:
            buttons.append([
                InlineKeyboardButton(text="Предыдущая", callback_data="prev_user_meter_page"),
                InlineKeyboardButton(text="Следующая", callback_data="next_user_meter_page"),
            ])
            buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{user_id}")])
        else:
            buttons.append([InlineKeyboardButton(text="Вернуться к жителю", callback_data=f"return_to_user_{user_id}")])

        meters_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await state.set_data({'to_user_id':user_id})
        await bot.send_message(user_id, f"Показания по счетчикам @{user.username}", reply_markup=meters_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["ticket_select_error"])


async def send_meter_data_to_employer_func(state: FSMContext, bot, user_id, is_checked=None):
    if is_checked == True:
        all_meters = get_all_checked_meters()
    elif is_checked == False:
        all_meters = get_all_unchecked_meters()
    else: 
        all_meters = get_all_meters()


    if all_meters:
        current_page = max(0, min(await state.get_state() or 0, len(all_meters) // 5))
        meters_on_page = all_meters[current_page*5 : (current_page+1)*5]

        buttons = [[types.InlineKeyboardButton(text="Показания от " + str(meter_item.datetime), callback_data=f"meter_{meter_item.meter_readings_id}")] for meter_item in meters_on_page]

        if len(all_meters) > 5:
            buttons.append([
                types.InlineKeyboardButton(text="Предыдущая", callback_data="prev_meter_page"),
                types.InlineKeyboardButton(text="Следующая", callback_data="next_meter_page")
            ])

        news_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)

        await bot.send_message(user_id, Lang.strings["ru"]["meter_select_reply"], reply_markup=news_markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await bot.send_message(user_id, Lang.strings["ru"]["meter_no_meters"])


async def get_meter_data(meter_id, logger):
    try:
        meter = get_meter_by_id(meter_id)
        if meter:
            meter_data = (
                f"Инофрмация о показаниях:\n"
                f"Номер: {meter.meter_readings_id}\n"
                f"Холодная вода: {meter.cold_water}\n"
                f"Горячая вода: {meter.hot_water}\n"
                f"Дата: {(str(meter.datetime).split()[0])}\n"
                f"Время: {str(meter.datetime).split()[1]}\n"
                f"Просмотрена: {'Да' if meter.is_checked else 'Нет'}\n"
            )
            if meter.is_checked:
                meter_data += f"Одобрена: {'Да' if meter.is_approved else 'Нет'}"

            return meter_data
        else:   
            return None
    except Exception as e:
        logger.error(f"Ошибка при получении показаний: {str(e)}")



async def get_meter_data_for_employer(meter_id, logger):
    try:
        meter = get_meter_by_id(meter_id)
        if meter:
            meter_data = (
                f"Инофрмация о жителе:\n"
                f"ФИО жителя: {meter.last_name + ' ' + meter.first_name + ' ' + meter.patronymic}\n"
                f"Адрес: {meter.address}\n"
                f"Квартира: {meter.apartment}\n"
                f"Контакт: @{meter.username}\n"
                f"Связаться: {meter.tg_link}\n\n"

                f"Инофрмация о показаниях:\n"
                f"Номер: {meter.meter_readings_id}\n"
                f"Холодная вода: {meter.cold_water}\n"
                f"Горячая вода: {meter.hot_water}\n"
                f"Дата: {(str(meter.datetime).split()[0])}\n"
                f"Время: {str(meter.datetime).split()[1]}\n"

            )
            if meter.is_checked:
                meter_data += f"\n\n{'✅ Показания подтверждены.' if meter.is_approved else '❌ Показания отклонены!'}"

            return meter_data
        else:   
            return None
    except Exception as e:
        logger.error(f"Ошибка при получении показаний: {str(e)}")