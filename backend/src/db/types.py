from sqlalchemy.dialects.postgresql import ENUM
from src.utils.classes.enums import SeniorityLevel


seniority_level_enum = ENUM(
    SeniorityLevel,
    name="seniority_level",
    create_type=False
)
