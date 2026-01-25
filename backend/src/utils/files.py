import os
from src.utils.classes.exceptions import NotFoundError


def get_static_file(filename: str, must_exist: bool = False):
    here = os.path.dirname(__file__)
    static_dir = os.path.join(here, "static")
    os.makedirs(static_dir, exist_ok=True)
    file = os.path.join(static_dir, filename) 
    if must_exist and not os.path.exists(file):
        raise NotFoundError(f"File '{filename}' not found") 
    return file


def get_log_file(filename: str, must_exist: bool = False):
    here = os.path.dirname(__file__)
    src = os.path.dirname(here)
    backend = os.path.dirname(src)
    logs_dir = os.path.join(backend, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    file = os.path.join(logs_dir, filename) 
    if must_exist and not os.path.exists(file):
        raise NotFoundError(f"File '{filename}' not found") 
    return file
