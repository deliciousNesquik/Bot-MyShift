from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram import Router
from aiogram import Bot

from app.resources import keyboards, messages
from app.database import requests as rq
from app.modules.company_role import company_role
from app.modules.company_chooser import company_chooser

from datetime import date

import logging
import aiogram.exceptions

router_main = Router()


@router_main.message(Command("start"))
async def cmd_start(message: Message, bot: Bot, command: CommandObject):
    company_id = command.args or ''

    if len(company_id) > 0:
        "Условие если боту написали по пригласительной ссылке"
        company = await rq.get_company_by_id(company_id=company_id)
        employee = await rq.set_employee(telegram_id=message.from_user.id, company_id=company_id, start_date_work=date.today())

        await company_role.set_role(user_id=message.from_user.id, user_role="employee")
        await company_chooser.set_choose(user_id=message.from_user.id, user_choose=company_id)

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
                logging.info(f"Сообщение о добавлении сотрудника {employee.id} в компанию {company_id}")
            except aiogram.exceptions.TelegramBadRequest as e:
                logging.error(f"Ошибка отправки сообщения {company.tg_id}: {e}")

        else:
            await message.answer(
                text=messages.message_employee_already_join
            )
            await message.answer(
                text=messages.message_welcome,
                reply_markup=keyboards.keyboard_whois
            )
    else:
        await message.answer(
            text=messages.message_welcome,
            reply_markup=keyboards.keyboard_whois
        )
