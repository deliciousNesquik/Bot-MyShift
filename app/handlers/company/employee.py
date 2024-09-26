import aiogram.exceptions
import sqlalchemy.exc
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router, Bot

from app.resources import keyboards, messages
from app.states.SendEmployee import SendEmployee
from app.modules.company_chooser import company_chooser
from datetime import datetime

import app.database.requests as rq

router_manage_employee = Router()


@router_manage_employee.message(F.text == "Сотрудники")
async def menu_employee(message: Message):
    current_company_id = await company_chooser.get_choose(user_id=message.from_user.id)

    company = await rq.get_company_by_id(
        company_id=current_company_id
    )
    if not current_company_id:
        await message.answer(
            text=messages.message_company_not_selected
        )
        return

    await message.answer(
        text=await messages.message_employee_data(
            company_address=company.company_address,
            count_employee=rq.count_employee,
            current_company_id=current_company_id
        ),
        reply_markup=await keyboards.get_manage_company_employee(
            company_id=current_company_id
        )
    )


@router_manage_employee.callback_query(F.data.startswith("invite-employee_"))
async def handler(call: CallbackQuery):
    await call.message.answer(
        text=await messages.message_referral_link(
            company_id=call.data.split("_")[1]
        )
    )


@router_manage_employee.callback_query(F.data.startswith("payout-employee_"))
async def handler(call: CallbackQuery):
    employee_id = call.data.split("_")[1]
    pay_sum = call.data.split("_")[2]

    employee = await rq.get_employee(
        employee_id=employee_id
    )

    await rq.create_payout(
        employee_id=employee_id,
        company_id=employee.company_id,
        pay_sum=pay_sum
    )

    await call.message.answer(
        text=await messages.message_payout_check(
            pay_sum=pay_sum,
            employee_id=employee_id
        )
    )


@router_manage_employee.callback_query(F.data.startswith("payment-employee_"))
async def handler(call: CallbackQuery):
    employee_id = call.data.split("_")[1]

    employee = await rq.get_employee(
        employee_id=employee_id
    )

    payouts = await rq.get_payouts(
        employee_id=employee_id
    )

    all_payout_date = []
    for pay in payouts:
        all_payout_date.append(pay.date)

    if len(all_payout_date) != 0:
        if all_payout_date[-1] == datetime.today().date():
            await call.message.answer(
                text=messages.message_payout_today_exists
            )
        else:
            hours = await rq.hours_period(
                start_date=all_payout_date[-1],
                end_date=datetime.today().date(),
                employee_id=employee_id
            )

            if hours == 0:
                await call.message.answer(
                    text=messages.message_payout_null_hourse
                )
            else:
                pay_sum = await rq.salary_calculation(
                    company_id=employee.company_id,
                    count_hours=hours
                )
                await call.message.answer(
                    text=await messages.message_payout_was_success(
                        pay_sum=pay_sum
                    ),
                    reply_markup=await keyboards.keyboard_payout(
                        employee_id=employee_id,
                        paysum=pay_sum
                    )
                )
    else:
        #await call.message.answer(f"Выплат еще не было, дата начала работы: {employee.start_date_work}")

        hours = await rq.hours_period(
            start_date=employee.start_date_work,
            end_date=datetime.today().date(),
            employee_id=employee_id
        )

        if hours == 0:
            await call.message.answer(
                text=messages.message_payout_null_hourse
            )
        else:
            pay_sum = await rq.salary_calculation(
                company_id=employee.company_id,
                count_hours=hours
            )
            await call.message.answer(
                text=await messages.message_payout_was_success(
                    pay_sum=pay_sum
                ),
                reply_markup=await keyboards.keyboard_payout(
                    employee_id=employee_id,
                    paysum=pay_sum
                )
            )


@router_manage_employee.callback_query(F.data.startswith("send-all-employee_"))
async def handler(call: CallbackQuery, state: FSMContext):
    company_id = call.data.split("_")[1]

    await state.set_state(SendEmployee.company_id)
    await state.update_data(company_id=company_id)
    await state.set_state(SendEmployee.message_all)

    await call.message.answer(
        text=messages.message_send_enter_text
    )


@router_manage_employee.message(SendEmployee.message_all)
async def handler(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(message_all=message.text)

    data = await state.get_data()

    all_employee = await rq.get_all_employee(
        company_id=await company_chooser.get_choose(user_id=message.from_user.id)
    )

    for employee in all_employee:
        try:
            await bot.send_message(
                chat_id=employee.telegram_id,
                text=await messages.message_send_employee(
                    text=str(data['message_all'])
                )
            )
        except aiogram.exceptions.TelegramBadRequest:
            pass

    await message.answer(
        text=messages.message_send_was_success
    )

    await state.clear()


@router_manage_employee.callback_query(F.data.startswith("delete-employee_"))
async def handler(call: CallbackQuery, bot: Bot):
    employee_id = call.data.split("_")[1]

    try:
        employee = await rq.get_employee(
            employee_id=employee_id
        )

        employee_tg_id = employee.telegram_id

        await rq.delete_employee(
            employee_id=employee_id,
            company_id=employee.company_id
        )

        await call.message.answer(
            text=messages.message_employee_was_delete_success
        )

        try:
            await bot.send_message(
                chat_id=employee_tg_id,
                text=messages.message_send_employee_delete_from_company
            )
        except aiogram.exceptions.TelegramBadRequest:
            pass

    except sqlalchemy.exc.OperationalError:
        await call.message.answer(
            text=messages.message_employee_was_delete_error
        )


@router_manage_employee.callback_query(F.data.startswith("delete-all-employee_"))
async def handler(call: CallbackQuery, bot: Bot):
    company_id = call.data.split("_")[1]

    all_employee = await rq.get_all_employee(
        company_id=company_id
    )

    for employee in all_employee:
        try:
            employee_tg_id = employee.telegram_id

            await rq.delete_employee(
                employee_id=employee.id,
                company_id=company_id
            )

            try:
                await bot.send_message(
                    chat_id=employee_tg_id,
                    text=messages.message_send_employee_delete_from_company
                )
            except aiogram.exceptions.TelegramBadRequest:
                pass

        except sqlalchemy.exc.OperationalError:
            await call.message.answer(
                text=messages.message_all_employee_was_delete_error
            )
            return

        await call.message.answer(
            text=messages.message_all_employee_was_delete_success
        )


@router_manage_employee.callback_query(F.data.startswith("send-employee_"))
async def handler(call: CallbackQuery, state: FSMContext):
    current_employee_id = call.data.split("_")[1]

    current_employee = await rq.get_employee(
        employee_id=current_employee_id
    )

    current_employee_tg_id = current_employee.telegram_id

    await state.set_state(SendEmployee.employee_tg)
    await state.update_data(employee_tg=current_employee_tg_id)
    await state.set_state(SendEmployee.message_one)

    await call.message.answer(
        text=messages.message_send_enter_text
    )


@router_manage_employee.message(SendEmployee.message_one)
async def handler(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(message_one=message.text)
    try:
        data = await state.get_data()

        await bot.send_message(
            chat_id=data['employee_tg'],
            text=await messages.message_send_employee(
                text=str(data['message_one'])
            )
        )

        await message.answer(
            text=messages.message_send_was_success
        )
    except aiogram.exceptions.TelegramBadRequest:
        await message.answer(
            text=messages.message_send_was_error
        )

    await state.clear()


@router_manage_employee.callback_query(F.data.startswith("employee_"))
async def handler(call: CallbackQuery):
    current_employee_id = call.data.split("_")[1]

    current_employee = await rq.get_employee(
        employee_id=current_employee_id
    )

    current_company = await rq.get_company_by_id(
        company_id=current_employee.company_id
    )

    await call.message.answer(
        text=await messages.message_short_info_employee(
            employee_id=current_employee_id,
            company_address=current_company.company_address,
            start_date_work=current_employee.start_date_work,
            full_name=current_employee.full_name,
            age=current_employee.age,
            phone=current_employee.phone,
            bank=current_employee.bank
        ),
        reply_markup=await keyboards.keyboard_manage_employee(
            employee_id=current_employee_id
        )
    )
