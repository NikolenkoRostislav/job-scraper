import json
import re
from typing import Callable
from src.utils.files import get_static_file


def get_pattern(aliases) -> str:
    if not aliases:
        return 
    
    escaped_aliases = [re.escape(alias.lower()) for alias in aliases]

    if len(escaped_aliases) == 1:
        return f"^{escaped_aliases[0]}$"

    pattern = "^(" + "|".join(escaped_aliases) + ")$"
    return pattern


def add_skill_mapping(entry, mappings):
    pattern = get_pattern(entry.get("aliases", []))
    canonical_name = entry.get("canonical")
    category = entry.get("category", "unknown")
    if not pattern or not canonical_name:
        return
    mappings.append({"canonical": canonical_name, "category": category, "pattern": pattern})


def add_country_mapping(entry, mappings):
    pattern = get_pattern(entry.get("aliases", []))
    name = entry.get("name")
    if not pattern or not name:
        return
    mappings.append({"name": name, "pattern": pattern})


def create_mappings_file(infos_path: str, mappings_filename: str, add_mapping: Callable):
    mappings = []

    with open(infos_path, "r", encoding="utf-8") as f:
        infos = json.load(f)
        for entry in infos:
            add_mapping(entry, mappings)

    mappings_file = get_static_file(mappings_filename)

    with open(mappings_file, "w", encoding="utf-8") as f:
        json.dump(mappings, f, indent=2, ensure_ascii=False)


def create_skill_mappings_file(infos_path: str, mappings_filename: str):
    create_mappings_file(infos_path, mappings_filename, add_skill_mapping)


def create_country_mappings_file(infos_path: str, mappings_filename: str):
    create_mappings_file(infos_path, mappings_filename, add_country_mapping)
