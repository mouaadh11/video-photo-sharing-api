from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Text,  DateTime, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


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