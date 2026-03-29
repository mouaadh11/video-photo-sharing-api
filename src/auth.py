from dotenv import load_dotenv
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
import os
load_dotenv()
SECRET = os.getenv("JWT_SECRET")


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

