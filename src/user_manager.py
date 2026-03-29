import os
from dotenv import load_dotenv
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import BaseUserManager, UUIDIDMixin
import uuid
from src.db import User, get_user_db

load_dotenv()
SECRET = os.getenv("JWT_SECRET")

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)