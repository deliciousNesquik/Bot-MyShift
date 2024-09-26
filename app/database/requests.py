from app.database.models import async_session
from app.database.schemas import Company, CompanyShiftConfiguration, Employee, Shifts, Payments
from sqlalchemy import select, func, delete, update
from sqlalchemy.sql.functions import coalesce
from datetime import datetime


async def get_company(company_name: str, company_address: str, company_type_of_activity: str, tg_id: int,
                      company_manager_name: str, company_manager_phone: str, company_manager_post: str):
    async with async_session() as session:
        return await session.scalar(
            select(Company).where(
                Company.company_name == company_name,
                Company.company_address == company_address,
                Company.company_type_of_activity == company_type_of_activity,
                Company.tg_id == tg_id,
                Company.company_manager_name == company_manager_name,
                Company.company_manager_phone == company_manager_phone,
                Company.company_manager_post == company_manager_post
            )
        )


async def get_company_by_id(company_id: int):
    async with async_session() as session:
        return await session.scalar(select(Company).where(
            Company.id == company_id
        ))


async def set_company(company_name: str, company_address: str, company_type_of_activity: str, tg_id: int,
                      company_manager_name: str, company_manager_phone: str, company_manager_post: str):
    async with async_session() as session:
        if not await get_company(company_name, company_address, company_type_of_activity, tg_id, company_manager_name,
                                 company_manager_phone, company_manager_post):
            session.add(
                Company(
                    company_name=company_name,
                    company_address=company_address,
                    company_type_of_activity=company_type_of_activity,
                    tg_id=tg_id,
                    company_manager_name=company_manager_name,
                    company_manager_phone=company_manager_phone,
                    company_manager_post=company_manager_post
                )
            )
            await session.commit()

            return await get_company(company_name, company_address, company_type_of_activity, tg_id,
                                     company_manager_name, company_manager_phone, company_manager_post)
        else:
            return -1


async def get_all_company(telegram_id: int):
    async with async_session() as session:
        return await session.scalars(select(Company).where(
            Company.tg_id == telegram_id
        ))


async def get_shift_config(company_id: int):
    async with async_session() as session:
        return await session.scalar(select(CompanyShiftConfiguration).where(
            CompanyShiftConfiguration.company_id == company_id
        ))


async def set_shift_config(company_id: int, company_chart: str, company_chart_time: str, start_date_shift: int,
                           end_date_shift: int, number_of_hours_per_shift: int, payment_per_hour: int,
                           payment_for_over_fulfillment: bool, premium: bool):
    async with async_session() as session:
        company = await session.scalar(
            select(CompanyShiftConfiguration).where(
                CompanyShiftConfiguration.company_id == company_id,
                CompanyShiftConfiguration.company_chart == company_chart,
                CompanyShiftConfiguration.company_chart_time == company_chart_time,
                CompanyShiftConfiguration.start_date_shift == start_date_shift,
                CompanyShiftConfiguration.end_date_shift == end_date_shift,
                CompanyShiftConfiguration.number_of_hours_per_shift == number_of_hours_per_shift,
                CompanyShiftConfiguration.payment_per_hour == payment_per_hour,
                CompanyShiftConfiguration.payment_for_over_fulfillment == payment_for_over_fulfillment,
                CompanyShiftConfiguration.premium == premium,
            )
        )

        if not company:
            session.add(
                CompanyShiftConfiguration(
                    company_id=company_id,
                    company_chart=company_chart,
                    company_chart_time=company_chart_time,
                    start_date_shift=start_date_shift,
                    end_date_shift=end_date_shift,
                    number_of_hours_per_shift=number_of_hours_per_shift,
                    payment_per_hour=payment_per_hour,
                    payment_for_over_fulfillment=payment_for_over_fulfillment,
                    premium=premium,
                )
            )
            await session.commit()
            return await session.scalar(
                select(CompanyShiftConfiguration).where(
                    CompanyShiftConfiguration.company_id == company_id,
                    CompanyShiftConfiguration.company_chart == company_chart,
                    CompanyShiftConfiguration.company_chart_time == company_chart_time,
                    CompanyShiftConfiguration.start_date_shift == start_date_shift,
                    CompanyShiftConfiguration.end_date_shift == end_date_shift,
                    CompanyShiftConfiguration.number_of_hours_per_shift == number_of_hours_per_shift,
                    CompanyShiftConfiguration.payment_per_hour == payment_per_hour,
                    CompanyShiftConfiguration.payment_for_over_fulfillment == payment_for_over_fulfillment,
                    CompanyShiftConfiguration.premium == premium,
                )
            )


async def count_employee(company_id: int):
    async with async_session() as session:
        rows = await session.scalars(
            select(func.count()).select_from(Employee).where(Employee.company_id == company_id))
        return rows.all()[0]


async def get_employee(telegram_id: int = None, employee_id: int = None, company_id: int = None):
    async with async_session() as session:

        if telegram_id is not None:
            return await session.scalar(
                select(Employee)
                .where(
                    Employee.telegram_id == telegram_id
                )
            )
        elif telegram_id is not None and company_id is not None:
            return await session.scalar(
                select(Employee)
                .where(
                    Employee.telegram_id == telegram_id,
                    Employee.company_id == company_id
                )
            )
        else:
            return await session.scalar(
                select(Employee).where(
                    Employee.id == employee_id
                )
            )


async def get_all_employee(company_id: int):
    async with async_session() as session:
        return await session.scalars(select(Employee).where(Employee.company_id == company_id))


async def update_employee(employee_id: int, full_name: str, age: int, phone: str, bank: str):
    async with async_session() as session:
        await session.execute(
            update(Employee).where(Employee.id == employee_id).values(full_name=full_name, age=age, phone=phone,
                                                                      bank=bank))
        await session.commit()


async def set_employee(telegram_id: int, company_id: int, start_date_work: str):
    async with async_session() as session:
        employee = await get_employee(
            telegram_id=telegram_id,
            company_id=company_id
        )

        if not employee:
            session.add(
                Employee(
                    telegram_id=telegram_id,
                    company_id=company_id,
                    start_date_work=start_date_work,
                    full_name="",
                    age=0,
                    phone="",
                    bank=""
                )
            )
            await session.commit()
            return await session.scalar(
                select(Employee).where(
                    Employee.telegram_id == telegram_id,
                    Employee.company_id == company_id,
                    Employee.start_date_work == start_date_work,
                )
            )
        else:
            return -1


async def delete_employee(employee_id: int, company_id: int):
    async with async_session() as session:
        await session.execute(delete(Employee).where(
            Employee.id == employee_id,
            Employee.company_id == company_id
        )
        )
        await session.commit()


async def delete_all_employee(company_id: int):
    async with async_session() as session:
        await session.execute(delete(Employee).where(
            Employee.company_id == company_id
        )
        )
        await session.commit()


async def get_shift(date: str):
    async with async_session() as session:
        return await session.scalar(
            select(Shifts)
            .where(Shifts.date == date)
        )


async def take_shift(company_id: int, employee_id: int, date: str, hours: int):
    async with async_session() as session:
        if not await get_shift(date=date):
            session.add(
                Shifts(
                    company_id=company_id,
                    employee_id=employee_id,
                    date=date,
                    hours=hours
                )
            )
            await session.commit()


async def ask_replacement_shift(support_employee: int, support_hours: int, main_hours: int, date: str):
    async with async_session() as session:
        shift = await get_shift(date=date)

        if shift.support_employee != "":
            await session.execute(
                update(Shifts)
                .where(
                    Shifts.date == shift.date
                )
                .values(
                    support_employee=support_employee,
                    support_hours=support_hours,
                    hours=main_hours
                )
            )
            await session.commit()


async def hours_period(start_date: str, end_date: str, employee_id: int):
    async with async_session() as session:
        main_hours = await session.scalars(
            select(coalesce(func.sum(Shifts.hours), 0)).select_from(Shifts).where(
                Shifts.employee_id == employee_id,
                Shifts.date > start_date,
                Shifts.date <= end_date
            )
        )

        support_hours = await session.scalars(
            select(coalesce(func.sum(Shifts.support_hours), 0)).select_from(Shifts).where(
                Shifts.support_employee == employee_id,
                Shifts.date > start_date,
                Shifts.date <= end_date
            )
        )
        return (0 if main_hours == 0 else main_hours.all()[0]) + (0 if support_hours == 0 else support_hours.all()[0])


async def salary_calculation(company_id: int, count_hours: int):
    shift_configuration = await get_shift_config(
        company_id=company_id
    )
    if shift_configuration:
        return count_hours * shift_configuration.payment_per_hour
    else:
        return 0


async def get_payouts(employee_id: int):
    async with async_session() as session:
        return await session.scalars(
            select(Payments)
            .where(
                Payments.employee_id == employee_id
            )
        )


async def create_payout(employee_id: int, company_id: int, pay_sum: float):
    async with async_session() as session:
        session.add(
            Payments(
                company_id=company_id,
                employee_id=employee_id,
                sum=pay_sum,
                date=datetime.today()
            )
        )
        await session.commit()
