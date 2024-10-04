from aiogram.types import ReplyKeyboardRemove

from app.database import requests
from app.modules.company_chooser import company_chooser
from app.modules.company_role import company_role
from app.resources import messages, keyboards

from data.config import subscription

import datetime
import logging

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_subscription(telegram_id: int) -> bool:
    if telegram_id in subscription.keys():
        deadline_subscription = subscription[telegram_id]

        if datetime.datetime.strptime(deadline_subscription, "%d.%m.%Y").date() >= datetime.date.today():
            return True

    return False


async def check_user_access(user_id: int, company_call_id: int = None):
    if not await has_chosen_role(user_id):
        logger.error(f"У пользователя {user_id} нет выбранной роли.")
        return messages.message_welcome, keyboards.keyboard_whois

    if not await has_chosen_company(user_id):
        logger.error(f"У пользователя {user_id} нет выбранной компании.")
        return (
            messages.message_menu_manage_company,
            await keyboards.get_manage_company_keyboard(
                tg_id=user_id,
                callback_prefix="company-view"
            )
        )

    if not await access_to_company(user_id):
        logger.error(f"У пользователя {user_id} нет доступа к данной компании.")
        return (
            "<b>У вас нет доступа к данной компании!</b>Используйте /start",
            ReplyKeyboardRemove(remove_keyboard=True)
        )

    return None  # Возвращаем None, если все проверки пройдены


async def has_chosen_role(telegram_id: int) -> bool:
    logging.info(f"Роль пользователя {telegram_id}: {await company_role.get_role(telegram_id)}")
    return True if await company_role.get_role(telegram_id) is not None else False


async def has_chosen_company(telegram_id: int) -> bool:
    logging.info(f"Выбранная компания пользователя {telegram_id}: {await company_chooser.get_choose(telegram_id)}")
    return True if await company_chooser.get_choose(telegram_id) is not None else False


async def access_to_company(telegram_id: int, company_call_id: int = None) -> bool:
    user_role = await company_role.get_role(telegram_id)
    user_choose_company_id = await company_chooser.get_choose(telegram_id)

    if user_role == "employer":
        if company_call_id is not None:
            logging.info(f"Пользователь {telegram_id} с ролью {user_role} пытается запросить доступ к компании {company_call_id}")
            company = await requests.get_company_by_id(company_call_id)

            try:
                if company.tg_id == telegram_id:
                    logging.info(
                        f"Пользователь {telegram_id} с ролью {user_role} имеет доступ к компании {company_call_id}")
                    return True
            except AttributeError:
                logging.info(f"Компания с ИД {company_call_id} не найдена!")
        else:
            logging.info(f"Пользователь {telegram_id} с ролью {user_role} пытается запросить доступ к компании {user_choose_company_id}")
            company = await requests.get_company_by_id(user_choose_company_id)

            try:
                if company.tg_id == telegram_id:
                    logging.info(f"Пользователь {telegram_id} с ролью {user_role} имеет доступ к компании {user_choose_company_id}")
                    return True
            except AttributeError:
                logging.info(f"Компания с ИД {user_choose_company_id} не найдена!")

    elif user_role == "employee":
        if company_call_id is not None:
            logging.info(f"Пользователь {telegram_id} с ролью {user_role} пытается запросить доступ к компании {company_call_id}")
            all_employee_in_company = await requests.get_all_employee(company_call_id)

            if all_employee_in_company:
                for employee in all_employee_in_company:
                    if employee.telegram_id == telegram_id:
                        logging.info(f"Пользователь {telegram_id} с ролью {user_role} имеет доступ к компании {company_call_id}")
                        return True
        else:
            logging.info(f"Пользователь {telegram_id} с ролью {user_role} пытается запросить доступ к компании {user_choose_company_id}")
            all_employee_in_company = await requests.get_all_employee(user_choose_company_id)

            if all_employee_in_company:
                for employee in all_employee_in_company:
                    if employee.telegram_id == telegram_id:
                        logging.info(
                            f"Пользователь {telegram_id} с ролью {user_role} имеет доступ к компании {user_choose_company_id}")
                        return True

    return False


async def get_part_time(time: str, time_part: int) -> int:
    return int(time.split(':')[time_part])


async def get_part_time_range(time_range: str, time_range_part: int) -> str:
    return time_range.split('-')[time_range_part]


async def time_format(time: str) -> bool:
    hours_part = int(time.split(':')[0])
    minutes_part = int(time.split(':')[1])

    if hours_part in range(0, 23) and minutes_part in range(0, 59):
        return True
    else:
        return False


async def time_range_format(time_range: str) -> bool:
    time_range.replace(' ', '')
    if len(time_range.split('-')) == 2:
        if len(time_range.split('-')[0].split(':')) == 2 and len(time_range.split('-')[1].split(':')) == 2:
            return True
        else:
            return False
    else:
        return False


async def get_available_dates(today, start_date_shift, end_date_shift):
    """Определяет доступные даты для сегодняшнего дня, учитывая смену графика.
    :param today: (datetime.date) Сегодняшняя дата.
    :param start_date_shift: int Начальная дата графика.
    :param end_date_shift: int Конечная дата графика.
    """

    dates: list = []
    if today.day > end_date_shift:
        # Переход к новому графику
        new_start_date = datetime.date(today.year, today.month, end_date_shift + 1)
        last_day_month = datetime.date(today.year, today.month, 1).replace(month=today.month + 1,
                                                                           day=1) - datetime.timedelta(days=1)
        dates.extend(range(new_start_date.day, last_day_month.day + 1))
        dates.extend(range(1, start_date_shift))
        return dates
    else:
        # Текущий график
        dates = list(range(start_date_shift, end_date_shift + 1))
        return dates


if __name__ == "__main__":
    print(get_part_time("09:00", 0))
