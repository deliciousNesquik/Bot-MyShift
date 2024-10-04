from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.RegisterEmployee import RegisterEmployee
from app.resources import messages, keyboards
from app.modules.company_chooser import company_chooser
from app.modules import utils

import re
import logging

import app.database.requests as rq

router_employee_register = Router()

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_employee_register.callback_query(F.data.startswith("set-employee-data_"))
async def handler(call: CallbackQuery, state: FSMContext):
    try:
        access_check_result = await utils.check_user_access(call.from_user.id)

        if access_check_result:
            await call.message.answer(
                text=access_check_result[0],
                reply_markup=access_check_result[1]
            )
            return

        current_employee_id = call.data.split("_")[1]

        await state.update_data(id=current_employee_id)
        await state.set_state(RegisterEmployee.full_name)

        await call.message.answer(text=messages.message_enter_full_name)

    except Exception as e:
        logger.error(f"Ошибка при установке данных сотрудника для пользователя {call.from_user.id}: {e}")
        await call.message.answer(text="Произошла ошибка. Попробуйте снова позже.")


@router_employee_register.message(RegisterEmployee.full_name)
async def handler(message: Message, state: FSMContext):
    full_name = message.text

    # Проверка, что имя не пустое
    if not full_name.strip() or len(full_name.strip()) < 2:
        await message.answer(text="Пожалуйста, введите действительное имя.")
        return

    await state.update_data(full_name=full_name)
    await state.set_state(RegisterEmployee.age)

    await message.answer(text=messages.message_enter_age)


@router_employee_register.message(RegisterEmployee.age)
async def handler(message: Message, state: FSMContext):
    age = message.text.strip()

    # Проверка, что возраст является числом и больше нуля
    if not age.isdigit() or int(age) <= 0:
        await message.answer(text="Пожалуйста, введите корректный возраст (число больше 0).")
        return

    await state.update_data(age=int(age))
    await state.set_state(RegisterEmployee.phone)

    await message.answer(text=messages.message_enter_phone)


@router_employee_register.message(RegisterEmployee.phone)
async def handler(message: Message, state: FSMContext):
    phone = message.text.strip()

    # Проверка формата телефона (пример для России: +7xxxxxxxxxx)
    phone_pattern = re.compile(r"^\+?\d{10,15}$")
    if not phone_pattern.match(phone):
        await message.answer(text="Пожалуйста, введите корректный номер телефона.")
        return

    await state.update_data(phone=phone)
    await state.set_state(RegisterEmployee.bank)

    await message.answer(text=messages.message_enter_bank)


@router_employee_register.message(RegisterEmployee.bank)
async def handler(message: Message, state: FSMContext):
    try:
        access_check_result = await utils.check_user_access(message.from_user.id)

        if access_check_result:
            await message.answer(
                text=access_check_result[0],
                reply_markup=access_check_result[1]
            )
            return

        bank = message.text.strip()

        # Проверка, что банк введён корректно (например, не пустое значение)
        if len(bank) < 2:
            await message.answer(text="Пожалуйста, введите действительное название банка.")
            return

        await state.update_data(bank=bank)

        data = await state.get_data()

        # Обновление данных сотрудника
        await rq.update_employee(
            employee_id=data['id'],
            full_name=data['full_name'],
            age=data['age'],
            phone=data['phone'],
            bank=data['bank']
        )

        employee = await rq.get_employee(employee_id=data['id'])

        # Устанавливаем выбранную компанию для пользователя
        await company_chooser.set_choose(user_id=message.from_user.id, user_choose=employee.company_id)

        await message.answer(text=messages.message_data_was_add)
        await message.answer(text=messages.message_welcome, reply_markup=keyboards.keyboard_whois)

        await state.clear()

        logger.info(f"Пользователь {message.from_user.id} успешно зарегистрировал данные сотрудника.")

    except Exception as e:
        logger.error(f"Ошибка при регистрации сотрудника для пользователя {message.from_user.id}: {e}")
        await message.answer(text="Произошла ошибка при регистрации. Попробуйте позже.")
