from typing import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from contextlib import contextmanager
from src.config import settings


class Database:
    # For raw SQL (aiomysql)
    pool = None

    # For ORM (SQLAlchemy async)
    engine = None
    async_session_maker = None

    # For ORM (SQLAlchemy sync)
    sync_engine = None
    sync_session_maker = None

    @classmethod
    def create_async_session(cls):
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

    @classmethod
    def create_sync_session(cls):
        sync_database_url = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"

        cls.sync_engine = create_engine(
            sync_database_url,
            echo=False,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )

        cls.sync_session_maker = sessionmaker(
            cls.sync_engine,
            class_=Session,
            expire_on_commit=False,
        )

    # GET CONNECTION SECTION
    @classmethod
    async def get_async_session(
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

    @classmethod
    @contextmanager
    def get_sync_session(cls) -> Generator[Session, None, None]:
        session = cls.sync_session_maker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # CLOSE METHODS SECTION
    @classmethod
    async def close_async(cls):
        """Close async ORM engine"""
        if cls.engine:
            await cls.engine.dispose()

    @classmethod
    def close_sync(cls):
        """Close sync ORM engine"""
        if cls.sync_engine:
            cls.sync_engine.dispose()