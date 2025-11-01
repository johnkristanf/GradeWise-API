import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.rubric.router import rubric_router
from src.essay.router import essay_router
from src.user.router import user_router
from src.auth.router import auth_router

from src.config import settings
from src.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Establish database connection on startup
    Database.create_async_session()

    # Close the database connection on shutdown
    yield
    await Database.close_async()


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CLIENT_ORIGIN_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API versioning: wrap all routes in a versioned APIRouter with /api/v1
api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_v1_router.include_router(user_router, prefix="/user", tags=["User"])
api_v1_router.include_router(essay_router, prefix="/essay", tags=["Essay"])
api_v1_router.include_router(rubric_router, prefix="/rubric", tags=["Rubric"])


@api_v1_router.get("/health")
def check_server_health():
    return {"message": "Server is Healthy"}


app.include_router(api_v1_router)