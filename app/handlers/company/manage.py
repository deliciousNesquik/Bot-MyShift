from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from app.resources import keyboards, messages
from app.modules.company_chooser import company_chooser

import app.database.requests as rq

router_manage_company = Router()


@router_manage_company.callback_query(F.data.startswith("company-view_"))
async def handler(call: CallbackQuery):
    current_company_id = call.data.split("_")[1]

    await company_chooser.set_choose(
        user_id=call.from_user.id,
        user_choose=current_company_id
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


@router_manage_company.message(F.text == "Профиль компании")
async def handler(message: Message):
    current_company_id = await company_chooser.get_choose(
                            user_id=message.from_user.id
                        )

    current_company = await rq.get_company_by_id(
        company_id=current_company_id
    )

    if not current_company_id:
        await message.answer(

            text=messages.message_company_not_selected

        )

        return

    await message.answer(f"Профиль для компании с адресом {current_company.company_address}\n\n")


@router_manage_company.message(F.text == "Настройки компании")
async def handler(message: Message):
    current_company_id = await company_chooser.get_choose(
                            user_id=message.from_user.id
                        )

    company = await rq.get_company_by_id(
        company_id=current_company_id
    )

    if not current_company_id:
        await message.answer(

            text=messages.message_company_not_selected

        )

        return

    await message.answer(f"Настройки для компании с адресом {company.company_address}\n\n")



