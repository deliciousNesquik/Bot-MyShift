from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.RegisterEmployee import RegisterEmployee
from app.resources import messages

import app.database.requests as rq

router_employee_register = Router()


@router_employee_register.callback_query(F.data.startswith("set-employee-data_"))
async def handler(call: CallbackQuery, state: FSMContext):
    current_employee_id = call.data.split("_")[1]

    await state.update_data(
        id=current_employee_id
    )

    await state.set_state(
        RegisterEmployee.full_name
    )

    await call.message.answer(
        text=messages.message_enter_full_name
    )


@router_employee_register.message(RegisterEmployee.full_name)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        full_name=message.text
    )

    await state.set_state(
        RegisterEmployee.age
    )

    await message.answer(
        text=messages.message_enter_age
    )


@router_employee_register.message(RegisterEmployee.age)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        age=message.text
    )

    await state.set_state(
        RegisterEmployee.phone
    )

    await message.answer(
        text=messages.message_enter_phone
    )


@router_employee_register.message(RegisterEmployee.phone)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        phone=message.text
    )

    await state.set_state(
        RegisterEmployee.bank
    )

    await message.answer(
        text=messages.message_enter_bank
    )


@router_employee_register.message(RegisterEmployee.bank)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        bank=message.text
    )

    data = await state.get_data()

    await rq.update_employee(
        employee_id=data['id'],
        full_name=data['full_name'],
        age=data['age'],
        phone=data['phone'],
        bank=data['bank']
    )

    await message.answer(
        text=messages.message_data_was_add
    )

    await state.clear()
