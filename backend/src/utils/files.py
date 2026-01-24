import os


def get_static_file(filename: str):
    here = os.path.dirname(__file__)
    static_dir = os.path.join(here, "static")
    os.makedirs(static_dir, exist_ok=True)
    return os.path.join(static_dir, filename) 


def get_log_file(filename: str):
    here = os.path.dirname(__file__)
    src = os.path.dirname(here)
    backend = os.path.dirname(src)
    logs_dir = os.path.join(backend, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.join(logs_dir, filename) 
