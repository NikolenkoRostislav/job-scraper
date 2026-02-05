from shared.utils import create_skill_mappings_file
from core.config import settings


# For creating a skill mappings file
skill_info_path = input("Enter skill info file path:")
create_skill_mappings_file(skill_info_path, settings.files.SKILL_MAPPINGS_FILENAME)
