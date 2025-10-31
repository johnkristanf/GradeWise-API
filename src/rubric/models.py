from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Rubric(SQLModel, table=True):
    __tablename__ = "rubric"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    student_level: str
    grade_intensity: str
    language: str
    essay_type: str

    criterion: List["Criterion"] = Relationship(back_populates="rubric")
    performance_levels: List["PerformanceLevel"] = Relationship(back_populates="rubric")


class Criterion(SQLModel, table=True):
    __tablename__ = "criterion"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    rubric_id: int = Field(foreign_key="rubric.id")

    rubric: Optional["Rubric"] = Relationship(back_populates="criterion")
    descriptors: List["CriterionLevelDescriptor"] = Relationship(back_populates="criterion")


class PerformanceLevel(SQLModel, table=True):
    __tablename__ = "performance_level"

    id: Optional[int] = Field(default=None, primary_key=True)
    label: str
    score: int
    rubric_id: int = Field(foreign_key="rubric.id")

    rubric: Optional["Rubric"] = Relationship(back_populates="performance_levels")
    descriptors: List["CriterionLevelDescriptor"] = Relationship(back_populates="performance_levels")


class CriterionLevelDescriptor(SQLModel, table=True):
    __tablename__ = "criterion_level_descriptor"

    criterion_id: int = Field(foreign_key="criterion.id", primary_key=True)
    level_id: int = Field(foreign_key="performance_level.id", primary_key=True)
    descriptor: str

    criterion: Optional["Criterion"] = Relationship(back_populates="descriptors")
    performance_levels: Optional["PerformanceLevel"] = Relationship(back_populates="descriptors")
