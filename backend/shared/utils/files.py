from pathlib import Path

from shared.utils.classes.exceptions import NotFoundError


def get_static_file(filename: str, must_exist: bool = False) -> Path:
    here = Path(__file__).resolve().parent
    static_dir = here / "static"
    static_dir.mkdir(parents=True, exist_ok=True)

    file = static_dir / filename
    if must_exist and not file.exists():
        raise NotFoundError(f"File '{filename}' not found")

    return file


def get_log_file(filename: str, must_exist: bool = False) -> Path:
    here = Path(__file__).resolve().parent
    backend = here.parent.parent
    logs_dir = backend / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    file = logs_dir / filename
    if must_exist and not file.exists():
        raise NotFoundError(f"File '{filename}' not found")

    return file
