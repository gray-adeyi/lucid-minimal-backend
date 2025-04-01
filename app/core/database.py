from collections.abc import AsyncGenerator

from app.core.config import settings

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import BaseDBModel

DATABASE_URL = f"mysql+asyncmy://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}/{settings.MYSQL_DATABASE}"

database_engine = AsyncEngine(create_engine(DATABASE_URL))


async def initialize_database(engine: AsyncEngine, drop_all_first: bool = False):
    """Creates all tables in the database using SQLAlchemy metadata"""
    async with database_engine.begin() as conn:
        if drop_all_first:
            await conn.run_sync(BaseDBModel.metadata.drop_all)
        await conn.run_sync(BaseDBModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Provides a database session"""
    async_session = sessionmaker(
        database_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        session: AsyncSession
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            print("closing db connection")
            await session.close()
