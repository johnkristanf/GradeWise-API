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
    async def initialize(cls):
        """Initialize both raw SQL pool and ORM engine"""
        await cls.create_pool()
        cls.create_session()

    @classmethod
    async def create_pool(cls):
        cls.pool = await aiomysql.create_pool(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB_DATABASE,
            minsize=5,
            maxsize=10,
        )

    @classmethod
    def create_session(cls):
        
        # Initialize SQLAlchemy async engine for ORM
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
    @asynccontextmanager
    async def get_cursor(cls):
        async with cls.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                yield cursor, conn

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        """
        Get SQLAlchemy session with automatic commit/rollback and error handling
        """
        async with cls.async_session_maker() as session:
            try:
                yield session
                await session.commit()  # Auto-commit on success
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()

    # CLOSE METHODS SECTION
    @classmethod
    async def close_pool(cls):
        if cls.pool:
            cls.pool.close()
            await cls.pool.wait_closed()

    @classmethod
    async def close_engine(cls):
        """Close ORM engine"""
        if cls.engine:
            await cls.engine.dispose()

    @classmethod
    async def close_all(cls):
        """Close both pool and engine"""
        await cls.close_pool()
        await cls.close_engine()



