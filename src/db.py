from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text,  DateTime, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

# DATABASE_URL= "sqlite+aiosqlite:///./test.db"
DATABASE_URL= os.getenv("DATABASE_URL")


#Create a model
Base = declarative_base()

class User(SQLAlchemyBaseUserTableUUID, Base):
    # __tablename__ = "users"

    # id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # email = Column(String, unique=True)
    # password = Column(String)

     # 🔗 relationship
    posts = relationship("Post", back_populates="user", cascade="all, delete")

class Post(Base):
    __tablename__= "posts"

    id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_id= Column(String, nullable=None)
    file_type = Column(String,nullable=False )
    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔑 Foreign key
    user_id = Column(UUID, ForeignKey("user.id"))

    # 🔗 relationship
    user = relationship("User", back_populates="posts")

# DB adapter





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
