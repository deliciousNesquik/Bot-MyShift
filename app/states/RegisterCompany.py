from aiogram.fsm.state import State, StatesGroup


class RegisterCompany(StatesGroup):
    company_name = State()
    company_address = State()
    company_type_of_activity = State()
    company_manager_name = State()
    company_manager_phone = State()
    company_manager_post = State()
