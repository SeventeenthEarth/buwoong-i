# extension_configs.py

EXTENSION_CONFIGS = {
    "common": {
        "exclude_dir": [
            ".vscode",
            ".idea",
            ".githook",
            ".aider.tags.cache.v3",
            ".git",
            ".githooks",
        ],
        "exclude_file": [".gitignore", ".gitkeep"],
        "exclude_extension": [],
        "include_file": ["makefile"],
    },
    "python": {
        "exclude_dir": [".venv", "venv", "__pycache__", ".mypy_cache"],
        "exclude_file": ["__init__.py"],
        "exclude_extension": [".pyc"],
        "include_file": [
            "dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
        ],
    },
    "dart": {
        "exclude_dir": [
            "ios",
            "android",
            "macos",
            "window",
            "web",
            "build",
            "assets",
            ".dart_tool",
        ],
        "exclude_file": [],
        "exclude_extension": [".g.dart", ".gr.dart"],
        "include_file": ["pubspec.yaml"],
    },
    "sql": {
        "exclude_dir": [],
        "exclude_file": [],
        "exclude_extension": [],
        "include_file": [],
    },
}

EXTENSION_MAP = {"py": "python", "dart": "dart", "sql": "sql"}
