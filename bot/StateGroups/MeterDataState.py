from aiogram.fsm.state import State, StatesGroup


class MeterDataState(StatesGroup):
    started = State()
    cold_water_sent = State()

    cold_water_warning = State()
    hot_water_warning = State()
