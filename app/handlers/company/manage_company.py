from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.States.ChoiseCompanyStateGroup import ChooseCompany
from app.resources import keyboards

import app.database.requests as rq

router_manage_company = Router()


@router_manage_company.callback_query(F.data.startswith("company-view_"))
async def handler(call: CallbackQuery, state: FSMContext):
    company_id = call.data.split("_")[1]

    await state.set_state(ChooseCompany.company_id)
    await state.update_data(company_id=company_id)

    company = await rq.get_company(company_id)

    await call.message.answer(
        "<b>Управление компанией:</b>\n\n"
        "Индефикатор компании:\n" + f"└<b>{company.id}</b>\n\n"
                                    "Название компании:\n" + f"└<b>{company.company_name}</b>\n\n"
                                                             "Адрес компании:\n" + f"└<b>{company.company_address}</b>\n\n"
                                                                                   "Вид деятельности:\n" + f"└<b>{company.company_type_of_activity}</b>\n\n",
        reply_markup=keyboards.keyboard_back_to_manage_company
    )

    await call.message.answer(
        "Для управления данной компанией используйте кнопки на вашей клавиатуре!",
        reply_markup=keyboards.keyboard_manage_company
    )


@router_manage_company.message(F.text == "График")
async def handler(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        current_company_id = data['company_id']
    except Exception:
        await message.answer("<b>Компания не выбрана!</b>\n\n"
                             "Пожалуйста нажмите в меню компании "
                             "на одну из предложенных или нажмите на клавиатуре Сменить компанию и управляйте ей!")
        return

    company = await rq.get_company(company_id=current_company_id)
    company_shift_conf = await rq.get_shift_config(current_company_id)
    try:
        await message.answer(f"<b>График компании</b>\n└{company.company_address}\n\n"
                             f"График работы:\n" + f"└<b>{company_shift_conf.company_chart}  {company_shift_conf.company_chart_time}</b>\n\n" +
                             f"Количество часов в смене:\n" + f"└<b>{company_shift_conf.number_of_hours_per_shift}</b>\n\n" +
                             f"Оплата за час работы:\n" + f"└<b>{company_shift_conf.payment_per_hour}</b>\n\n" +
                             f"Оплата за переизбыток часов:\n" + f"└<b>{'Да' if company_shift_conf.payment_for_over_fulfillment else 'Нет'}</b>\n\n" +
                             f"Оплата премий:\n" + f"└<b>{'Да' if company_shift_conf.premium else 'Нет'}</b>\n\n"
                                                   f"Составление графика:\n" + f"└<b>с {company_shift_conf.start_date_shift} по {company_shift_conf.end_date_shift}</b>"
                             )
    except Exception:
        await message.answer(f"График для компании с адресом {company.company_address}\n\n"
                             f"Данные отсутствуют, пожалуйста заполните их!",
                             reply_markup=await keyboards.set_info_shift(current_company_id))


@router_manage_company.message(F.text == "Профиль компании")
async def handler(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        current_company_id = data['company_id']
        company = await rq.get_company(company_id=current_company_id)
    except Exception:
        await message.answer("<b>Компания не выбрана!</b>\n\n"
                             "Пожалуйста нажмите в меню компании "
                             "на одну из предложенных или нажмите на клавиатуре Сменить компанию и управляйте ей!")
        return

    await message.answer(f"Профиль для компании с адресом {company.company_address}\n\n")


@router_manage_company.message(F.text == "Настройки компании")
async def handler(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        current_company_id = data['company_id']
        company = await rq.get_company(company_id=current_company_id)
    except Exception:
        await message.answer("<b>Компания не выбрана!</b>\n\n"
                             "Пожалуйста нажмите в меню компании "
                             "на одну из предложенных или нажмите на клавиатуре Сменить компанию и управляйте ей!")
        return

    await message.answer(f"Настройки для компании с адресом {company.company_address}\n\n")


@router_manage_company.message(F.text == "Сотрудники")
async def handler(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        current_company_id = data['company_id']
        company = await rq.get_company(company_id=current_company_id)
    except Exception:
        await message.answer("<b>Компания не выбрана!</b>\n\n"
                             "Пожалуйста нажмите в меню компании "
                             "на одну из предложенных или нажмите на клавиатуре Сменить компанию и управляйте ей!")
        return
    await message.answer(f"<b>Сотрудники компании</b>\n"
                         f"└{company.company_address}\n\n"
                         f"Количество сотрудников\n"
                         f"└{await rq.count_employee(company_id=current_company_id)}", reply_markup=await keyboards.get_manage_company_employee(current_company_id))


@router_manage_company.callback_query(F.data.startswith("invite-employee_"))
async def handler(call: CallbackQuery):
    await call.message.answer(f"<b>Пригласительная ссылка</b>\n\n"
                              f"Данная ссылка может использоваться для нескольких сотрудников\n"
                              f"https://t.me/workRoster_bot?start={call.data.split("_")[1]}")
