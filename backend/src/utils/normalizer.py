import re


def remove_special_chars(input_str: str):
    if not input_str:
        return input_str
    return re.sub(r'[^\w\s\.+#-]', '', input_str)

def remove_extra_spaces(input_str: str):
    if not input_str:
        return input_str
    return re.sub(r'\s+', ' ', input_str)

def normalize_string(input_str: str):
    if not input_str:
        return input_str
    output_str = input_str.strip().lower()
    output_str = remove_special_chars(output_str)
    output_str = remove_extra_spaces(output_str)
    return output_str
