from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from ..config import settings

from .schemas import FetchUser, LoginUser, RegisterUser
from .service import AuthService, JWTService

from ..database import Database

auth_router = APIRouter()

jwt_service = JWTService(
    secret_key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
)
auth_service = AuthService(jwt_service=jwt_service)


@auth_router.post("/register", response_model=FetchUser, status_code=201)
async def register(
    user: RegisterUser, session: AsyncSession = Depends(Database.get_session)
):
    registered_user = await auth_service.register(user, session)
    return registered_user


@auth_router.post("/login", status_code=200)
async def login(user: LoginUser, session: AsyncSession = Depends(Database.get_session)):
    return await auth_service.login(user.email, user.password, session)
