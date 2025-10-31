from pydantic import BaseModel
from typing import List, Dict


class CriterionIn(BaseModel):
    id: int
    name: str

class PerformanceLevelIn(BaseModel):
    id: int
    label: str
    score: int


class RubricIn(BaseModel):
    name: str
    student_level: str
    grade_intensity: str
    language: str
    essay_type: str

    criteria: List[CriterionIn]
    performance_levels: List[PerformanceLevelIn]
    descriptors: Dict[str, Dict[str, str]]



# --------------------------------------- OUTGOING RUBRIC DATA ----------------------------------------

class PerformanceLevelMiniOut(BaseModel):
    label: str
    score: int

    class Config:
        from_attributes = True


class CriterionLevelDescriptorOut(BaseModel):
    descriptor: str
    performance_levels: PerformanceLevelMiniOut  # ✅ embed level data here

    class Config:
        from_attributes = True


class CriterionOut(BaseModel):
    id: int
    title: str
    descriptors: List[CriterionLevelDescriptorOut]

    class Config:
        from_attributes = True

class LLMConsumableRubricOut(BaseModel):
    id: int
    name: str
    student_level: str
    grade_intensity: str
    language: str
    essay_type: str
    criterion: List[CriterionOut]

    class Config:
        from_attributes = True