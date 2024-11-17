from dataclasses import dataclass
import yaml


@dataclass
class ProjectConfig:
    path: str
    extension: str
    title: str = None
    exclude_dir: list = None

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
