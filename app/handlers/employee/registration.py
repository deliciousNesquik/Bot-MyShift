from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.States.RegisterEmployee import RegisterEmployee
import app.database.requests as rq

router_employee_register = Router()


@router_employee_register.callback_query(F.data.startswith("set-employee-data_"))
async def handler(call: CallbackQuery, state: FSMContext):
    employee_id = call.data.split("_")[1]
    await state.update_data(id=employee_id)
    await state.set_state(RegisterEmployee.full_name)

    await call.message.answer("<b>Пожалуйста введите свое ФИО</b>\n\n"
                              "Необходимо ввести полностью фио, эти данные будут видны только работодателю!")


@router_employee_register.message(RegisterEmployee.full_name)
async def handler(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    await state.set_state(RegisterEmployee.age)
    await message.answer("<b>Пожалуйста введите свой возраст</b>\n\n"
                         "Необходимо ввести ваш текущий полный возраст. Например: 18, эти данные будут видны только работодателю!")

@router_employee_register.message(RegisterEmployee.age)
async def handler(message: Message, state: FSMContext):
    await state.update_data(age=message.text)

    await state.set_state(RegisterEmployee.phone)
    await message.answer("<b>Пожалуйста введите свой номер телефона</b>\n\n"
                         "Необходимо ввести номер телефона в формате: 89991234567, эти данные будут видны только работодателю!")


@router_employee_register.message(RegisterEmployee.phone)
async def handler(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)

    await state.set_state(RegisterEmployee.bank)
    await message.answer("<b>Пожалуйста введите название банка</b>\n\n"
                         "Необходимо ввести название банка для того чтобы перечилять зп, эти данные будут видны только работадателю!")


@router_employee_register.message(RegisterEmployee.bank)
async def handler(message: Message, state: FSMContext):
    await state.update_data(bank=message.text)

    data = await state.get_data()

    await rq.update_employee(
        data['id'],
        data['full_name'],
        data['age'],
        data['phone'],
        data['bank']
    )

    await message.answer("<b>Данные успешно добавлены!</b>")