from typing import AsyncGenerator
import aiomysql

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from contextlib import asynccontextmanager
from src.config import settings


class Database:
    # For raw SQL (aiomysql)
    pool = None

    # For ORM (SQLAlchemy async)
    engine = None
    async_session_maker = None

    # DATABASE INITIALIZATION SECTION
    @classmethod
    def initialize(cls):
        cls.create_session()

    @classmethod
    def create_session(cls):
        database_url = f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"

        cls.engine = create_async_engine(
            database_url,
            echo=False,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,  # Verify connections before using
        )

        cls.async_session_maker = sessionmaker(
            cls.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    # GET CONNECTION SECTION
    @classmethod
    async def get_session(
        cls,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with cls.async_session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    # CLOSE METHODS SECTION
    @classmethod
    async def close(cls):
        """Close ORM engine"""
        if cls.engine:
            await cls.engine.dispose()