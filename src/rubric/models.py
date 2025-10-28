from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from src.models import TimestampMixin


class Rubric(SQLModel, TimestampMixin, table=True):
    __tablename__ = "rubric"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    student_level: str
    grade_intensity: str
    language: str


class Criterion(SQLModel, TimestampMixin, table=True):
    __tablename__ = "criterion"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    rubric_id: int = Field(foreign_key="rubric.id")
    
    rubric: Optional[Rubric] = Relationship(back_populates="rubric")
    
    
class PerformanceLevel(SQLModel, TimestampMixin, table=True):
    __tablename__ = "performance_level"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    label: str
    score: int
    rubric_id: int = Field(foreign_key="rubric.id")
    
    rubric: Optional[Rubric] = Relationship(back_populates="rubric")


class CriterionLevelDescriptor(SQLModel, table=True):
    __tablename__ = "criterion_level_descriptor"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    criterion_id: Optional[int] = Field(
        default=None, foreign_key="criterion.id", primary_key=True
    )
    level_id: Optional[int] = Field(
        default=None, foreign_key="performance_level.id", primary_key=True
    )
    descriptor: str