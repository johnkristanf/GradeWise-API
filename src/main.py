from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rubric.router import rubric_router
from src.essay.router import essay_router
from src.user.router import user_router
from src.auth.router import auth_router

from src.config import settings
from src.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Establish database connection on startup
    await Database.initialize()

    # Close the database connection on shutdown
    yield
    await Database.close_all()


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,  # <-- Pass the class, not an instance
    allow_origins=settings.CLIENT_ORIGIN_URLS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(essay_router, prefix="/essay", tags=["Essay"])
app.include_router(rubric_router, prefix="/rubric", tags=["Rubric"])


@app.get("/health")
def check_server_health():
    return {"message": "Server is Healthy"}
