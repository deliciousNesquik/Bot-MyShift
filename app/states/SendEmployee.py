from aiogram.fsm.state import State, StatesGroup


class SendEmployee(StatesGroup):
    company_id = State()
    employee_tg = State()
    message_one = State()
    message_all = State()
