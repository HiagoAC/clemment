from pathlib import Path
from typing import List


PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_absolute_path(filename: str, subdirs: List[str] = list()) -> str:
    """"
    Get the absolute path of a file in clemment package.
    """
    path = PROJECT_ROOT
    for subdir in subdirs:
        path = path / subdir
    return str(path / filename)