from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from data.config import URL_DATABASE

async_engine = create_async_engine(url=URL_DATABASE)
async_session = async_sessionmaker(async_engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def async_main() -> object:
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
