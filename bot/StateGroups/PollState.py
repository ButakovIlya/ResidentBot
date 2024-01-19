from aiogram.fsm.state import State, StatesGroup

class PollState(StatesGroup):
    WaitingForPoll = State()