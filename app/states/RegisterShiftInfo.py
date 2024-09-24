from aiogram.fsm.state import State, StatesGroup


class RegisterShiftInfo(StatesGroup):
    company_id = State()
    company_chart = State()
    company_chart_time = State()
    start_date_shift = State()
    end_date_shift = State()
    payment_per_hour = State()
    payment_for_over_fulfillment = State()
    premium = State()
