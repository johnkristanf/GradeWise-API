from typing import List, Union
from fastapi import APIRouter, File, HTTPException, UploadFile
from openai import OpenAI
from ..config import settings

client = OpenAI()
essay_router = APIRouter()


@essay_router.post("/grade", status_code=200)
async def grade(files: List[UploadFile] = File(...)):
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    for file in files:
        content = await file.read()
        
    return
