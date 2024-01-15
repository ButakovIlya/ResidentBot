from aiogram.fsm.state import State, StatesGroup


class RegistrationEmplState(StatesGroup):
    is_employee = State()
    role = State()
    full_name = State()
    phone_number = State()
    email = State()
