from aiogram.fsm.state import State, StatesGroup


class ChooseCompany(StatesGroup):
    company_id = State()
