from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    role = State()
    full_name = State()
    phone_number = State()
    email = State()
    address = State()
    apartment = State()
    residential_complex = State()
