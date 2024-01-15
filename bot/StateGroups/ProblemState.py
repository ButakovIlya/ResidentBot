from aiogram.fsm.state import State, StatesGroup

class ProblemState(StatesGroup):
    problem_type = State()
    problem_description = State()
    processing_attachments = State()