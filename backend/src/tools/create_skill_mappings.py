from src.utils.json_mapper import create_skill_mappings_file


# For creating a skill mappings file
skill_info_path = input("Enter skill info file path:")
create_skill_mappings_file(skill_info_path, "skill_mappings.json")
