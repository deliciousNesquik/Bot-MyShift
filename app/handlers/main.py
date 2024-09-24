from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from aiogram import Bot

from app.resources import keyboards, messages
from app.database import requests as rq

import datetime
import aiogram.exceptions

router_main = Router()


@router_main.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    company_id = message.text.replace('/start', '').replace(' ', '')

    if len(company_id) > 0:

        company = await rq.get_company_by_id(
            company_id=company_id
        )

        employee = await rq.set_employee(
            telegram_id=message.from_user.id,
            company_id=company_id,
            start_date_work=datetime.date.today()
        )

        if employee != -1:
            await message.answer(
                text=await messages.message_get_invite(
                    company_name=company.company_name,
                    company_address=company.company_address
                ),
                reply_markup=await keyboards.keyboard_set_employee_data(employee.id)
            )

            try:
                await bot.send_message(
                    chat_id=company.tg_id,
                    text=messages.message_employee_join
                )
            except aiogram.exceptions.TelegramBadRequest:
                pass

        else:
            await message.answer(
                text=messages.message_employee_already_join
            )
    else:
        await message.answer(
            text=messages.message_welcome,
            reply_markup=keyboards.keyboard_whois
        )
