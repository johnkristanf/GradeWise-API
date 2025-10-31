from src.rubric.service import RubricService
from src.celery import celery_app
from src.database import Database
from src.essay.service import EssayService


@celery_app.task(max_retries=3, default_retry_delay=60)
async def process_essay_grading(essay_id: int, rubric_id: int, image_content: str):
    task = process_essay_grading.request
    async with Database.get_session() as session:
        essay_service = EssayService()
        rubric_service = RubricService()

        if hasattr(task, 'update_state'):
            task.update_state(state='PROCESSING', meta={'step': 'extracting_text'})
        extracted_text = essay_service.extract_text_from_image(image_content)
        
        if hasattr(task, 'update_state'):
            task.update_state(state='PROCESSING', meta={'step': 'fetching_rubric'})
        rubric_data = await rubric_service.get_rubric_by_id(rubric_id, session)

        if hasattr(task, 'update_state'):
            task.update_state(state='PROCESSING', meta={'step': 'grading'})
        llm_grade_results = essay_service.llm_grade_essay(extracted_text, rubric_data.model_dump_json())

        # Save LLM result to grade-related database tables
        
        # Update the essay status using the essay_id