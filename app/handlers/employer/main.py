from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
import logging

from app.modules.company_role import company_role
from app.resources import messages, keyboards
from app.modules import utils

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router_employer = Router()


@router_employer.callback_query(F.data == "employer")
async def employer_role_handler(call: CallbackQuery):
    """Нажатие кнопки Работодатель"""
    try:
        await company_role.set_role(user_id=call.from_user.id, user_role="employer")
        await call.message.answer(
            text=messages.message_menu_manage_company,
            reply_markup=await keyboards.get_manage_company_keyboard(
                tg_id=call.from_user.id,
                callback_prefix="company-view"
            )
        )
        logger.info(f"Пользователю {call.from_user.id} присвоена роль 'Работодатель'.")
    except Exception as e:
        logger.error(f"Ошибка при установке роли 'Работодатель' для пользователя {call.from_user.id}: {e}")
        await call.message.answer("Произошла ошибка. Попробуйте снова позже.")


@router_employer.callback_query(F.data == "cancel-whoiam")
async def cancel_whoiam_handler(call: CallbackQuery):
    """Нажатие кнопки назад на сообщение выбора роли"""
    try:
        await call.message.answer(
            text=messages.message_welcome,
            reply_markup=keyboards.keyboard_whois
        )
        logger.info(f"Пользователь {call.from_user.id} вернулся к окну выбора роли.")
    except Exception as e:
        logger.error(f"Ошибка при возврате к окну выбора роли для пользователя {call.from_user.id}: {e}")
        await call.message.answer("Произошла ошибка. Попробуйте снова позже.")


@router_employer.callback_query(F.data == "new-company")
async def new_company_handler(call: CallbackQuery):
    """Нажатие кнопки создать новую компанию"""
    try:
        await call.message.answer(
            text=messages.message_create_company,
            reply_markup=keyboards.keyboard_confirm_create_company
        )
        logger.info(f"Пользователь {call.from_user.id} инициировал создание новой компании.")
    except Exception as e:
        logger.error(f"Ошибка при создании новой компании пользователем {call.from_user.id}: {e}")
        await call.message.answer("Произошла ошибка. Попробуйте снова позже.")


@router_employer.callback_query(F.data == "cancel-manage-company")
async def cancel_manage_company_handler(call: CallbackQuery):
    """Нажатие кнопки назад к окну взаимодействия с компаниями"""
    try:
        access_check_result = await utils.check_user_access(call.from_user.id)
        if access_check_result:
            await call.message.answer(
                text=access_check_result[0],
                reply_markup=access_check_result[1]
            )
            return

        user_role = await company_role.get_role(user_id=call.from_user.id)

        if user_role == "employer":
            await call.message.answer(
                text=messages.message_menu_manage_company,
                reply_markup=await keyboards.get_manage_company_keyboard(
                    tg_id=call.from_user.id,
                    callback_prefix="company-view"
                )
            )
            logger.info(f"Пользователь {call.from_user.id} вернулся к управлению компаниями как Работодатель.")
        elif user_role == "employee":
            await call.message.answer(
                text=messages.message_menu_employee_company,
                reply_markup=await keyboards.get_employee_company_keyboard(
                    tg_id=call.from_user.id,
                    callback_prefix="company-view"
                )
            )
            logger.info(f"Пользователь {call.from_user.id} вернулся к управлению как Сотрудник.")
    except Exception as e:
        logger.error(f"Ошибка при возвращении к управлению компаниями для пользователя {call.from_user.id}: {e}")
        await call.message.answer("Произошла ошибка. Попробуйте снова позже.")


@router_employer.message(F.text == "Сменить компанию")
async def change_company_handler(message: Message):
    """Нажатие кнопки смены компании"""
    try:
        access_check_result = await utils.check_user_access(message.from_user.id)
        if access_check_result:
            await message.answer(
                text=access_check_result[0],
                reply_markup=access_check_result[1]
            )
            return

        user_role = await company_role.get_role(user_id=message.from_user.id)

        if user_role == "employer":
            await message.answer(
                text=messages.message_menu_manage_company,
                reply_markup=await keyboards.get_manage_company_keyboard(
                    tg_id=message.from_user.id,
                    callback_prefix="company-view"
                )
            )
            logger.info(f"Пользователь {message.from_user.id} выбрал смену компании как Работодатель.")
        elif user_role == "employee":
            await message.answer(
                text=messages.message_menu_employee_company,
                reply_markup=await keyboards.get_employee_company_keyboard(
                    tg_id=message.from_user.id,
                    callback_prefix="company-view"
                )
            )
            logger.info(f"Пользователь {message.from_user.id} выбрал смену компании как Сотрудник.")
        else:
            await message.answer(
                text=messages.message_welcome,
                reply_markup=keyboards.keyboard_whois
            )
            logger.info(f"Пользователь {message.from_user.id} вернулся к окну выбора роли.")
    except Exception as e:
        logger.error(f"Ошибка при смене компании для пользователя {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова позже.")
