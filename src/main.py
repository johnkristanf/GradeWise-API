from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .auth.router import auth_router
from .database import Database


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

@app.get("/health")
def check_server_health():
    return {"message": "Server is Healthy"}
