from aiogram.fsm.state import State, StatesGroup


class MeterDataState(StatesGroup):
    started = State()
    cold_water_sent = State()
