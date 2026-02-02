from src.utils import create_skill_mappings_file
from src.core.config import settings


# For creating a skill mappings file
skill_info_path = input("Enter skill info file path:")
create_skill_mappings_file(skill_info_path, settings.SKILL_MAPPINGS_FILENAME)
