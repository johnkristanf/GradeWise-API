from enum import Enum

class EssayStatus(str, Enum):
    GRADING = "grading"
    READY_FOR_REVIEW = "ready_for_review"
    
    
class RubricStudentLevel(str, Enum):
    ELEMENTARY = "Elementary"
    HIGH_SCHOOL = "High School"
    COLLEGE = "College"
    
    
class RubricGradeIntensity(str, Enum):
    EASY = "Easy"
    MODERATE = "Moderate"
    STRICT = "Strict"
    
    
class RubricLanguage(str, Enum):
    ENGLISH = "English"
    FILIPINO = "Filipino"


class RubricEssayType(str, Enum):
    ARGUMENTATIVE = "Argumentative"
    NARRATIVE = "Narrative"
    DESCRIPTIVE = "Descriptive"
    PERSUASIVE = "Persuasive"
    REFLECTIVE = "Reflective"