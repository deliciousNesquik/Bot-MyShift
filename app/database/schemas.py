from sqlalchemy import BigInteger, ForeignKey, String, Integer, Float, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.database.models import Base


class Company(Base):
    """Таблица для хранения всех компаний"""
    __tablename__: str = 'company'

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(100))
    company_address: Mapped[str] = mapped_column(String(100))
    company_type_of_activity: Mapped[str] = mapped_column(String(100))
    tg_id = mapped_column(BigInteger)
    company_manager_name: Mapped[str] = mapped_column(String(150))
    company_manager_phone: Mapped[str] = mapped_column(String(11))
    company_manager_post: Mapped[str] = mapped_column(String(100))


class CompanyShiftConfiguration(Base):
    """Таблица для хранения данных о компании"""

    __tablename__: str = 'company_shift_configurations'

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company_chart: Mapped[str] = mapped_column(String(20))
    company_chart_time: Mapped[str] = mapped_column(String(11))
    start_date_shift: Mapped[int] = mapped_column(Integer)
    end_date_shift: Mapped[int] = mapped_column(Integer)
    number_of_hours_per_shift: Mapped[float] = mapped_column(Float)
    payment_per_hour: Mapped[int] = mapped_column(Float)
    payment_for_over_fulfillment: Mapped[bool] = mapped_column(Boolean)
    premium: Mapped[bool] = mapped_column(Boolean)


class Employee(Base):
    """Таблица для хранения всех сотрудников компаний"""
    __tablename__: str = 'employee'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    start_date_work: Mapped[str] = mapped_column(String(10))

    full_name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)
    phone: Mapped[str] = mapped_column(String(11))
    bank: Mapped[str] = mapped_column(String(20))


class Shifts(Base):
    """Таблица для хранения всех смен всех компаний"""
    __tablename__: str = 'shifts'

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    date: Mapped[str] = mapped_column(String)
    hours: Mapped[int] = mapped_column(Integer)
    support_employee: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    support_hours: Mapped[int] = mapped_column(Integer)
    start_shift_time: Mapped[str] = mapped_column(String)
    end_shift_time: Mapped[str] = mapped_column(String)


class Payments(Base):
    """Таблица для хранения всех выплат всем сотрудникам всех компаний"""
    __tablename__: str = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    sum: Mapped[float] = mapped_column(Float)
    date: Mapped[str] = mapped_column(Date)
