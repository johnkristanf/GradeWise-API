from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DEBUG: bool = True
    APP_NAME: str = "GradeWise"

    # Security
    OPEN_AI_API_KEY: str
    HANDWRITING_OCR_API_TOKEN: str
    JWT_SECRET_KEY: str

    # Database
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str

    # CORS
    CLIENT_ORIGIN_URLS: List[str] = ["http://localhost:9000"]


settings = Settings()
