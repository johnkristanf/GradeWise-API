from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel



class Classes(SQLModel, table=True):
    __tablename__ = "classes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    
    assignments: Optional["Assignments"] = Relationship(back_populates="classes")


class Assignments(SQLModel, table=True):
    __tablename__ = "assignments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    
    class_id: int = Field(foreign_key="classes.id")
    classes: Optional[Classes] = Relationship(back_populates="assignments")
    essay: Optional["Essay"] = Relationship(back_populates="assignments")
    

class Essay(SQLModel, table=True):
    __tablename__ = "essay"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str
    graded_at: Optional[datetime] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    assignment_id: int = Field(foreign_key="assignments.id")
    
    overall_essay_grade: Optional["OverAllEssayGrade"] = Relationship(back_populates="essay")
    assignments: Optional[Assignments] = Relationship(back_populates="essay")


class OverAllEssayGrade(SQLModel, table=True):
    __tablename__ = "overall_essay_grade"

    id: Optional[int] = Field(default=None, primary_key=True)
    feedback: str
    suggestion: str
    max_score: int

    essay_id: int = Field(foreign_key="essay.id")
    
    essay: Optional[Essay] = Relationship(back_populates="overall_essay_grade")
    criterion_essay_grade: Optional["CriterionEssayGrade"] = Relationship(back_populates="overall_essay_grade")


class CriterionEssayGrade(SQLModel, table=True):
    __tablename__ = "criterion_essay_grade"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    score: int
    feedback: str
    suggestion: str

    overall_grade_id: int = Field(foreign_key="overall_essay_grade.id")
    overall_essay_grade: Optional[OverAllEssayGrade] = Relationship(back_populates="criterion_essay_grade")
