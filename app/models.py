# models.py
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, declared_attr
from sqlalchemy.sql import func


class Base:
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


BaseDBModel = declarative_base(cls=Base)


class User(BaseDBModel):
    __tablename__ = "users"

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Relationship
    posts = relationship("Post", back_populates="author")


class Post(BaseDBModel):
    __tablename__ = "posts"

    author_id = Column(String(36), ForeignKey("users.id"))
    text = Column(String(1000), nullable=False)

    author = relationship("User", back_populates="posts")
