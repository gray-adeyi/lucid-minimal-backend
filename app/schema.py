from datetime import timedelta, datetime
from typing import Annotated, Callable, Self

from fastapi import Depends
from jose import jwt
from pydantic import BaseModel, EmailStr, model_validator

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
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("password mismatch, please try again")
        return self


class SignInSchema(BaseModel):
    email: EmailStr
    password: str
