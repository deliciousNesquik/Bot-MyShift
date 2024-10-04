from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from app.resources import keyboards, messages
from app.modules.company_chooser import company_chooser
from app.modules import utils

import app.database.requests as rq
from app.modules.company_role import company_role

import logging

router_manage_company = Router()

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_manage_company.callback_query(F.data.startswith("company-view_"))
async def handler(call: CallbackQuery):
    company_id = call.data.split("_")[1]
    await company_chooser.set_choose(
        user_id=call.from_user.id,
        user_choose=company_id
    )

    access_check_result = await utils.check_user_access(call.from_user.id)

    if access_check_result:
        await call.message.answer(
            text=access_check_result[0],
            reply_markup=access_check_result[1]
        )
        return

    logging.info(f"Пользователь {call.from_user.id} "
                 f"с ролью {await company_role.get_role(call.from_user.id)} "
                 f"выбрал компанию {company_id}")

    company = await rq.get_company_by_id(
        company_id=company_id
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
    if await company_role.get_role(user_id=call.from_user.id) == "employer":
        await call.message.answer(
            text=messages.message_use_keyboard,
            reply_markup=keyboards.keyboard_manage_company
        )
    elif await company_role.get_role(user_id=call.from_user.id) == "employee":
        await call.message.answer(
            text=messages.message_use_keyboard,
            reply_markup=keyboards.keyboard_employee_company
        )


@router_manage_company.message(F.text == "Профиль компании")
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

    if not current_company_id:
        await message.answer(
            text=messages.message_company_not_selected
        )

        return

    await message.answer(f"Профиль для компании с адресом {current_company.company_address}\n\n"
                         f"Данная функция еще в разработке!")


@router_manage_company.message(F.text == "Настройки компании")
async def handler(message: Message):
    access_check_result = await utils.check_user_access(message.from_user.id)

    if access_check_result:
        await message.answer(
            text=access_check_result[0],
            reply_markup=access_check_result[1]
        )
        return

    current_company_id = await company_chooser.get_choose(user_id=message.from_user.id)
    company = await rq.get_company_by_id(
        company_id=current_company_id
    )

    if not current_company_id:
        await message.answer(

            text=messages.message_company_not_selected

        )

        return

    await message.answer(f"Настройки для компании с адресом {company.company_address}\n\n"
                         f"Данная функция еще в разработке")
