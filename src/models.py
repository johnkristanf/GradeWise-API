from datetime import datetime
from typing import Optional
from sqlmodel import Column, DateTime, Field, text


# class TimestampMixin:
#     created_at: Optional[datetime] = Field(
#         sa_column=Column(
#             DateTime(timezone=True),
#             nullable=False,
#             server_default=text("CURRENT_TIMESTAMP"),
#         )
#     )

#     updated_at: Optional[datetime] = Field(
#         sa_column=Column(
#             DateTime(timezone=True),
#             nullable=False,
#             server_default=text("CURRENT_TIMESTAMP"),
#             server_onupdate=text("CURRENT_TIMESTAMP"),
#         )
#     )