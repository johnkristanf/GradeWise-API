import json
from openai import OpenAI
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from src.grade.models import CriterionEssayGrade, OverAllEssayGrade
from src.config import settings

openai_client = OpenAI(api_key=settings.OPEN_AI_API_KEY)


class GradeService:
    def __init__(self):
        self.llm_prompts = LLMPrompts()

    async def async_create_and_load_overall_essay_grade(
        self, essay_id: int, overall_results: dict, session: AsyncSession
    ) -> OverAllEssayGrade:
        overall_essay_grade = OverAllEssayGrade(
            essay_id=essay_id,
            feedback=overall_results.get("overall_feedback", ""),
            suggestion=overall_results.get("overall_suggestion", ""),
            total_score=overall_results.get("total_score", 0),
            total_max_score=overall_results.get("total_max_score", 0),
        )
        session.add(overall_essay_grade)
        await session.commit()
        await session.refresh(overall_essay_grade)
        return overall_essay_grade
    
    
    def sync_create_and_load_overall_essay_grade(
        self, essay_id: int, overall_results: dict, session: Session
    ) -> OverAllEssayGrade:
        overall_essay_grade = OverAllEssayGrade(
            essay_id=essay_id,
            feedback=overall_results.get("overall_feedback", ""),
            suggestion=overall_results.get("overall_suggestion", ""),
            total_score=overall_results.get("total_score", 0),
            total_max_score=overall_results.get("total_max_score", 0),
        )
        session.add(overall_essay_grade)
        session.commit()
        session.refresh(overall_essay_grade)
        return overall_essay_grade

    async def async_create_and_load_criterion_essay_grade(
        self,
        overall_grade_id: int,
        criterion_grade_results: dict,
        session: AsyncSession,
    ):
        criterion_essay_grade = CriterionEssayGrade(
            overall_grade_id=overall_grade_id,
            title=criterion_grade_results.get("criterion", ""),
            score=criterion_grade_results.get("score", 0),
            feedback=criterion_grade_results.get("feedback", ""),
            suggestion=criterion_grade_results.get("suggestion", ""),
        )
        session.add(criterion_essay_grade)
        await session.commit()
        await session.refresh(criterion_essay_grade)
        return criterion_essay_grade
    
    def sync_create_and_load_criterion_essay_grade(
        self,
        overall_grade_id: int,
        criterion_grade_results: dict,
        session: Session,
    ):
        criterion_essay_grade = CriterionEssayGrade(
            overall_grade_id=overall_grade_id,
            title=criterion_grade_results.get("criterion", ""),
            score=criterion_grade_results.get("score", 0),
            feedback=criterion_grade_results.get("feedback", ""),
            suggestion=criterion_grade_results.get("suggestion", ""),
        )
        session.add(criterion_essay_grade)
        session.commit()
        session.refresh(criterion_essay_grade)
        return criterion_essay_grade

    def grade_essay(self, essay_text: str, rubric_data: dict):
        system_prompt = self.llm_prompts.system_essay_grading(
            rubric_data.get("essay_type", "General"),
            rubric_data.get("grade_level", "High School"),
            rubric_data.get("grade_intensity", "Moderate"),
        )
        user_prompt = self.llm_prompts.user_essay_grading(
            essay_text, rubric_data.get("criterion", [])
        )

        try:
            response = openai_client.responses.create(
                model="gpt-4o-mini",
                input=[system_prompt, user_prompt],
                temperature=0.2,
            )
            serialized_content = self._serialize_llm_content(response.output_text)
            return serialized_content
        except Exception as e:
            print(f"LLM grading error: {e}")
            return None

    def _serialize_llm_content(self, content):
        try:
            return json.loads(content)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Failed to serialize LLM content: {e}")
            return None


class LLMPrompts:
    def system_essay_grading(self, essay_type, grade_level, grade_intensity):
        return {
            "role": "system",
            "content": (
                f"You are a professional academic essay grader. Your task is to evaluate an essay "
                f"written at a **{grade_level}** level, focusing on **{essay_type}** style "
                f"essay characteristics, with a **{grade_intensity}** grading intensity. "
                "You will be given the essay and a grading rubric in JSON format.\n"
                """
                **Your Tasks**:
                    1. The essay may come from OCR (scanned image). First, clean up formatting and minor grammar issues, such as:
                        - Fix strange line breaks and misused punctuation.
                        - Correct common OCR mistakes (e.g., 'bo' → 'to', 'esources' → 'resources').
                        - Make the essay more readable without changing the student’s tone or intent.
                        - Do NOT rewrite or over-edit. Only correct what's needed for clarity.
            
                    2. For **each criterion** in the provided rubric, select the performance level that best reflects the quality of the essay, considering the specified grade level and essay type.
                    
                    3. Extract and return for each criterion:
                        - The `criterion` title.
                        - The selected performance level's `label`.
                        - The assigned `score`.
                        - The `max_score` possible for that criterion (use the highest score from that criterion’s performance_levels).
                        
                        - A clear `feedback` explaining why the score was assigned.
                            **Be specific. Quote or reference exact words, phrases, or sentences from the essay that influenced your decision, always keeping the defined grade level and essay type in mind.**
                            **Keep the 'reason' concise, ideally 2-3 sentences or around 70 words.**
                        
                        - A helpful `suggestion` to improve that specific aspect.
                            **Keep the 'suggestion' brief, ideally 2-3 sentences or around 50 words.**
                        
                    4. After evaluating all criteria, compute the **overall total score** out of the **maximum possible score**, like `12 / 20`.
                    
                    5. Provide an `overall_feedback` summary that reflects the essay's strengths and areas for improvement across all criteria, aligning with the **{grade_level}** expectations and **{essay_type}** conventions.
                    
                    6. Provide an `overall_suggestion` summary that reflects the area of improvement, across all criteria.
                    
                    7. Return the final essay text that is used in the grading.
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
                        "criterion_grade_results": [
                            {{
                                "criterion": "Thesis & Focus",
                                "matched_label": "Good",
                                "score": 3,
                                "max_score": 4,
                                "feedback": "The thesis is clear but lacks deeper insight.",
                                "suggestion": "Refine the thesis to be more specific and analytical."
                            }},
                            ...
                        ],
                        "final_essay_text": "Today, technology plays a vital role in education. It allows students to access information easily and learn new skills. For example, using computers in the classroom helps develop research abilities and critical thinking. While there are challenges, like distractions, the benefits of technology in learning are clear. By using these tools wisely, students can become more prepared for the future.",
                        "total_score": 12,
                        "total_max_score": 20,
                        "overall_feedback": "Your essay demonstrates a clear understanding of the topic and is generally well-organized. The arguments are supported with relevant examples, and your writing is mostly clear and effective. However, the thesis could be made more specific, and some transitions between paragraphs would strengthen the overall flow. Keep working on refining your main point and connecting your ideas for greater impact."
                        "overall_suggestion": "Focus on clarifying and specifying your thesis, and work on improving transitions between paragraphs to create a smoother flow. Aim to provide deeper analysis where appropriate, and ensure each main point is clearly connected to your thesis for greater overall coherence."
                    }}
                """,
        }
