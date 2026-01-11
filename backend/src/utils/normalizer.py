import re


def normalize_string(input_str: str):
    if not input_str:
        return input_str
    output_str = input_str.strip().lower()
    output_str = re.sub(r'[^\w\s\.+#-]', '', output_str) #remove special chars
    output_str = re.sub(r'\s+', ' ', output_str) #remove extra spaces
    return output_str
