from shared.utils import create_country_mappings_file
from core.config import settings


# For creating a country mappings file
country_info_path = input("Enter country info file path:")
create_country_mappings_file(country_info_path, settings.files.COUNTRY_MAPPINGS_FILENAME)
