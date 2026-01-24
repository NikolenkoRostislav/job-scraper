from src.utils.json_mapper import create_country_mappings_file
from src.config import settings


# For creating a country mappings file
country_info_path = input("Enter country info file path:")
create_country_mappings_file(country_info_path, settings.COUNTRY_MAPPINGS_FILENAME)
