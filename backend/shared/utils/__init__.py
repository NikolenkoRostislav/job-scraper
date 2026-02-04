"""
shared.utils

This package contains utility functions and classes for IT-JobScraper, including:

- File helpers: get_static_file, get_log_file
- JSON mappers: create_skill_mappings_file, create_country_mappings_file
- Logging: setup_logging
- Normalization: remove_special_chars, remove_extra_spaces, normalize_string
- Parsers: parse_skill, parse_skill_list, try_extract_skills, parse_seniority, parse_seniority_list, try_extract_seniorities, parse_country
- Classes (Enums & Exceptions)
"""

# File helpers
from shared.utils.files import get_static_file, get_log_file

# JSON mappers
from shared.utils.json_mapper import create_skill_mappings_file, create_country_mappings_file
from shared.utils.logging import setup_logging

# Normalization
from shared.utils.normalizer import remove_special_chars, remove_extra_spaces, normalize_string

# Parsers
from shared.utils.parsers import (
    parse_skill,
    parse_skill_list,
    try_extract_skills,
    parse_seniority,
    parse_seniority_list,
    try_extract_seniorities,
    parse_country,
)

from shared.utils.classes import *

__all__ = [
    # File helpers
    "get_static_file",
    "get_log_file",

    # JSON mappers
    "create_skill_mappings_file",
    "create_country_mappings_file",

    # Logging
    "setup_logging",

    # Normalization
    "remove_special_chars",
    "remove_extra_spaces",
    "normalize_string",

    # Parsers
    "parse_skill",
    "parse_skill_list",
    "try_extract_skills",
    "parse_seniority",
    "parse_seniority_list",
    "try_extract_seniorities",
    "parse_country",

    # Classes
    "JobOrder",
    "LogLevel",
    "SeniorityLevel",
    "SourceWebsite"
    "LOG_LEVEL_PRIORITY",
    "AppError",
    "AlreadyExistsError",
    "InvalidEntryError",
    "NotFoundError",
    "UnauthorizedError",
    "PermissionDeniedError",
    "TooManyRequestsError",
]
