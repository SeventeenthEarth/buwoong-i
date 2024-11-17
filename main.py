from typing import Union, Dict, Any
import os
import datetime
from pathlib import Path
import typer

from project_config import ProjectConfig


def read_files_in_directory(
    directory: Union[str, os.PathLike],
    target_extension: str,
    title: str = None,
    additional_exclude_dirs: list = None,
) -> str:
    if target_extension not in ["dart", "py", "sql"]:
        raise ValueError("Only 'dart', 'py', 'sql' file extensions are allowed.")

    if not os.path.exists(directory):
        raise FileNotFoundError(f"The provided path '{directory}' does not exist.")

    extension_configs = {
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
            "exclude_dir": [".venv", "venv", "__pycache__"],
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

    # Map file extension to config key
    extension_map = {"py": "python", "dart": "dart", "sql": "sql"}

    config_key = extension_map[target_extension]
    current_config = extension_configs[config_key]
    common_config = extension_configs["common"]

    # Combine common and specific configs
    exclude_dirs = set(
        common_config["exclude_dir"]
        + current_config["exclude_dir"]
        + (additional_exclude_dirs or [])
    )
    exclude_files = set(common_config["exclude_file"] + current_config["exclude_file"])
    exclude_extensions = set(
        common_config["exclude_extension"] + current_config["exclude_extension"]
    )
    include_files = set(common_config["include_file"] + current_config["include_file"])

    # Get absolute path for clarity
    abs_directory = os.path.abspath(directory)
    last_directory = os.path.basename(os.path.normpath(abs_directory))

    # Use provided title or fallback to last_directory
    header_title = title if title else last_directory

    # Start the markdown content with an H1 header of the directory path
    markdown_content = f"# Files for {header_title}\n\n"

    # Collect all target files and count them
    target_files = []
    infrastructure_files = []

    def should_include_file(filename: str, extension: str) -> bool:
        # Check if file should be excluded
        if filename in exclude_files:
            return False

        # Check if file has excluded extension
        if any(filename.endswith(ext) for ext in exclude_extensions):
            return False

        # Include if it's a target extension file or in include_files
        return filename.endswith(f".{extension}") or filename.lower() in include_files

    for root, dirs, files in os.walk(abs_directory):
        # Filter directories using exclude_dirs
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = os.path.join(root, file)

            if should_include_file(file, target_extension):
                if file.endswith(f".{target_extension}"):
                    target_files.append(file_path)
                else:
                    infrastructure_files.append(file_path)

    # Add metadata section with file count and directory tree
    markdown_content += "## Metadata\n\n"
    markdown_content += (
        f"- Total number of '{target_extension}' files: {len(target_files)}\n"
    )
    markdown_content += (
        f"- Total number of Infrastructure files: {len(infrastructure_files)}\n\n"
    )
    markdown_content += "```\n"

    # Generate directory tree
    for root, dirs, files in os.walk(abs_directory):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        level = root.replace(abs_directory, "").count(os.sep)
        indent = " " * 4 * level
        markdown_content += f"{indent}{Path(root).name}/\n"

        sub_indent = " " * 4 * (level + 1)
        included_files = [f for f in files if should_include_file(f, target_extension)]
        for file in sorted(included_files):
            markdown_content += f"{sub_indent}{file}\n"

    markdown_content += "```\n\n"

    # Add code section header
    markdown_content += "## Code\n\n"

    # Add each file's content
    for file_path in sorted(target_files + infrastructure_files):
        relative_path = os.path.relpath(file_path, abs_directory)
        file_name = Path(file_path).name

        # Determine the file extension for code block
        if file_name.lower() == "dockerfile":
            extension = "docker"
        elif file_name.lower() in ["docker-compose.yml", "docker-compose.yaml"]:
            extension = "yaml"
        elif file_name.lower() == "makefile":
            extension = "makefile"
        else:
            extension = target_extension

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()

            # Add H3 with file name including internal directory path and code block
            markdown_content += f"### {relative_path}\n\n"
            markdown_content += f"```{extension}\n{file_content}\n```\n\n"
        except Exception as e:
            markdown_content += f"### {relative_path}\n\n"
            markdown_content += f"Error reading file: {str(e)}\n\n"

    return markdown_content


def save_markdown(content: str, output_file: str):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)


def main(
    input_file: str = typer.Option(
        None, "--input", "-i", help="YAML configuration file path"
    ),
):
    """
    Collect files and generate markdown documentation.
    Can be run either with command line arguments or with a YAML configuration file.
    """
    config = None
    if input_file:
        config = ProjectConfig.from_yaml(input_file)
        directory = config.path
        extension = config.extension
        title = config.title
    else:
        raise typer.BadParameter("Please provide a YAML configuration file.")

    # Generate timestamp for the output file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    last_directory = os.path.basename(os.path.normpath(directory))
    output_directory = "output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_title = title if title else last_directory
    output_file = os.path.join(output_directory, f"{output_file_title}_{timestamp}.md")

    try:
        additional_exclude_dirs = config.exclude_dir if config else None
        markdown_content = read_files_in_directory(
            directory, extension, title, additional_exclude_dirs
        )
        save_markdown(markdown_content, output_file)
        print(f"Markdown file '{output_file}' created successfully.")
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    typer.run(main)
