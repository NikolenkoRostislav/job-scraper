import json
import os
import re


def parse_skill(skill: str):
    normalized_skill = skill.strip().lower()
    normalized_skill = re.sub(r'[^\w\s\.-]', '', normalized_skill) #remove special chars
    normalized_skill = re.sub(r'\s+', ' ', normalized_skill) #remove extra spaces

    here = os.path.dirname(__file__)
    skill_file = os.path.join(here, "skill_mappings.json")

    with open(skill_file, "r") as f:
        skill_mappings = json.load(f)
        for entry in skill_mappings:
            if re.fullmatch(entry["pattern"], normalized_skill):
                return entry["canonical"], entry["category"]
    return normalized_skill, None

def parse_skill_list(skill_list):
    parsed_skills = []
    for skill in skill_list:
        canonical, category = parse_skill(skill)
        parsed_skills.append((canonical, category))
    return parsed_skills

def parse_seniority(seniority: str, strict: bool = False):
    patterns = {
        "junior": r"junior",
        "mid": r"(mid|middle|intermediate)",
        "senior": r"senior"
    }

    normalized = seniority.strip().lower()
    normalized = re.sub(r'[^\w\s\.-]', '', normalized) #remove special chars

    for level, pattern in patterns.items():
        if re.search(pattern, normalized):
            return level
        
    if strict:   
        return None
    return normalized

def parse_seniority_list(seniority_list, strict: bool = False):
    parsed_levels = []
    for seniority in seniority_list:
        level = parse_seniority(seniority, strict=strict)
        parsed_levels.append(level)
    return parsed_levels

