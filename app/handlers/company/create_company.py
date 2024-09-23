from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.States.RegisterCompanyStateGroup import RegisterCompany
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
    await state.update_data(
        company_manager_phone=message.text
    )

    await state.set_state(
        RegisterCompany.company_manager_post
    )

    await message.answer(
        text=messages.message_enter_manager_post
    )


@router_create_company.message(RegisterCompany.company_manager_post)
async def handler(message: Message, state: FSMContext):
    await state.update_data(
        company_manager_post=message.text
    )

    company_data = await state.get_data()

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
            "Индефикатор компании:\n" + f"└<b>{company.id}</b>\n\n"
                                        "Название компании:\n" + f"└<b>{company_data["company_name"]}</b>\n\n"
                                                                 "Адрес компании:\n" + f"└<b>{company_data["company_address"]}</b>\n\n"
                                                                                       "Вид деятельности:\n" + f"└<b>{company_data["company_type_of_activity"]}</b>\n\n"
                                                                                                               "Фамилия Имя Отчество:\n" + f"└<b>{company_data["company_manager_name"]}</b>\n\n"
                                                                                                                                           "Номер телефона:\n" + f"└<b>{company_data["company_manager_phone"]}</b>\n\n"
                                                                                                                                                                 "Должность в компании:\n" + f"└<b>{company_data["company_manager_post"]}</b>\n\n"
                                                                                                                                                                                             "Компания успешно создалась!",
            reply_markup=keyboards.keyboard_back_to_manage_company
        )
    else:
        await message.answer(
            messages.message_company_already_create,
            reply_markup=keyboards.keyboard_back_to_manage_company
        )
