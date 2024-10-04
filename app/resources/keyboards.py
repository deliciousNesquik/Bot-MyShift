from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_all_company, get_all_employee, get_employee, get_company_by_id, get_employees
from app.resources import messages

keyboard_whois: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=messages.word_button_employer, callback_data='employer'),
        InlineKeyboardButton(text=messages.word_button_employee, callback_data='employee')
    ]
])

keyboard_confirm_create_company: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=messages.message_button_start_create_company, callback_data='create-company')],
    [InlineKeyboardButton(text=messages.message_button_back, callback_data='cancel-manage-company')]
])

keyboard_back_to_manage_company: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=messages.message_button_back, callback_data='cancel-manage-company')]
])

keyboard_manage_company = ReplyKeyboardMarkup(keyboard=
                                              [[KeyboardButton(text="График"), KeyboardButton(text="Сотрудники")],
                                               [KeyboardButton(text="Настройки компании")],
                                               [KeyboardButton(text="Профиль компании")],
                                               [KeyboardButton(text="Сменить компанию")]], resize_keyboard=True)

keyboard_employee_company = ReplyKeyboardMarkup(keyboard=
                                                [[KeyboardButton(text="График"), KeyboardButton(text="Сотрудники")],
                                                 [KeyboardButton(text="Сменить компанию")]], resize_keyboard=True)


async def keyboard_manage_employee(employee_id: int, payment: bool, send: bool, delete: bool):
    keyboard_employee: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if payment:
        keyboard_employee.add(
            InlineKeyboardButton(text=messages.message_button_make_a_payment,
                                 callback_data=f"payment-employee_{employee_id}")
        )
    if send:
        keyboard_employee.add(
            InlineKeyboardButton(text=messages.message_button_send_employee, callback_data=f"send-employee_{employee_id}")
        )
    if delete:
        keyboard_employee.add(
            InlineKeyboardButton(text=messages.message_button_delete_employee,
                                 callback_data=f"delete-employee_{employee_id}")
        )

    return keyboard_employee.adjust(1).as_markup()


async def keyboard_payout(employee_id: int, paysum: float):
    keyboard_set_payout: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_set_payout.add(InlineKeyboardButton(text=messages.message_button_make_payout,
                                                 callback_data=f'payout-employee_{employee_id}_{paysum}'))

    return keyboard_set_payout.adjust(1).as_markup()


async def keyboard_shift(employee_id: int = None, support_id: int = None, can_set_shift: bool = False,
                         can_replacement_shift: bool = False, date: str = None):
    keyboard_shift_management: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if employee_id is not None:
        employee = await get_employee(
            employee_id=employee_id
        )

        keyboard_shift_management.add(
            InlineKeyboardButton(
                text=employee.full_name,
                callback_data=f'employee_{employee_id}'
            )
        )
    if support_id is not None:
        support = await get_employee(
            employee_id=support_id
        )

        keyboard_shift_management.add(
            InlineKeyboardButton(
                text=support.full_name,
                callback_data=f'employee_{employee_id}'
            )
        )
    if can_set_shift:
        keyboard_shift_management.add(
            InlineKeyboardButton(
                text="Выйти на смену",
                callback_data=f'shift-set_{date}'
            )
        )
    if can_replacement_shift:
        keyboard_shift_management.add(
            InlineKeyboardButton(
                text="Выйти на подмену",
                callback_data=f'shift-replacement_{date}'
            )
        )

    return keyboard_shift_management.adjust(1).as_markup()


async def keyboard_set_employee_data(employee_id: int):
    keyboard_set_data: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_set_data.add(InlineKeyboardButton(text="Заполнить данные для работодателя",
                                               callback_data=f'set-employee-data_{employee_id}'))

    return keyboard_set_data.adjust(1).as_markup()


async def set_info_shift(company_id: int):
    keyboard_set_info_shift: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_set_info_shift.add(
        InlineKeyboardButton(text="Заполнить данные о сменах", callback_data=f'set-info-shift_{company_id}'),
    )
    return keyboard_set_info_shift.adjust(1).as_markup()


async def get_manage_company_employee(company_id: int, show_payments: bool, create_invite: bool, send_all: bool, delete_all: bool):
    keyboard_manage_company_employee: InlineKeyboardBuilder = InlineKeyboardBuilder()

    all_employee = await get_all_employee(
        company_id=company_id
    )
    count_employee: int = 0
    for employee in all_employee:
        if employee.full_name == "":
            keyboard_manage_company_employee.add(
                InlineKeyboardButton(text=f"Нет данных", callback_data=f'employee_{employee.id}')
            )
            count_employee += 1
        else:
            keyboard_manage_company_employee.add(
                InlineKeyboardButton(text=f"{str(employee.full_name)}", callback_data=f'employee_{employee.id}')
            )
            count_employee += 1

    if count_employee > 0:
        keyboard_manage_company_employee.add(
            InlineKeyboardButton(text="ㅤ", callback_data=f'---')
        )

        if show_payments:
            keyboard_manage_company_employee.add(
                InlineKeyboardButton(text=messages.message_button_show_all_payout, callback_data=f'payments_{company_id}')
            )
        if create_invite:
            keyboard_manage_company_employee.add(
                InlineKeyboardButton(text="Создать приглашение", callback_data=f'invite-employee_{company_id}')
            )
        if send_all:
            keyboard_manage_company_employee.add(
                InlineKeyboardButton(text="Отправить сообщение всем", callback_data=f'send-all-employee_{company_id}')
            )
        if delete_all:
            keyboard_manage_company_employee.add(
                InlineKeyboardButton(text="Удалить всех", callback_data=f'delete-all-employee_{company_id}')
            )

    else:
        if create_invite:
            keyboard_manage_company_employee.add(
                InlineKeyboardButton(text="Создать приглашение", callback_data=f'invite-employee_{company_id}')
            )

    return keyboard_manage_company_employee.adjust(1).as_markup()


async def get_manage_company_keyboard(tg_id: int, callback_prefix: str, add_create_delete_buttons: bool = True):
    all_company = await get_all_company(tg_id)

    keyboard_menu_manage_company: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if add_create_delete_buttons:
        keyboard_menu_manage_company.add(
            InlineKeyboardButton(text=messages.message_button_create_company, callback_data='new-company'),
        )

    for company in all_company:
        keyboard_menu_manage_company.add(
            InlineKeyboardButton(
                text=f"🏢{company.company_name} | {company.company_address}",
                callback_data=f"{callback_prefix}_{company.id}"
            )
        )

    keyboard_menu_manage_company.add(
        InlineKeyboardButton(text=messages.message_button_back, callback_data='cancel-whoiam'))

    if add_create_delete_buttons:
        return keyboard_menu_manage_company.adjust(1).as_markup()
    else:
        return keyboard_menu_manage_company.adjust(1).as_markup()


async def get_employee_company_keyboard(tg_id: int, callback_prefix: str):
    all_employee = await get_employees(telegram_id=tg_id)

    keyboard_menu_employee_company: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for employee in all_employee:
        company = await get_company_by_id(company_id=employee.company_id)

        keyboard_menu_employee_company.add(
            InlineKeyboardButton(
                text=f"🏢{company.company_name} | {company.company_address}",
                callback_data=f"{callback_prefix}_{company.id}"
            )
        )

    keyboard_menu_employee_company.add(
        InlineKeyboardButton(text=messages.message_button_back, callback_data='cancel-whoiam'))

    return keyboard_menu_employee_company.adjust(1).as_markup()
