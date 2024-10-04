from aiogram.types import CallbackQuery
from aiogram import Router, F
import logging

from app.resources import messages, keyboards
from app.modules.company_role import company_role

router_employee = Router()


@router_employee.callback_query(F.data == "employee")
async def employee_role_handler(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    try:
        # Установим роль пользователя
        await company_role.set_role(user_id=telegram_id, user_role="employee")

        # Отправим сообщение с клавиатурой для выбора компании
        await callback.message.answer(
            text=messages.message_menu_employee_company,
            reply_markup=await keyboards.get_employee_company_keyboard(
                tg_id=telegram_id,
                callback_prefix="company-view"
            )
        )

        logging.info(f"Роль 'employee' успешно присвоена пользователю {telegram_id}")

    except Exception as e:
        logging.error(f"Ошибка после присваивания роли пользователю: {telegram_id}: {e}")
        await callback.message.answer(text="Произошла ошибка. Попробуйте снова позже.")
