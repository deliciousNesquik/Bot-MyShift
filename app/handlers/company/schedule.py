from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from app.resources import keyboards, messages
from app.modules.company_chooser import company_chooser
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
    get_user_locale

from datetime import datetime

import app.database.requests as rq

router_schedule = Router()


@router_schedule.message(F.text == "График")
async def handler(message: Message):
    current_company_id = await company_chooser.get_choose(
        user_id=message.from_user.id
    )
    if not current_company_id:
        await message.answer(
            text=messages.message_company_not_selected
        )
        return

    current_company = await rq.get_company_by_id(
        company_id=current_company_id
    )

    company_session_configuration = await rq.get_session_config(
        company_id=current_company_id
    )

    try:
        await message.answer(
            text=await messages.message_schedule_data(
                company_address=current_company.company_address,
                company_chart=company_session_configuration.company_chart,
                company_chart_time=company_session_configuration.company_chart_time,
                number_of_hours_per_shift=company_session_configuration.number_of_hours_per_shift,
                payment_per_hour=company_session_configuration.payment_per_hour,
                payment_for_over_fulfillment=company_session_configuration.payment_for_over_fulfillment,
                premium=company_session_configuration.premium,
                start_date_shift=company_session_configuration.start_date_shift,
                end_date_shift=company_session_configuration.end_date_shift
            )
        )
        await message.answer(
            text="Выберите дату:",
            reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
        )
    except Exception:
        await message.answer(
            text=await messages.message_data_schedule_not_exists(
                company_address=current_company.company_address
            ),
            reply_markup=await keyboards.set_info_shift(
                company_id=current_company_id
            )
        )


@router_schedule.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'Ты выбрал {date.strftime("%d/%m/%Y")}'
        )
