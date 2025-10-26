from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from .schemas import FetchUser, RegisterUser
from .service import AuthService

from ..database import Database

auth_service = AuthService()
auth_router = APIRouter()


@auth_router.post("/register", response_model=FetchUser, status_code=201)
async def register(
    user: RegisterUser, session: AsyncSession = Depends(Database.get_session)
):
    registered_user = await auth_service.register(user, session)
    return registered_user


@auth_router.post("/login", status_code=200)
def login(user_credentials):
    authenticated_user = auth_service.login(
        user_credentials.email, user_credentials.password
    )
    return authenticated_user
