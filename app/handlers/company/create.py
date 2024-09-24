import sqlalchemy.exc
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.RegisterCompany import RegisterCompany
from app.resources import messages, keyboards

import app.database.requests as rq

router_create_company = Router()


@router_create_company.callback_query(F.data == "create-company")
async def handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(
        RegisterCompany.company_name
    )

    await call.message.answer(
        text=messages.message_enter_company_name
    )


@router_create_company.message(RegisterCompany.company_name)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        company_name=message.text
    )

    await state.set_state(
        RegisterCompany.company_address
    )

    await message.answer(
        text=messages.message_enter_company_adress
    )


@router_create_company.message(RegisterCompany.company_address)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        company_address=message.text
    )

    await state.set_state(
        RegisterCompany.company_type_of_activity
    )

    await message.answer(
        text=messages.message_enter_company_type_of_activity
    )


@router_create_company.message(RegisterCompany.company_type_of_activity)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        company_type_of_activity=message.text
    )

    await state.set_state(
        RegisterCompany.company_manager_name
    )

    await message.answer(
        text=messages.message_enter_manager_name
    )


@router_create_company.message(RegisterCompany.company_manager_name)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        company_manager_name=message.text
    )

    await state.set_state(
        RegisterCompany.company_manager_phone
    )

    await message.answer(
        text=messages.message_enter_manager_phone
    )


@router_create_company.message(RegisterCompany.company_manager_phone)
async def handler(message: Message, state: FSMContext):
    if len(message.text) == 11:
        await state.update_data(
            company_manager_phone=message.text
        )

        await state.set_state(
            RegisterCompany.company_manager_post
        )

        await message.answer(
            text=messages.message_enter_manager_post
        )

    else:
        await state.set_state(
            RegisterCompany.company_manager_phone
        )

        await message.answer(
            text=messages.message_enter_manager_phone
        )


@router_create_company.message(RegisterCompany.company_manager_post)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        company_manager_post=message.text
    )

    company_data = await state.get_data()

    await state.clear()

    try:
        company = await rq.set_company(
            company_data["company_name"],
            company_data["company_address"],
            company_data["company_type_of_activity"],
            message.from_user.id,
            company_data["company_manager_name"],
            company_data["company_manager_phone"],
            company_data["company_manager_post"]
        )

        if company:
            await message.answer(
                text=await messages.message_company_was_created(
                    company_id=company.id,
                    company_name=company_data["company_name"],
                    company_address=company_data["company_address"],
                    company_type_of_activity=company_data["company_type_of_activity"],
                    company_manager_name=company_data["company_manager_name"],
                    company_manager_phone=company_data["company_manager_phone"],
                    company_manager_post=company_data["company_manager_post"]
                ),
                reply_markup=keyboards.keyboard_back_to_manage_company
            )
        else:
            await message.answer(
                messages.message_company_already_create,
                reply_markup=keyboards.keyboard_back_to_manage_company
            )
    except sqlalchemy.exc.OperationalError:
        await message.answer(
            text=messages.message_data_was_error
        )

