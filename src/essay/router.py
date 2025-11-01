from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.essay.dependencies import get_essay_service
from src.essay.service import EssayService
from src.database import Database
from src.grade.tasks import process_essay_grading

essay_router = APIRouter()


@essay_router.post("/grade", status_code=200)
async def grade(
    assignment_id: int = Form(...),
    rubric_id: int = Form(...),
    files: List[UploadFile] = File(...),
    essay_service: EssayService = Depends(get_essay_service),
    session: AsyncSession = Depends(Database.get_async_session),
):
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No file uploaded")

    for file in files:
        image_content = await file.read()
        filename = file.filename

        essay = await essay_service.create_and_load_essay(
            filename, assignment_id, session
        )

        # Background task queue
        process_essay_grading.delay(essay.id, rubric_id, image_content)

    return {
        "success": True,
        "message": "Essay Submitted Successfully",
    }
