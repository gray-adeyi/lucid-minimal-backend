from typing import Annotated
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from app import crud
from app.core.config import settings
from app.core.database import get_session
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import verify_password
from app.models import User
from app.schema import SignUpSchema
from jose import jwt, JWTError

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_from_form_data(
    *,
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> User:
    user = await crud.get_user_by_email(session=session, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with email address {form_data.username} does not exist",
        )
    password_is_valid = verify_password(
        password=form_data.password,
        hashed_password=user.password,
        password_context=settings.PASSWORD_CONTEXT,
    )
    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect password, try again",
        )
    return user


async def create_user_from_signup(*, session: SessionDep, body: SignUpSchema) -> User:
    try:
        return await crud.create_user(session=session, data=body)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with this email already exist",
        )


async def get_user_from_access_token(
    *,
    session: SessionDep,
    token: Annotated[str, Depends(settings.OAUTH2_SCHEME)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_PRIVATE_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = UUID(user_id_str)
    except JWTError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await crud.get_user_by_id(session=session, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user


AuthenticatedUserDep = Annotated[User, Depends(get_user_from_access_token)]
