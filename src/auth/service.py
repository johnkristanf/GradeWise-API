from pwdlib import PasswordHash
from sqlalchemy import select
from jose import JWTError, jwt

from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio.session import AsyncSession

from ..config import settings
from ..user.models import User
from .schemas import FetchUser, RegisterUser


class JWTService:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        expire = datetime.now() + (expires_delta or timedelta(minutes=15))

        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )


class AuthService:

    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service
        self.password_hash = PasswordHash.recommended()

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def hash_password(self, password):
        return self.password_hash.hash(password)

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

        return FetchUser.model_validate(registered_user)

    async def login(self, email: str, password: str, session: AsyncSession):
        user = await self.get_user_by_email(session, email)
        if not user or not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = self.jwt_service.create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=timedelta(minutes=settings.JWT_TOKEN_EXPIRES_MINUTES),
        )

        return {"message": "Login Successfully", "access_token": access_token}
