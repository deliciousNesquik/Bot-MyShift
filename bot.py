from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers.company.create import router_create_company
from app.handlers.main import router_main
from app.handlers.company.manage import router_manage_company
from app.handlers.shifts.set_data import router_shift_info
from app.handlers.employee.registration import router_employee_register
from app.handlers.employer.main import router_employer
from app.handlers.company.employee import router_manage_employee
from app.database.models import async_main

from data import config
import asyncio
import logging
import sys


async def main():
    await async_main()

    bot = Bot(
        config.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    dispatcher = Dispatcher()

    dispatcher.include_routers(
        router_main,
        router_create_company,
        router_manage_company,
        router_shift_info,
        router_employee_register,
        router_employer,
        router_manage_employee,
    )
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("INFO:aiogram.dispatcher:Stop polling")
