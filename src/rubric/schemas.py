from pydantic import BaseModel
from typing import List, Dict

class CriterionIn(BaseModel):
    id: int
    name: str
   

class PerformanceLevelIn(BaseModel):
    id: int
    label: str
    score: int

class RubricCreateIn(BaseModel):
    name: str
    student_level: str
    grade_intensity: str
    language: str
    
    criteria: List[CriterionIn]
    performance_levels: List[PerformanceLevelIn]
    descriptors: Dict[str, Dict[str, str]]
