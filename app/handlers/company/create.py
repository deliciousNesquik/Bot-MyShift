import logging
import sqlalchemy.exc
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.RegisterCompany import RegisterCompany
from app.resources import messages, keyboards
import app.database.requests as rq

router_create_company = Router()

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router_create_company.callback_query(F.data == "create-company")
async def start_company_creation(call: CallbackQuery, state: FSMContext):
    """Начало процесса регистрации компании."""
    try:
        await state.set_state(RegisterCompany.company_name)
        await call.message.answer(text=messages.message_enter_company_name)
        logger.info(f"Пользователь {call.from_user.id} начал регистрацию компании.")
    except Exception as e:
        logger.error(f"Ошибка при начале регистрации компании: {e}")
        await call.message.answer(text=messages.error_message)


@router_create_company.message(RegisterCompany.company_name)
async def process_company_name(message: Message, state: FSMContext):
    """Обработка введенного названия компании."""
    company_name = message.text.strip()

    if not company_name:
        await message.answer(text=messages.invalid_company_name)
        return

    await state.update_data(company_name=company_name)
    await state.set_state(RegisterCompany.company_address)
    await message.answer(text=messages.message_enter_company_adress)
    logger.info(f"Пользователь {message.from_user.id} ввел название компании: {company_name}")


@router_create_company.message(RegisterCompany.company_address)
async def process_company_address(message: Message, state: FSMContext):
    """Обработка введенного адреса компании."""
    company_address = message.text.strip()

    if not company_address:
        await message.answer(text=messages.invalid_company_address)
        return

    await state.update_data(company_address=company_address)
    await state.set_state(RegisterCompany.company_type_of_activity)
    await message.answer(text=messages.message_enter_company_type_of_activity)
    logger.info(f"Пользователь {message.from_user.id} ввел адрес компании: {company_address}")


@router_create_company.message(RegisterCompany.company_type_of_activity)
async def process_company_activity(message: Message, state: FSMContext):
    """Обработка введенного вида деятельности компании."""
    company_type_of_activity = message.text.strip()

    if not company_type_of_activity:
        await message.answer(text=messages.invalid_company_type_of_activity)
        return

    await state.update_data(company_type_of_activity=company_type_of_activity)
    await state.set_state(RegisterCompany.company_manager_name)
    await message.answer(text=messages.message_enter_manager_name)
    logger.info(f"Пользователь {message.from_user.id} ввел вид деятельности: {company_type_of_activity}")


@router_create_company.message(RegisterCompany.company_manager_name)
async def process_manager_name(message: Message, state: FSMContext):
    """Обработка введенного имени менеджера компании."""
    company_manager_name = message.text.strip()

    if not company_manager_name:
        await message.answer(text=messages.invalid_manager_name)
        return

    await state.update_data(company_manager_name=company_manager_name)
    await state.set_state(RegisterCompany.company_manager_phone)
    await message.answer(text=messages.message_enter_manager_phone)
    logger.info(f"Пользователь {message.from_user.id} ввел имя менеджера: {company_manager_name}")


@router_create_company.message(RegisterCompany.company_manager_phone)
async def process_manager_phone(message: Message, state: FSMContext):
    """Обработка введенного номера телефона менеджера компании."""
    company_manager_phone = message.text.strip()

    if len(company_manager_phone) != 11 or not company_manager_phone.isdigit():
        await message.answer(text=messages.invalid_manager_phone)
        return

    await state.update_data(company_manager_phone=company_manager_phone)
    await state.set_state(RegisterCompany.company_manager_post)
    await message.answer(text=messages.message_enter_manager_post)
    logger.info(f"Пользователь {message.from_user.id} ввел номер телефона менеджера: {company_manager_phone}")


@router_create_company.message(RegisterCompany.company_manager_post)
async def process_manager_post(message: Message, state: FSMContext):
    """Обработка введенной должности менеджера компании."""
    company_manager_post = message.text.strip()

    if not company_manager_post:
        await message.answer(text=messages.invalid_manager_post)
        return

    await state.update_data(company_manager_post=company_manager_post)
    company_data = await state.get_data()
    await state.clear()

    try:
        company = await rq.set_company(
            company_data["company_name"],
            company_data["company_address"],
            company_data["company_type_of_activity"],
            message.from_user.id,
            company_data["company_manager_name"],
            company_data["company_manager_phone"],
            company_data["company_manager_post"]
        )

        if company:
            await message.answer(
                text=await messages.message_company_was_created(
                    company_id=company.id,
                    company_name=company_data["company_name"],
                    company_address=company_data["company_address"],
                    company_type_of_activity=company_data["company_type_of_activity"],
                    company_manager_name=company_data["company_manager_name"],
                    company_manager_phone=company_data["company_manager_phone"],
                    company_manager_post=company_data["company_manager_post"]
                ),
                reply_markup=keyboards.keyboard_back_to_manage_company
            )
            logger.info(f"Компания {company_data['company_name']} успешно создана.")
        else:
            await message.answer(
                messages.message_company_already_create,
                reply_markup=keyboards.keyboard_back_to_manage_company
            )
            logger.warning(f"Компания {company_data['company_name']} уже существует.")
    except sqlalchemy.exc.OperationalError as e:
        logger.error(f"Ошибка при создании компании: {e}")
        await message.answer(text=messages.message_data_was_error)
