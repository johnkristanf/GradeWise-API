from src.enums import EssayStatus
from src.celery import app
from src.database import Database
from src.essay.service import EssayService
from src.rubric.service import RubricService
from src.grade.service import GradeService

essay_service = EssayService()
rubric_service = RubricService()
grade_service = GradeService()


# MAKE THIS TASK TO SUPPORT SYNC PROCESS CAUSE CELERY IS BUILT TO EXECUTE SYNCHRONOUSLY
@app.task(max_retries=3, default_retry_delay=60)
def process_essay_grading(essay_id: int, rubric_id: int, image_content: str):

    with Database.get_sync_session() as sync_session:
        extracted_text = essay_service.extract_text_from_image(image_content)

        rubric_data = rubric_service.sync_get_rubric_by_id(rubric_id, sync_session)

        grade_results = grade_service.grade_essay(extracted_text, rubric_data.model_dump())

        criterion_grade_results = grade_results.get("criterion_grade_results", [])
        overall_results = {
            "overall_feedback": grade_results.get("overall_feedback", ""),
            "overall_suggestion": grade_results.get("overall_suggestion", ""),
            "total_score": grade_results.get("total_score", 0),
            "total_max_score": grade_results.get("total_max_score", 0),
        }

        overall_essay_grade = grade_service.sync_create_and_load_overall_essay_grade(
            essay_id, overall_results, sync_session
        )

        for results in criterion_grade_results:
            grade_service.sync_create_and_load_criterion_essay_grade(
                overall_essay_grade.id, results, sync_session
            )

        essay_service.sync_update_essay_status(
            essay_id, EssayStatus.READY_FOR_REVIEW, sync_session
        )
