from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters.callback_data import CallbackData

from app.resources import keyboards, messages
from app.modules import utils
from app.modules.company_chooser import company_chooser
from app.modules.company_role import company_role
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, DialogCalendar, DialogCalendarCallback, \
    get_user_locale

from datetime import datetime

import logging

import app.database.requests as rq

router_schedule = Router()

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_schedule.message(F.text == "График")
async def handler(message: Message):
    access_check_result = await utils.check_user_access(message.from_user.id)

    if access_check_result:
        await message.answer(
            text=access_check_result[0],
            reply_markup=access_check_result[1]
        )
        return

    current_company_id = await company_chooser.get_choose(user_id=message.from_user.id)
    current_company = await rq.get_company_by_id(
        company_id=current_company_id
    )

    try:
        await message.answer(
            text="Выберите дату:",
            reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
        )
    except Exception:
        if current_company.tg_id == message.from_user.id:
            await message.answer(
                text=await messages.message_data_schedule_not_exists(
                    company_address=current_company.company_address
                ),
                reply_markup=await keyboards.set_info_shift(
                    company_id=current_company_id
                )
            )
        else:
            await message.answer(
                text=await messages.message_data_schedule_not_exists(
                    company_address=current_company.company_address
                )
            )


@router_schedule.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    access_check_result = await utils.check_user_access(callback_query.from_user.id)

    if access_check_result:
        await callback_query.message.answer(
            text=access_check_result[0],
            reply_markup=access_check_result[1]
        )
        return

    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2022, 1, 1), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        company_id = await company_chooser.get_choose(
            user_id=callback_query.from_user.id
        )
        company = await rq.get_company_by_id(
            company_id=company_id
        )
        if company_id is not None:
            shift_configuration = await rq.get_shift_config(
                company_id=company_id
            )
            try:
                _ = shift_configuration.id
            except Exception:
                if company.tg_id == callback_query.from_user.id:
                    await callback_query.message.answer(
                        text=await messages.message_data_schedule_not_exists(
                            company_address=company.company_address
                        ),
                        reply_markup=await keyboards.set_info_shift(
                            company_id=company_id
                        )
                    )
                else:
                    await callback_query.message.answer(
                        text=await messages.message_data_schedule_not_exists(
                            company_address=company_id.company_address
                        )
                    )
                return

            available_dates = await utils.get_available_dates(
                today=datetime.today().date(),
                start_date_shift=shift_configuration.start_date_shift,
                end_date_shift=shift_configuration.end_date_shift
            )

            if int(date.strftime("%d")) in available_dates:
                can_set_shift = True
                can_replacement_shift = True

                shift = await rq.get_shift(
                    date=date.strftime("%Y-%m-%d")
                )
                try:
                    _ = shift.id
                    can_set_shift = False

                    if shift.support_employee != shift.employee_id:
                        can_replacement_shift = False

                    employee = await rq.get_employee(
                        employee_id=shift.employee_id
                    )
                    support = await rq.get_employee(
                        employee_id=shift.support_employee
                    )
                    try:
                        _ = support.id
                    except AttributeError:
                        support = employee

                    await callback_query.message.answer(
                        text=await messages.message_shift_info(
                            shift_date=date.strftime("%Y-%m-%d"),
                            employee_full_name=employee.full_name,
                            main_hours=shift.hours,
                            support_hours=shift.support_hours if support.id != employee.id else "Отсутствует",
                            support_full_name=support.full_name if support.id != employee.id else "Отсутствует",
                            start_shift_time=shift.start_shift_time if shift.start_shift_time != "" else "Нет данных",
                            end_shift_time=shift.end_shift_time if shift.end_shift_time != "" else "Нет данных"
                        ),
                        reply_markup=await keyboards.keyboard_shift(
                            employee_id=employee.id,
                            support_id=support.id if employee.id != support.id else None,
                            can_set_shift=can_set_shift,
                            can_replacement_shift=can_replacement_shift,
                            date=date.strftime("%Y-%m-%d")
                        )
                    )

                except AttributeError:
                    _date = datetime((int(date.strftime("%Y-%m-%d").split('-')[0])),
                                     int((date.strftime("%Y-%m-%d")).split('-')[1]),
                                     int((date.strftime("%Y-%m-%d")).split('-')[2])).date()
                    if _date <= datetime.today().date():
                        can_set_shift = False

                    over_time = int(shift_configuration.company_chart_time.split('-')[1].split(':')[0]) - 1
                    if _date == datetime.today().date() and int(datetime.today().time().hour) <= over_time:
                        can_replacement_shift = True
                    elif _date > datetime.today().date():
                        can_replacement_shift = True
                    else:
                        can_replacement_shift = False

                    await callback_query.message.answer(
                        text=await messages.message_shift_info(
                            shift_date=date.strftime("%Y-%m-%d"),
                            employee_full_name="Отсутствует",
                            main_hours="Отсутствует",
                            support_hours="Отсутствует",
                            support_full_name="Отсутствует",
                            start_shift_time="Нет данных",
                            end_shift_time="Нет данных"
                        ),
                        reply_markup=await keyboards.keyboard_shift(
                            employee_id=None,
                            support_id=None,
                            can_set_shift=can_set_shift,
                            can_replacement_shift=can_replacement_shift,
                            date=date.strftime("%Y-%m-%d")
                        )
                    )

            else:
                can_set_shift = False
                can_replacement_shift = False

                shift = await rq.get_shift(
                    date=date.strftime("%Y-%m-%d")
                )
                try:
                    _ = shift.id
                except AttributeError:
                    await callback_query.message.answer(
                        text=messages.message_shift_not_info
                    )
                    return

                employee = await rq.get_employee(
                    employee_id=shift.employee_id
                )
                support = await rq.get_employee(
                    employee_id=shift.support_employee
                )

                await callback_query.message.answer(
                    text=await messages.message_shift_info(
                        shift_date=date.strftime("%Y-%m-%d"),
                        employee_full_name=employee.full_name,
                        main_hours=shift.hours,
                        support_hours=shift.support_hours if support.id != employee.id else "Отсутствует",
                        support_full_name=support.full_name if support.id != employee.id else "Отсутствует",
                        start_shift_time=shift.start_shift_time if shift.start_shift_time != "" else "Нет данных",
                        end_shift_time=shift.end_shift_time if shift.end_shift_time != "" else "Нет данных"
                    ),
                    reply_markup=await keyboards.keyboard_shift(
                        employee_id=employee.id,
                        support_id=support.id if employee.id != support.id else None,
                        can_set_shift=can_set_shift,
                        can_replacement_shift=can_replacement_shift,
                        date=date.strftime("%Y-%m-%d")
                    )
                )
