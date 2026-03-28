from fastapi_users.db import SQLAlchemyUserDatabase
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, Security
from passlib.context import CryptContext
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users import BaseUserManager, UUIDIDMixin
import uuid

from src.db import User, get_user_db

SECRET = "Random"


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

from fastapi_users import FastAPIUsers
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
get_current_user = fastapi_users.current_user(active=True)
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(hours=1)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



# def hash_password(password: str):
#     print ("----hash-func----")
#     print("PASSWORD:", password)
#     print("LENGTH:", len(password))
#     print("TYPE:", type(password))
#     return pwd_context.hash(password)

# def verify_password(password: str, hashed: str):
#     return pwd_context.verify(password, hashed)