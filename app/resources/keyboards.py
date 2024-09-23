from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_all_company, get_employee
from app.resources import messages

keyboard_whois: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=messages.word_button_employer, callback_data='employer'),
        InlineKeyboardButton(text=messages.word_button_employee, callback_data='worker')
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


async def keyboard_set_employee_data(employee_id: int):
    keyboard_set_employee_data: InlineKeyboardBuilder = InlineKeyboardBuilder()

    keyboard_set_employee_data.add(InlineKeyboardButton(text="Заполнить данные для работодателя", callback_data=f'set-employee-data_{employee_id}'))

    return keyboard_set_employee_data.adjust(1).as_markup()


async def set_info_shift(company_id: int):
    keyboard_set_info_shift: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_set_info_shift.add(
        InlineKeyboardButton(text="Заполнить данные о сменах", callback_data=f'set-info-shift_{company_id}'),
    )
    return keyboard_set_info_shift.adjust(1).as_markup()


async def get_manage_company_employee(company_id: int):
    keyboard_manage_company_employee: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard_manage_company_employee.add(
        InlineKeyboardButton(text="Создать приглашение", callback_data=f'invite-employee_{company_id}')
    )

    employee = await get_employee(company_id=company_id)
    for employ in employee:
        keyboard_manage_company_employee.add(
            InlineKeyboardButton(text=f"{str(employ.full_name)}", callback_data=f'employee_{employ.id}')
        )

    return keyboard_manage_company_employee.adjust(1).as_markup()


async def get_manage_company_keyboard(tg_id: int, callback_prefix: str, add_create_delete_buttons: bool = True):
    all_company = await get_all_company(tg_id)

    keyboard_menu_manage_company: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if add_create_delete_buttons:
        keyboard_menu_manage_company.add(
            InlineKeyboardButton(text=messages.message_button_create_company, callback_data='new-company'),
            #InlineKeyboardButton(text=messages.message_button_delete_company, callback_data='delete-company')
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
