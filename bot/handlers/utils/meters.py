    
# from aiogram import types
# from aiogram.fsm.context import FSMContext

# from StateGroups.MeterDataState import *

# from handlers.localization import Lang

# from utils.db_requests import  get_all_meters_by_user


# async def get_all_meters_by_user_markup(state: FSMContext, user_id):
#     all_meters = get_all_meters_by_user(user_id)
#     if all_meters:
#         current_page = max(0, min(await state.get_state() or 0, len(all_meters) // 5))
#         meters_on_page = all_meters[current_page*5 : (current_page+1)*5]

#         buttons = [[types.InlineKeyboardButton(text="Показания от " + str(meter_item.datetime), callback_data=f"meter_{meter_item.meter_readings_id}")] for meter_item in meters_on_page]

#         if len(all_meters) > 5:
#             buttons.append([
#                 types.InlineKeyboardButton(text="Предыдущая", callback_data="prev_meter_page"),
#                 types.InlineKeyboardButton(text="Следующая", callback_data="next_meter_page")
#             ])

#         meters_markup = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#         return meters_markup
#     else:
#         return Lang.strings["ru"]["ticket_select_error"]