from aiogram.fsm.state import State, StatesGroup


class RegisterEmployee(StatesGroup):
    id = State()
    full_name = State()
    age = State()
    phone = State()
    bank = State()
