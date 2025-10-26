from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user
from src.user.models import User

user_router = APIRouter()


@user_router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
