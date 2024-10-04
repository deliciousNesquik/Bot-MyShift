from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from app.modules import utils
from app.states.ReplacementShift import ReplacementShift
import app.database.requests as rq

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router_shift_manage = Router()


@router_shift_manage.callback_query(F.data.startswith("shift-set_"))
async def set_shift_handler(call: CallbackQuery):
    """Обработка запроса на установку смены"""
    try:
        access_check_result = await utils.check_user_access(call.from_user.id)

        if access_check_result:
            await call.message.answer(
                text=access_check_result[0],
                reply_markup=access_check_result[1]
            )
            return

        employee = await rq.get_employee(telegram_id=call.from_user.id)
        shift_date = call.data.split("_")[1]

        if not await rq.get_shift(date=shift_date):
            await rq.take_shift(
                company_id=employee.company_id,
                employee_id=employee.id,
                date=shift_date,
                hours=12
            )

        shift = await rq.get_shift(date=shift_date)

        if shift.employee_id == employee.id:
            await call.message.answer(text="Запись прошла успешно!")
            logger.info(f"Смена установлена для сотрудника {call.from_user.id} на дату {shift_date}.")
        else:
            await call.message.answer(text="Запись не прошла!")
            logger.error(f"Не удалось установить смену для сотрудника {call.from_user.id} на дату {shift_date}.")
    except Exception as e:
        logger.error(f"Ошибка при установке смены для {call.from_user.id}: {e}")
        await call.message.answer("Произошла ошибка. Попробуйте снова позже.")


@router_shift_manage.callback_query(F.data.startswith("shift-replacement_"))
async def shift_replacement_handler(call: CallbackQuery, state: FSMContext):
    """Обработка запроса на подмену смены"""
    try:
        access_check_result = await utils.check_user_access(call.from_user.id)

        if access_check_result:
            await call.message.answer(
                text=access_check_result[0],
                reply_markup=access_check_result[1]
            )
            return

        shift_date = call.data.split("_")[1]
        shift = await rq.get_shift(date=shift_date)
        employee = await rq.get_employee(telegram_id=call.from_user.id)

        if shift.employee_id == employee.id:
            await call.message.answer(
                text="<b>Основной сотрудник не может выйти на подмену сам себе!</b>"
            )
            logger.info(f"Пользователь {call.from_user.id} попытался подменить сам себя на дату {shift_date}.")
            return

        await state.update_data(shift_date=shift_date)
        await state.set_state(ReplacementShift.time_range)

        await call.message.answer(
            text="Для того чтобы записаться на подмену, необходимо написать время подмены, используйте формат 09:00-14:00"
        )
        logger.info(f"Пользователь {call.from_user.id} начал процесс подмены смены на {shift_date}.")
    except Exception as e:
        logger.error(f"Ошибка при запросе подмены смены для {call.from_user.id}: {e}")
        await call.message.answer("Произошла ошибка. Попробуйте снова позже.")


@router_shift_manage.message(ReplacementShift.time_range)
async def set_replacement_time_handler(message: Message, state: FSMContext):
    """Обработка ввода времени подмены"""
    try:
        access_check_result = await utils.check_user_access(message.from_user.id)

        if access_check_result:
            await message.answer(
                text=access_check_result[0],
                reply_markup=access_check_result[1]
            )
            return

        if await utils.time_range_format(message.text):
            start_time = await utils.get_part_time_range(message.text, 0)
            end_time = await utils.get_part_time_range(message.text, 1)

            if await utils.time_format(start_time) and await utils.time_format(end_time):
                data = await state.get_data()
                shift_date = data['shift_date']
                shift = await rq.get_shift(date=shift_date)

                support_employee = await rq.get_employee(telegram_id=message.from_user.id)
                support_hours = await utils.get_part_time(end_time, 0) - await utils.get_part_time(start_time, 0)
                main_hours = shift.hours - support_hours

                await rq.ask_replacement_shift(
                    support_employee=support_employee.id,
                    support_hours=support_hours,
                    main_hours=main_hours,
                    date=shift_date
                )

                shift = await rq.get_shift(date=shift_date)

                if shift.support_employee == support_employee.id:
                    await message.answer(text="Запись прошла успешно!")
                    logger.info(f"Пользователь {message.from_user.id} успешно записался на подмену на {shift_date}.")
                else:
                    await message.answer(text="Запись не прошла!")
                    logger.error(f"Не удалось записать пользователя {message.from_user.id} на подмену на {shift_date}.")
                await state.clear()
                return

        await state.set_state(ReplacementShift.time_range)
        await message.answer(
            text="Неверный формат времени. Используйте формат 09:00-14:00"
        )
        logger.warning(f"Пользователь {message.from_user.id} ввел неверный формат времени для подмены.")
    except Exception as e:
        logger.error(f"Ошибка при установке времени подмены для {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова позже.")
