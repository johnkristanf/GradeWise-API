from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.rubric.dependencies import get_rubric_service
from src.rubric.service import RubricService
from src.database import Database
from src.rubric.schemas import RubricIn

rubric_router = APIRouter()

@rubric_router.post("/create", status_code=201)
async def create(
    rubricData: RubricIn,
    session: AsyncSession = Depends(Database.get_session),
    rubric_service: RubricService = Depends(get_rubric_service),
):
    rubric = await rubric_service.create_rubric(rubricData.model_dump(), session)
    return rubric
