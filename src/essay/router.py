from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from sqlalchemy.ext.asyncio.session import AsyncSession


from src.rubric.dependencies import get_rubric_service
from src.rubric.service import RubricService
from src.essay.dependencies import get_essay_service
from src.essay.service import EssayService
from src.database import Database
from src.tasks.essay import process_essay_grading


essay_router = APIRouter()


@essay_router.post("/grade", status_code=200)
async def grade(
    assignment_id: int = Form(...),
    rubric_id: int = Form(...),
    files: List[UploadFile] = File(...),
    essay_service: EssayService = Depends(get_essay_service),
    rubric_service: RubricService = Depends(get_rubric_service),
    session: AsyncSession = Depends(Database.get_session),
):
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No file uploaded")

    for file in files:
        image_content = await file.read()
        filename = file.filename

        essay = await essay_service.create_and_load_essay(
            filename, assignment_id, session
        )

        # METHODS TO PUT INSIDE A CELERY TASK
        # extracted_text = essay_service.extract_text_from_image(image_content)

        rubric_data = await rubric_service.get_rubric_by_id(rubric_id, session)

        llm_grade_results = essay_service.llm_grade_essay(
            "extracted_text", rubric_data.model_dump()
        )
        
        # Save the grade results to database
        
        
        # Update the Essay status using on the given id
        
        
        # Finally, put this whole process in the celery task for queuing implementation

    return {
        "success": True,
        "message": "Essay Submitted Successfully",
        "rubric_data": rubric_data.model_dump(),
    }
