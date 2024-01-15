from aiogram.fsm.state import State, StatesGroup

class NewsPage(StatesGroup):
    page = State()

class NewsStates(StatesGroup):
    InputMessage = State()
    InputTopic = State()
    SendToUsers = State()