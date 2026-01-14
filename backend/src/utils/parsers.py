import json
import os
import re
from src.utils.normalizer import normalize_string


def parse_skill(skill: str, strict: bool = False):
    normalized_skill = normalize_string(skill)

    here = os.path.dirname(__file__)
    skill_file = os.path.join(here, "skill_mappings.json")

    with open(skill_file, "r") as f:
        skill_mappings = json.load(f)
        for entry in skill_mappings:
            if re.fullmatch(entry["pattern"], normalized_skill):
                return entry["canonical"], entry["category"]
    if strict:
        return None, None
    return normalized_skill, None


def parse_skill_list(skill_list, strict: bool = False):
    parsed_skills = []
    for skill in skill_list:
        canonical, category = parse_skill(skill, strict=strict)
        parsed_skills.append((canonical, category))
    return parsed_skills


def try_extract_skills(source: str):  # gets skill names from a str, used for spiders
    if not source:
        return []

    skills = set()
    words = normalize_string(source).split()
    for word in words:
        skill_name, skill_category = parse_skill(word, strict=True)
        if skill_name:
            skills.add(skill_name)
    return list(skills)


def parse_seniority(seniority: str, strict: bool = False):
    patterns = {
        "junior": r"junior",
        "mid": r"(mid|middle|intermediate)",
        "senior": r"senior",
    }

    normalized_seniority = normalize_string(seniority)

    for level, pattern in patterns.items():
        if re.search(pattern, normalized_seniority):
            return level

    if strict:
        return None
    return normalized_seniority


def parse_seniority_list(seniority_list, strict: bool = False):
    parsed_levels = []
    for seniority in seniority_list:
        level = parse_seniority(seniority, strict=strict)
        parsed_levels.append(level)
    return parsed_levels


def try_extract_seniorities(source: str):
    if not source:
        return []

    seniorities = set()
    words = normalize_string(source).split()
    for word in words:
        if seniority := parse_seniority(word, strict=True):
            seniorities.add(seniority)
    return list(seniorities)


def parse_country(location_str: str):
    normalized_location_str = normalize_string(location_str)
    if not normalized_location_str:
        return None

    here = os.path.dirname(__file__)
    country_file = os.path.join(here, "country_mappings.json")

    with open(country_file, "r", encoding="utf-8") as f:
        words = normalized_location_str.split()
        country_mappings = json.load(f)
        for entry in country_mappings:
            for word in words:
                if re.fullmatch(entry["pattern"], word):
                    return entry["name"]
    return None
