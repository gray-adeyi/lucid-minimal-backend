from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.core.config import settings
from app.core.security import hash_password
from app.models import User
from app.schema import SignUpSchema
from pydantic import EmailStr
from sqlalchemy import select


async def create_user(*, session: AsyncSession, data: SignUpSchema) -> User:
    hashed_password = hash_password(
        password=data.password, password_context=settings.PASSWORD_CONTEXT
    )
    new_user = User(email=data.email, password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_email(*, session: AsyncSession, email: EmailStr) -> User | None:
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_id(*, session: AsyncSession, id: UUID) -> User | None:
    query = select(User).where(User.id == id)
    result = await session.execute(query)
    return result.scalar_one_or_none()
