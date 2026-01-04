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
