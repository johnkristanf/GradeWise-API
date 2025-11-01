from typing import Optional
from sqlmodel import Column, Field, Relationship, SQLModel, Text

class OverAllEssayGrade(SQLModel, table=True):
    __tablename__ = "overall_essay_grade"

    id: Optional[int] = Field(default=None, primary_key=True)
    feedback: str = Field(sa_column=Column(Text))
    suggestion: str = Field(sa_column=Column(Text))
    total_score: int
    total_max_score: int

    essay_id: int = Field(foreign_key="essay.id")

    essay: Optional["Essay"] = Relationship(back_populates="overall_essay_grade")
    criterion_essay_grade: Optional["CriterionEssayGrade"] = Relationship(
        back_populates="overall_essay_grade"
    )

class CriterionEssayGrade(SQLModel, table=True):
    __tablename__ = "criterion_essay_grade"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    score: int
    feedback: str = Field(sa_column=Column(Text))
    suggestion: str = Field(sa_column=Column(Text))

    overall_grade_id: int = Field(foreign_key="overall_essay_grade.id")
    overall_essay_grade: Optional[OverAllEssayGrade] = Relationship(
        back_populates="criterion_essay_grade"
    )
