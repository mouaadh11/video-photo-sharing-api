from collections.abc import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.dialects.postgresql import UUID
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.models import Base, User


load_dotenv()

# DATABASE_URL= "sqlite+aiosqlite:///./test.db"
DATABASE_URL= os.getenv("DATABASE_URL")


#Database connection
engine = create_async_engine(DATABASE_URL, echo = 
                             True)
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() ->AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
