from datetime import datetime
import json

from google.cloud import vision
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import Session
from src.enums import EssayStatus
from src.essay.models import Essay


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

    async def async_update_essay_status(
        self, essay_id: int, status: EssayStatus, session: AsyncSession
    ):
        essay = await session.get(Essay, essay_id)
        essay.status = status
        essay.graded_at = datetime.now()
        session.add(essay)
        await session.commit()
        await session.refresh(essay)
        return essay
    
    
    def sync_update_essay_status(
        self, essay_id: int, status: EssayStatus, session: Session
    ):
        essay = session.get(Essay, essay_id)
        essay.status = status
        essay.graded_at = datetime.now()
        session.add(essay)
        session.commit()
        session.refresh(essay)
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
