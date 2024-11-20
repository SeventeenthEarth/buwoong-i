from dataclasses import dataclass
from typing import Optional

import yaml


@dataclass
class ProjectConfig:
    path: str
    extension: str
    title: str
    exclude_dir: list

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "ProjectConfig":
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)
        return cls(
            path=config.get("path"),
            extension=config.get("extension"),
            title=config.get("title"),
            exclude_dir=config.get("exclude_dir", []),
        )
