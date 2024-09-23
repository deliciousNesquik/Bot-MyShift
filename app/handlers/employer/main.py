from aiogram.types import Message, CallbackQuery
from aiogram import Router, F

from app.resources import messages, keyboards

router_employer = Router()


@router_employer.callback_query(F.data == "employer")
async def handler(call: CallbackQuery):
    await call.message.answer(
        text=messages.message_menu_manage_company,
        reply_markup=await keyboards.get_manage_company_keyboard(
            tg_id=call.from_user.id,
            callback_prefix="company-view"
        )
    )


@router_employer.callback_query(F.data == "cancel-whoiam")
async def handler(call: CallbackQuery):
    await call.message.answer(
        text=messages.message_welcome,
        reply_markup=keyboards.keyboard_whois
    )


@router_employer.callback_query(F.data == "new-company")
async def handler(call: CallbackQuery):
    await call.message.answer(
        text=messages.message_create_company,
        reply_markup=keyboards.keyboard_confirm_create_company
    )


@router_employer.callback_query(F.data == "cancel-manage-company")
async def handler(call: CallbackQuery):
    await call.message.answer(
        text=messages.message_menu_manage_company,
        reply_markup=await keyboards.get_manage_company_keyboard(call.from_user.id, "company-view")
    )


@router_employer.message(F.text == "Сменить компанию")
async def handler(message: Message):
    await message.answer(
        text=messages.message_menu_manage_company,
        reply_markup=await keyboards.get_manage_company_keyboard(message.from_user.id, "company-view")
    )
