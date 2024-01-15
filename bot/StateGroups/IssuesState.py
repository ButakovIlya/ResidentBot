from aiogram.fsm.state import State, StatesGroup

class issuesState(StatesGroup):
    selected_status = State()