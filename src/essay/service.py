from google.cloud import vision
from openai import OpenAI
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.config import settings
from src.rubric.models import Rubric
from src.enums import EssayStatus
from src.essay.models import Essay


openai_client = OpenAI(api_key=settings.OPEN_AI_API_KEY)
vision_client = vision.ImageAnnotatorClient()


class EssayService:
    async def create_and_load_essay(
        self, filename: str, assignment_id: int, session: AsyncSession
    ) -> Essay:
        essay = Essay(
            name=filename, status=EssayStatus.GRADING, assignment_id=assignment_id
        )
        session.add(essay)
        await session.commit()
        await session.refresh(essay)

        return essay

    def extract_text_from_image(self, image_content: bytes) -> str | None:
        image = vision.Image(content=image_content)
        response = vision_client.document_text_detection(image=image)

        if response.error and response.error.message:
            print(f"Vision API Error: {response.error.message}")

        if response.full_text_annotation and response.full_text_annotation.text:
            text = response.full_text_annotation.text
            return text

        return None

    def llm_grade_essay(self, essay_text: str, rubric_data: dict):
        print("essay_text inside llm_grade_essay: ", essay_text)
        print("rubric_data: ", rubric_data)
        return


class LLMPrompts:

    def system_essay_grading(self, essay_type, grade_level, grade_intensity):
        return {
            "role": "system",
            "content": (
                f"You are a professional academic essay grader. Your task is to evaluate an essay "
                f"Written at a **{grade_level}** level, focusing on **{essay_type}** style "
                f"Essay characteristics, with a **{grade_intensity}** grading intensity. "
                "You will be given the essay and a grading rubric in JSON format.\n"
                """
                **Your Tasks**:
                    1. The essay may come from OCR (scanned image). First, clean up formatting and minor grammar issues, such as:
                        - Fix strange line breaks and misused punctuation.
                        - Correct common OCR mistakes (e.g., 'bo' → 'to', 'esources' → 'resources').
                        - Make the essay more readable without changing the student’s tone or intent.
                        - Do NOT rewrite or over-edit. Only correct what's needed for clarity.
            
                    2. For **each criterion** in the provided rubric, select the performance level that best reflects the quality of the essay, considering the specified grade level and essay category.
                    
                    3. Extract and return for each criterion:
                        - The `criterion` title.
                        - The selected performance level's `label`.
                        - The assigned `score`.
                        - The `max_score` possible for that criterion (use the highest score from that criterion’s levels).
                        
                        - A clear `reason` explaining why the score was assigned.
                            **Be specific. Quote or reference exact words, phrases, or sentences from the essay that influenced your decision, always keeping the defined grade level and essay type in mind.**
                            **Keep the 'reason' concise, ideally 2-3 sentences or around 70 words.**
                        
                        - A helpful `suggestion` to improve that specific aspect.
                            **Keep the 'suggestion' brief, ideally 2-3 sentences or around 50 words.**
                        
                    4. After evaluating all criteria, compute the **overall total score** out of the **maximum possible score**, like `12 / 20`.
                    
                    5. Provide an `overall_feedback` summary that reflects the essay's strengths and areas for improvement across all criteria, aligning with the **{grade_level}** expectations and **{essay_type}** conventions.
                """
            ),
        }

    def user_essay_grading(self, essay: str, rubric_criteria: str):
        return {
            "role": "user",
            "content": f"""
                    Essay:
                    \"\"\"
                    {essay}
                    \"\"\"

                    Rubric Criteria (JSON):
                    {rubric_criteria}

                    "Return only a valid JSON object in the format below — do not include any explanation, markdown, or commentary:"
                    {{
                        "evaluations": [
                            {{
                                "criterion": "Thesis & Focus",
                                "matched_label": "Good",
                                "score": 3,
                                "max_score": 4,
                                "reason": "The thesis is clear but lacks deeper insight.",
                                "suggestion": "Refine the thesis to be more specific and analytical."
                            }},
                            ...
                        ],
                        
                        "total_score": 12,
                        "max_total_score": 20,
                        "overall_feedback": "The essay is generally well-organized and grammatically sound but could benefit from a sharper thesis and improved transitions."
                    }}
                """,
        }
