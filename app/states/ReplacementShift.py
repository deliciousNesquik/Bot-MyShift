from aiogram.fsm.state import State, StatesGroup


class ReplacementShift(StatesGroup):
    time_range = State()
    shift_date = State()
