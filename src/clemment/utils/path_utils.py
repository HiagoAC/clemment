import os
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


def discover_files(path: Path) -> List[Path]:
    """
    Discover all files in a directory and its subdirectories.
    """
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    return files
