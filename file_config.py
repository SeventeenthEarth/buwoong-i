from dataclasses import dataclass
from typing import Set


@dataclass
class FileConfig:
    exclude_dirs: Set[str]
    exclude_files: Set[str]
    exclude_extensions: Set[str]
    include_files: Set[str]
