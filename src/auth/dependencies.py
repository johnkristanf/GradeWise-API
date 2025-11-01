from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.schemas import FetchUser
from src.config import settings

from src.auth.service import JWTService

from src.user.models import User

from src.database import Database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

jwt_service = JWTService(
    secret_key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(Database.get_async_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt_service.decode_token(token)
        user_id: int = payload.get("sub")
        
        user = await session.get(User, user_id)
        if not user:
            raise credentials_exception

        return FetchUser.model_validate(user)
    except JWTError:
        raise credentials_exception
