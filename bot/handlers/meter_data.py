from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from buttons.main_menu import main_menu_markup
from buttons.meters_menu import confirm_meters_menu_markup
from buttons.return_button import return_to_main_menu_markup
from StateGroups.MeterDataState import *

from utils.db_requests import get_last_meters_by_user
from utils.save_meters import save_meter_readings

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
