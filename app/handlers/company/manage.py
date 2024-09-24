from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.ChoiseCompany import ChooseCompany
from app.resources import keyboards, messages

import app.database.requests as rq

router_manage_company = Router()


@router_manage_company.callback_query(F.data.startswith("company-view_"))
async def handler(call: CallbackQuery, state: FSMContext):
    current_company_id = call.data.split("_")[1]

    await state.update_data(
        company_id=current_company_id
    )

    company = await rq.get_company_by_id(
        company_id=current_company_id
    )

    await call.message.answer(
        text=await messages.message_short_info_company(
            company_id=company.id,
            company_name=company.company_name,
            company_address=company.company_address,
            company_type_of_activity=company.company_type_of_activity
        ),
        reply_markup=keyboards.keyboard_back_to_manage_company
    )

    await call.message.answer(
        text=messages.message_use_keyboard,
        reply_markup=keyboards.keyboard_manage_company
    )


@router_manage_company.message(F.text == "График")
async def handler(message: Message, state: FSMContext):
    data = await state.get_data()

    try:
        current_company_id = data['company_id']
    except KeyError:
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
    except Exception:
        await message.answer(
            text=await messages.message_data_schedule_not_exists(
                company_address=current_company.company_address
            ),
            reply_markup=await keyboards.set_info_shift(
                company_id=current_company_id
            )
        )


@router_manage_company.message(F.text == "Профиль компании")
async def handler(message: Message, state: FSMContext):
    data = await state.get_data()

    try:
        current_company_id = data['company_id']

        current_company = await rq.get_company_by_id(
            company_id=current_company_id
        )

    except Exception:
        await message.answer(
            text=messages.message_company_not_selected
        )
        return

    await message.answer(f"Профиль для компании с адресом {current_company.company_address}\n\n")


@router_manage_company.message(F.text == "Настройки компании")
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

    await message.answer(f"Настройки для компании с адресом {company.company_address}\n\n")



