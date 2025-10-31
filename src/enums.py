from enum import Enum

class EssayStatus(str, Enum):
    GRADING = "grading"
    READY_FOR_REVIEW = "ready_for_review"
    
    
class RubricStudentLevel(str, Enum):
    ELEMENTARY = "elementary"
    HIGH_SCHOOL = "high_school"
    COLLEGE = "college"
    
    
class RubricGradeIntensity(str, Enum):
    EASY = "easy"
    NORMAL = "normal"
    STRICT = "strict"
    
    
class RubricLanguage(str, Enum):
    ENGLISH = "english"
    FILIPINO = "filipino"


class RubricEssayType(str, Enum):
    ARGUMENTATIVE = "argumentative"
    NARRATIVE = "narrative"
    DESCRIPTIVE = "descriptive"
    PERSUASIVE = "persuasive"
    REFLECTIVE = "reflective"