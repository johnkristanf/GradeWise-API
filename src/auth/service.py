from typing import Optional
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from .models import User
from .schemas import FetchUser, RegisterUser
from ..database import Database

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def verify_password(self, plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)

    def hash_password(self, password):
        return password_hash.hash(password)

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def register(self, user: RegisterUser, session: AsyncSession):
        existing_user = await self.get_user_by_email(session, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address is already registered.",
            )
            
        hashed_password = self.hash_password(user.password)
        user_dict = user.model_dump(exclude={"password"})

        registered_user = User(**user_dict, password=hashed_password)

        session.add(registered_user)
        await session.commit()
        await session.refresh(registered_user)

        return FetchUser(
            id=registered_user.id,
            first_name=registered_user.first_name,
            middle_name=registered_user.middle_name,
            last_name=registered_user.last_name,
            email=registered_user.email,
            created_at=registered_user.created_at,
            updated_at=registered_user.updated_at,
        )

    async def login(self, email, password):
        async with Database.get_cursor() as (cursor, conn):
            await cursor.execute("SELECT * FROM users WHERE email = %s", (email))
            user = await cursor.fetchone()
        print("user: ", user)
        return user
