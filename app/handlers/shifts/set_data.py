import sqlalchemy.exc
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from app.modules import utils
from app.states.RegisterShiftInfo import RegisterShiftInfo
from app.resources import messages
import app.database.requests as rq

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router_shift_info = Router()


@router_shift_info.callback_query(F.data.startswith("set-info-shift_"))
async def set_info_shift_handler(call: CallbackQuery, state: FSMContext):
    """Обработчик установки информации о смене"""
    try:
        access_check_result = await utils.check_user_access(call.from_user.id, call.data.split("_")[1])

        if access_check_result:
            await call.message.answer(
                text=access_check_result[0],
                reply_markup=access_check_result[1]
            )
            return

        await state.update_data(company_id=call.data.split("_")[1])
        await state.set_state(RegisterShiftInfo.company_chart)

        await call.message.answer(text=messages.message_enter_schedule)
        logger.info(f"Пользователь {call.from_user.id} начал процесс регистрации смены.")
    except Exception as e:
        logger.error(f"Ошибка при установке информации о смене для {call.from_user.id}: {e}")
        await call.message.answer("Произошла ошибка. Попробуйте снова позже.")


@router_shift_info.message(RegisterShiftInfo.company_chart)
async def company_chart_handler(message: Message, state: FSMContext):
    """Обработчик ввода расписания компании"""
    try:
        if message.text.lower() in ("ежедневно", "5/2", "6/1"):
            await state.update_data(company_chart=message.text)
            await state.set_state(RegisterShiftInfo.start_date_shift)
            await message.answer(text=messages.message_enter_startday)
            logger.info(f"Пользователь {message.from_user.id} выбрал график: {message.text}.")
        else:
            await message.answer(text=messages.message_enter_schedule)
            logger.warning(f"Пользователь {message.from_user.id} ввел неверный график: {message.text}.")
    except Exception as e:
        logger.error(f"Ошибка при вводе графика компании для {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова.")


@router_shift_info.message(RegisterShiftInfo.start_date_shift)
async def start_date_shift_handler(message: Message, state: FSMContext):
    """Обработчик ввода даты начала смены"""
    try:
        if int(message.text):
            await state.update_data(start_date_shift=message.text)
            await state.set_state(RegisterShiftInfo.end_date_shift)
            await message.answer(text=messages.message_enter_endday)
            logger.info(f"Пользователь {message.from_user.id} указал дату начала смены: {message.text}.")
    except ValueError:
        await message.answer(text=messages.message_enter_startday)
        logger.warning(f"Пользователь {message.from_user.id} ввел неверную дату начала: {message.text}.")
    except Exception as e:
        logger.error(f"Ошибка при вводе даты начала смены для {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова.")


@router_shift_info.message(RegisterShiftInfo.end_date_shift)
async def end_date_shift_handler(message: Message, state: FSMContext):
    """Обработчик ввода даты окончания смены"""
    try:
        if int(message.text):
            await state.update_data(end_date_shift=message.text)
            await state.set_state(RegisterShiftInfo.company_chart_time)
            await message.answer(text=messages.message_enter_charttime)
            logger.info(f"Пользователь {message.from_user.id} указал дату окончания смены: {message.text}.")
    except ValueError:
        await message.answer(text=messages.message_enter_endday)
        logger.warning(f"Пользователь {message.from_user.id} ввел неверную дату окончания: {message.text}.")
    except Exception as e:
        logger.error(f"Ошибка при вводе даты окончания смены для {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова.")


@router_shift_info.message(RegisterShiftInfo.company_chart_time)
async def company_chart_time_handler(message: Message, state: FSMContext):
    """Обработчик ввода времени работы компании"""
    try:
        if len(message.text) == 11:
            await state.update_data(company_chart_time=message.text)
            await state.set_state(RegisterShiftInfo.payment_per_hour)
            await message.answer(text=messages.message_enter_payrephouse)
            logger.info(f"Пользователь {message.from_user.id} указал время работы: {message.text}.")
        else:
            await message.answer(text=messages.message_enter_charttime)
            logger.warning(f"Пользователь {message.from_user.id} ввел неверное время работы: {message.text}.")
    except Exception as e:
        logger.error(f"Ошибка при вводе времени работы компании для {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова.")


@router_shift_info.message(RegisterShiftInfo.payment_per_hour)
async def payment_per_hour_handler(message: Message, state: FSMContext):
    """Обработчик ввода оплаты за час работы"""
    try:
        if int(message.text):
            await state.update_data(payment_per_hour=message.text)
            await state.set_state(RegisterShiftInfo.payment_for_over_fulfillment)
            await message.answer(text=messages.message_enter_paymentforoverfulfillment)
            logger.info(f"Пользователь {message.from_user.id} указал оплату за час: {message.text}.")
    except ValueError:
        await message.answer(text=messages.message_enter_payrephouse)
        logger.warning(f"Пользователь {message.from_user.id} ввел неверную оплату за час: {message.text}.")
    except Exception as e:
        logger.error(f"Ошибка при вводе оплаты за час для {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова.")


@router_shift_info.message(RegisterShiftInfo.payment_for_over_fulfillment)
async def payment_for_over_fulfillment_handler(message: Message, state: FSMContext):
    """Обработчик ввода оплаты за перевыполнение"""
    try:
        if message.text.lower() in ("да", "нет"):
            await state.update_data(payment_for_over_fulfillment=message.text)
            await state.set_state(RegisterShiftInfo.premium)
            await message.answer(text=messages.message_enter_premium)
            logger.info(f"Пользователь {message.from_user.id} указал оплату за перевыполнение: {message.text}.")
        else:
            await message.answer(text=messages.message_enter_paymentforoverfulfillment)
            logger.warning(f"Пользователь {message.from_user.id} ввел неверное значение для перевыполнения: {message.text}.")
    except Exception as e:
        logger.error(f"Ошибка при вводе оплаты за перевыполнение для {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова.")


@router_shift_info.message(RegisterShiftInfo.premium)
async def premium_handler(message: Message, state: FSMContext):
    """Обработчик ввода премии"""
    try:
        if message.text.lower() in ("да", "нет"):
            await state.update_data(premium=message.text)
            data = await state.get_data()
            await state.clear()

            try:
                # Расчет количества часов
                hours_per_shift = float(
                    float(data['company_chart_time'].split('-')[1].split(':')[0]) -
                    float(data['company_chart_time'].split('-')[0].split(':')[0])
                )

                await rq.set_shift_config(
                    company_id=data['company_id'],
                    company_chart=data['company_chart'],
                    company_chart_time=data['company_chart_time'],
                    start_date_shift=data['start_date_shift'],
                    end_date_shift=data['end_date_shift'],
                    number_of_hours_per_shift=hours_per_shift,
                    payment_per_hour=data['payment_per_hour'],
                    payment_for_over_fulfillment=(data['payment_for_over_fulfillment'].lower() == "да"),
                    premium=(data['premium'].lower() == "да")
                )

                await message.answer(text=messages.message_data_was_update)
                logger.info(f"Данные по смене успешно обновлены для компании {data['company_id']}.")
            except sqlalchemy.exc.OperationalError as e:
                logger.error(f"Ошибка базы данных при обновлении смены для компании {data['company_id']}: {e}")
                await message.answer(text=messages.message_data_was_error)
        else:
            await message.answer(text=messages.message_enter_premium)
            logger.warning(f"Пользователь {message.from_user.id} ввел неверное значение премии: {message.text}.")
    except Exception as e:
        logger.error(f"Ошибка при вводе премии для {message.from_user.id}: {e}")
        await message.answer("Произошла ошибка. Попробуйте снова.")
