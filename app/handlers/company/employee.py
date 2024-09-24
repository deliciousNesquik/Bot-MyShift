from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from app.resources import keyboards, messages
import app.database.requests as rq

router_manage_employee = Router()


@router_manage_employee.message(F.text == "Сотрудники")
async def handler(message: Message, state: FSMContext):
    data = await state.get_data()

    try:
        current_company_id = data['company_id']

        company = await rq.get_company_by_id(
            company_id=current_company_id
        )

    except Exception:
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
        reply_markup=keyboards.keyboard_back_to_employee
    )
