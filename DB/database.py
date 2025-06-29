import pathlib

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

path = pathlib.Path(r"DB\user.db").resolve()

async_engine = create_async_engine(url=rf"sqlite+aiosqlite:///{path}", echo=True)
async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
