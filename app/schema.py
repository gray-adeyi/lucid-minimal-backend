from datetime import timedelta, datetime
from typing import Annotated, Callable, Self
from uuid import UUID

from fastapi import Depends
from jose import jwt
from pydantic import BaseModel, EmailStr, model_validator, Field

from app.core.config import settings
from app.models import User


class ResponseSchema[T](BaseModel):
    detail: str | None = None
    data: T | None = None


class TokenSchema(BaseModel):
    token_type: str = "bearer"
    access_token: str
    refresh_token: str

    @staticmethod
    def create_jwt_token(data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        # Note that this timezone is naive for  simplicity
        to_encode["exp"] = datetime.now() + expires_delta
        return jwt.encode(
            to_encode,
            settings.JWT_PRIVATE_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @classmethod
    def generate_tokens(cls, get_user_fn: Callable) -> Callable:
        def inner(user: Annotated[User, Depends(get_user_fn)]) -> TokenSchema:
            data = {"sub": str(user.id)}
            # Create access token
            access_token = cls.create_jwt_token(
                data,
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN),
            )

            # Create refresh token
            refresh_token = cls.create_jwt_token(
                data,
                expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN),
            )
            return TokenSchema(access_token=access_token, refresh_token=refresh_token)

        return inner


class SignUpSchema(BaseModel):
    email: EmailStr = Field(
        description="The email address of the user",
        examples=["johndoe@example.com", "adeyigbenga005@gmail.com"],
    )
    password: str = Field(description="Password", examples=["password123"])
    confirm_password: str = Field(
        description="Confirm password, must match password", examples=["password123"]
    )

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("password mismatch, please try again")
        return self


class CreatePostSchema(BaseModel):
    text: str = Field(
        description="The content of the post",
        examples=["Beautiful is better than ugly.", "Explicit is better than implicit"],
    )


class PostSchema(CreatePostSchema):
    id: UUID
    text: str


class PostDetailSchema(PostSchema):
    author_id: UUID
    created_at: datetime
    updated_at: datetime | None
