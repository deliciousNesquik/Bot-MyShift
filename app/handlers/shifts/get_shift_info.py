from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.States.RegisterShiftInfoStateGroup import RegisterShiftInfo

import app.database.requests as rq

router_shift_info = Router()


@router_shift_info.callback_query(F.data.startswith("set-info-shift_"))
async def handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(company_id = call.data.split("_")[1])

    await state.set_state(RegisterShiftInfo.company_chart)
    await call.message.answer(f"<b>Введите тип графика комапнии</b>\n\n"
                              f"5/2, 6/1, ежедневно")


@router_shift_info.message(RegisterShiftInfo.company_chart)
async def handler(message: Message, state: FSMContext):
    await state.update_data(company_chart=message.text)
    await state.set_state(RegisterShiftInfo.start_date_shift)
    await message.answer(f"<b>Введите с какого дня будет сгенерирован график</b>\n\n"
                         f"Используйте формат числа. Например: 9 - то есть с 9 числа каждого месяца будет "
                         f"генерироваться график")


@router_shift_info.message(RegisterShiftInfo.start_date_shift)
async def handler(message: Message, state: FSMContext):
    await state.update_data(start_date_shift=message.text)
    await state.set_state(RegisterShiftInfo.end_date_shift)
    await message.answer(f"<b>Введите по какой день будет сгенерирован график</b>\n\n"
                         f"Используйте формат числа. Например: 25 - то есть по 25 число каждого месяца будет "
                         f"генерироваться график")


@router_shift_info.message(RegisterShiftInfo.end_date_shift)
async def handler(message: Message, state: FSMContext):
    await state.update_data(end_date_shift=message.text)
    await state.set_state(RegisterShiftInfo.company_chart_time)
    await message.answer(f"<b>Введите время работы компании</b>\n\n"
                         f"Используйте формат типа 09:00-21:00")


@router_shift_info.message(RegisterShiftInfo.company_chart_time)
async def handler(message: Message, state: FSMContext):
    await state.update_data(company_chart_time=message.text)
    await state.set_state(RegisterShiftInfo.payment_per_hour)
    await message.answer(f"<b>Введите оплату за час работы компании</b>\n\n"
                         f"Используйте формат 120.0")


@router_shift_info.message(RegisterShiftInfo.payment_per_hour)
async def handler(message: Message, state: FSMContext):
    await state.update_data(payment_per_hour=message.text)
    await state.set_state(RegisterShiftInfo.payment_for_over_fulfillment)
    await message.answer(f"<b>Оплачивается ли излишки за час работы компании</b>\n\n"
                         f"Используйте формат Да/Нет\n"
                         f"Да - если работник задержится тогда это будет учитыватся\n"
                         f"Нет - если не учитывается время задержки после работы")


@router_shift_info.message(RegisterShiftInfo.payment_for_over_fulfillment)
async def handler(message: Message, state: FSMContext):
    await state.update_data(payment_for_over_fulfillment=message.text)
    await state.set_state(RegisterShiftInfo.premium)
    await message.answer(f"<b>Есть ли премия за работу в компании</b>\n\n"
                         f"Используйте формат Да/Нет\n"
                         f"Да - если есть премии\n"
                         f"Нет - если нет премии")


@router_shift_info.message(RegisterShiftInfo.premium)
async def handler(message: Message, state: FSMContext):
    await state.update_data(premium=message.text)
    data = await state.get_data()

    await rq.set_shift_config(
        company_id=data['company_id'],
        company_chart=data['company_chart'],
        company_chart_time=data['company_chart_time'],
        start_date_shift=data['start_date_shift'],
        end_date_shift=data['end_date_shift'],
        number_of_hours_per_shift=float(float(str(data['company_chart_time']).split('-')[1].split(':')[0]) - float(str(data['company_chart_time']).split('-')[0].split(':')[0])),
        payment_per_hour=data['payment_per_hour'],
        payment_for_over_fulfillment=True if str(data['payment_for_over_fulfillment']).lower() == "да" else False,
        premium=True if str(data['premium']).lower() == "да" else False
    )


    await message.answer(f"<b>Данные успешно обновлены!</b>")
