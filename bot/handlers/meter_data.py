from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from buttons.main_menu import main_menu_markup
from buttons.return_button import return_to_main_menu_markup
from StateGroups.MeterDataState import *

meter_router = Router()


@meter_router.message(MeterDataState.cold_water_sent)
async def hot_water_sent(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Вернуться в главное меню':
            await state.clear()
            await message.answer('Вы вернулись в главное меню.', reply_markup=main_menu_markup)
            return
        
        data = float(message.text.replace(',', '.'))  # ValueError возникнет, если введено не число
        if data <= 0:                # или data < 0
            raise ValueError
    except ValueError:
        await message.answer("Некорретные данные.\nГорячая вода. Введите показания прибота учёта в кубических метрах:")
        return

    # todo сохранять показания горячей воды
    await state.clear()
    await message.answer("✅ Данные сохранены", reply_markup=main_menu_markup)


@meter_router.message(MeterDataState.started)
async def cold_water_sent(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Вернуться в главное меню':
            await state.clear()
            await message.answer('Вы вернулись в главное меню.', reply_markup=main_menu_markup)
            return
        
        data = float(message.text.replace(',', '.'))
        if data <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Некорретные данные.\nХолодная вода. Введите показания прибота учёта в кубических метрах:")
        return

    # todo сохранять показания холодной воды
    await state.set_state(MeterDataState.cold_water_sent)
    await message.answer("Горячая вода. Введите показания прибота учёта в кубических метрах:")


@meter_router.message(lambda message: message.text == "Передача показаний")
async def send_meter_data(message: types.Message, state: FSMContext):
    await state.set_state(MeterDataState.started)
    await message.answer("Холодная вода. Введите показания прибота учёта в кубических метрах:", reply_markup=return_to_main_menu_markup)
