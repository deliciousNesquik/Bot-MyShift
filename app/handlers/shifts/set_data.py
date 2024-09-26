import sqlalchemy.exc
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.RegisterShiftInfo import RegisterShiftInfo
from app.resources import messages

import app.database.requests as rq

router_shift_info = Router()


@router_shift_info.callback_query(F.data.startswith("set-info-shift_"))
async def handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(
        company_id=call.data.split("_")[1]
    )

    await state.set_state(
        RegisterShiftInfo.company_chart
    )

    await call.message.answer(
        text=messages.message_enter_schedule
    )


@router_shift_info.message(RegisterShiftInfo.company_chart)
async def handler(message: Message, state: FSMContext):
    if message.text.lower() in ("ежедневно", "5/2", "6/1"):
        await state.update_data(
            company_chart=message.text
        )

        await state.set_state(
            RegisterShiftInfo.start_date_shift
        )

        await message.answer(
            text=messages.message_enter_startday
        )
    else:
        await state.set_state(
            RegisterShiftInfo.company_chart
        )

        await message.answer(
            text=messages.message_enter_schedule
        )


@router_shift_info.message(RegisterShiftInfo.start_date_shift)
async def handler(message: Message, state: FSMContext):
    try:
        int(message.text)

        await state.update_data(
            start_date_shift=message.text
        )

        await state.set_state(
            RegisterShiftInfo.end_date_shift
        )

        await message.answer(
            text=messages.message_enter_endday
        )
    except Exception:
        await state.set_state(
            RegisterShiftInfo.start_date_shift
        )

        await message.answer(
            text=messages.message_enter_startday
        )


@router_shift_info.message(RegisterShiftInfo.end_date_shift)
async def handler(message: Message, state: FSMContext):
    try:
        int(message.text)

        await state.update_data(
            end_date_shift=message.text
        )

        await state.set_state(
            RegisterShiftInfo.company_chart_time
        )

        await message.answer(
            text=messages.message_enter_charttime
        )

    except Exception:
        await state.set_state(
            RegisterShiftInfo.end_date_shift
        )

        await message.answer(
            text=messages.message_enter_endday
        )


@router_shift_info.message(RegisterShiftInfo.company_chart_time)
async def handler(message: Message, state: FSMContext):
    if len(message.text) == 11:
        await state.update_data(
            company_chart_time=message.text
        )

        await state.set_state(
            RegisterShiftInfo.payment_per_hour
        )

        await message.answer(
            text=messages.message_enter_payrephouse
        )
    else:
        await state.set_state(
            RegisterShiftInfo.company_chart_time
        )

        await message.answer(
            text=messages.message_enter_charttime
        )


@router_shift_info.message(RegisterShiftInfo.payment_per_hour)
async def handler(message: Message, state: FSMContext):
    try:
        int(message.text)

        await state.update_data(
            payment_per_hour=message.text
        )

        await state.set_state(
            RegisterShiftInfo.payment_for_over_fulfillment
        )

        await message.answer(
            text=messages.message_enter_paymentforoverfulfillment
        )
    except Exception:
        await state.set_state(
            RegisterShiftInfo.payment_per_hour
        )

        await message.answer(
            text=messages.message_enter_payrephouse
        )


@router_shift_info.message(RegisterShiftInfo.payment_for_over_fulfillment)
async def handler(message: Message, state: FSMContext):
    if message.text.lower() in ("да", "нет"):
        await state.update_data(
            payment_for_over_fulfillment=message.text
        )

        await state.set_state(
            RegisterShiftInfo.premium
        )

        await message.answer(
            text=messages.message_enter_premium
        )
    else:
        await state.set_state(
            RegisterShiftInfo.payment_for_over_fulfillment
        )

        await message.answer(
            text=messages.message_enter_paymentforoverfulfillment
        )


@router_shift_info.message(RegisterShiftInfo.premium)
async def handler(message: Message, state: FSMContext):
    if message.text.lower() in ("да", "нет"):
        await state.update_data(
            premium=message.text
        )

        data = await state.get_data()

        await state.clear()

        try:
            await rq.set_shift_config(
                company_id=data['company_id'],
                company_chart=data['company_chart'],
                company_chart_time=data['company_chart_time'],
                start_date_shift=data['start_date_shift'],
                end_date_shift=data['end_date_shift'],
                number_of_hours_per_shift=float(
                    float(str(data['company_chart_time']).split('-')[1].split(':')[0]) - float(
                        str(data['company_chart_time']).split('-')[0].split(':')[0])),
                payment_per_hour=data['payment_per_hour'],
                payment_for_over_fulfillment=True if str(
                    data['payment_for_over_fulfillment']).lower() == "да" else False,
                premium=True if str(data['premium']).lower() == "да" else False
            )

            await message.answer(
                text=messages.message_data_was_update
            )
        except sqlalchemy.exc.OperationalError:
            await message.answer(
                text=messages.message_data_was_error
            )

        """IndexError: list
        index
        out
        of
        range"""
        "number_of_hours_per_shift=float(float(str(data['company_chart_time']).split('-')[1].split(':')[0]) - float("


    else:
        await state.set_state(
            RegisterShiftInfo.premium
        )

        await message.answer(
            text=messages.message_enter_premium
        )
