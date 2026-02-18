from enum import Enum


class JobOrder(Enum):
    update_time = "update_time"
    creation_time = "creation_time"
    favorites = "favorites"


class SeniorityLevel(Enum):
    junior = "junior"
    mid = "mid"
    senior = "senior"


LOG_LEVEL_PRIORITY = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50,
}


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class SourceWebsite(Enum):
    get_in_it = "getinit"
    relocate_me = "relocateme"
    sap = "sap"
    siemens = "siemens"
    we_are_developers = "wearedevelopers"
    zalando = "zalando"
    dice = "dice"
    djinni = "djinni"