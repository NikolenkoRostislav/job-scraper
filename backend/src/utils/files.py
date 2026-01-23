import os


def get_static_file(filename: str):
    here = os.path.dirname(__file__)
    return os.path.join(here, "static", filename) 
