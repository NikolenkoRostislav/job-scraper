from typing import List, Optional
from src.utils.skill_parser import parse_skill

def parse_filters(seniority_filters: Optional[List[str]], skill_filters: Optional[List[str]]) -> dict:
    filters = {"seniority": [], "skills": []}
    
    for item in seniority_filters or []:
        normalized = item.lower().strip()
        if normalized in {"junior", "mid", "senior"}: # I should make a seniority parser util later
            filters["seniority"].append(normalized)

    for item in skill_filters or []:
        skill, category = parse_skill(item)
        if category is not None: # only include recognized skills, otherwise typos like "pythn" will result in no matches and that would be bad :(
            filters["skills"].append(skill) # maybe I'll remove the check later and just have frontend suggest skills but I'll leave it like this for now

    return dict(filters)
