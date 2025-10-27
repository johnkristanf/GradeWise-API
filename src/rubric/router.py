from fastapi import APIRouter
from openai import OpenAI


rubric_router = APIRouter()


@rubric_router.post("/create", status_code=201)
async def create():
    return
