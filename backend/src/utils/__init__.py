"""
src.utils

This package contains utility functions and classes for IT-JobScraper, including:

- File helpers: get_static_file, get_log_file
- JSON mappers: create_skill_mappings_file, create_country_mappings_file
- Logging: setup_logging
- Normalization: remove_special_chars, remove_extra_spaces, normalize_string
- OAuth: oauth2_scheme, oauth
- Parsers: parse_skill, parse_skill_list, try_extract_skills, parse_seniority, parse_seniority_list, try_extract_seniorities, parse_country
- Security: verify_password, get_password_hash, validate_password_complexity, create_access_token, create_refresh_token, decode_token, hash_token
- Classes (Enums & Exceptions)
"""

# File helpers
from src.utils.files import get_static_file, get_log_file

# JSON mappers
from src.utils.json_mapper import create_skill_mappings_file, create_country_mappings_file
from src.utils.logging import setup_logging

# Normalization
from src.utils.normalizer import remove_special_chars, remove_extra_spaces, normalize_string

# OAuth
from src.utils.oauth import oauth2_scheme, oauth

# Parsers
from src.utils.parsers import (
    parse_skill,
    parse_skill_list,
    try_extract_skills,
    parse_seniority,
    parse_seniority_list,
    try_extract_seniorities,
    parse_country,
)

# Security
from src.utils.security import (
    verify_password,
    get_password_hash,
    validate_password_complexity,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_token,
)

from src.utils.classes import *

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

    # OAuth
    "oauth2_scheme",
    "oauth",

    # Parsers
    "parse_skill",
    "parse_skill_list",
    "try_extract_skills",
    "parse_seniority",
    "parse_seniority_list",
    "try_extract_seniorities",
    "parse_country",

    # Security
    "verify_password",
    "get_password_hash",
    "validate_password_complexity",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "hash_token",

    # Classes
    "LogLevel",
    "SeniorityLevel",
    "LOG_LEVEL_PRIORITY",
    "AppError",
    "AlreadyExistsError",
    "InvalidEntryError",
    "NotFoundError",
    "UnauthorizedError",
    "PermissionDeniedError",
]
