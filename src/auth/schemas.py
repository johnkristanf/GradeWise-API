from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    """Base fields shared across schemas"""
    first_name: str = Field(min_length=1, max_length=50)
    middle_name: Optional[str] = Field(default=None, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: str = Field(
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    )


class RegisterUser(UserBase):
    password: str = Field(min_length=8, max_length=100)


class LoginUser(SQLModel):
    email: str = Field(
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    )
    password: str = Field(min_length=8, max_length=100)

    # This drops the fields inside the request body that are not set in the schema
    class Config:
        extra = "ignore"


class FetchUser(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
