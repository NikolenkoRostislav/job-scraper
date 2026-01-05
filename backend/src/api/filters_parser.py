from typing import List, Optional
from src.utils.parsers import parse_skill_list, parse_seniority_list

def parse_filters(seniority_filters: Optional[List[str]], skill_filters: Optional[List[str]]) -> dict:
    filters = {"seniority": [], "skills": []}
    
    seniority_list = parse_seniority_list(seniority_filters or [], strict=True)
    for seniority in seniority_list:
        if seniority is not None:
            filters["seniority"].append(seniority)

    skill_list = parse_skill_list(skill_filters or [])
    for item in skill_list:
        skill, category = item
        if category is not None: # only include recognized skills, otherwise typos like "pythn" will result in no matches and that would be bad :(
            filters["skills"].append(skill) # maybe I'll remove the check later and just have frontend suggest skills but I'll leave it like this for now

    return dict(filters)
