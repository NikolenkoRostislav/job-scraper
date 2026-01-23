from enum import Enum


class SeniorityLevel(Enum):
    junior = "junior"
    mid = "mid"
    senior = "senior"


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
