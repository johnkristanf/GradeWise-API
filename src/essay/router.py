import io

from typing import List
from fastapi import APIRouter, File, HTTPException, UploadFile
from openai import OpenAI
from src.config import settings
from google.cloud import vision

openai_client = OpenAI(api_key=settings.OPEN_AI_API_KEY)
vision_client = vision.ImageAnnotatorClient()

essay_router = APIRouter()


@essay_router.post("/grade", status_code=200)
async def grade(files: List[UploadFile] = File(...)):
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No file uploaded")

    for file in files:
        content = await file.read()
        image = vision.Image(content=content)
        response = vision_client.document_text_detection(image=image)

        if response.full_text_annotation:
            text = response.full_text_annotation.text
            print("Extracted Text:")
            print(text)

            response = openai_client.responses.create(
                model="gpt-4.1-mini",
                input="Write a one-sentence bedtime story about a unicorn.",
            )

    return
