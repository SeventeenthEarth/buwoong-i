from typing import Union, Dict, Any, Set, List, Tuple
import os
import datetime
from pathlib import Path
import typer

from file_config import FileConfig
from project_config import ProjectConfig
from extension_configs import EXTENSION_CONFIGS, EXTENSION_MAP


def validate_inputs(directory: Union[str, os.PathLike], target_extension: str) -> None:
    if target_extension not in ["dart", "py", "sql"]:
        raise ValueError("Only 'dart', 'py', 'sql' file extensions are allowed.")

    if not os.path.exists(directory):
        raise FileNotFoundError(f"The provided path '{directory}' does not exist.")


def get_file_config(
    target_extension: str, additional_exclude_dirs: List[str] = None
) -> FileConfig:
    config_key = EXTENSION_MAP[target_extension]
    current_config = EXTENSION_CONFIGS[config_key]
    common_config = EXTENSION_CONFIGS["common"]

    return FileConfig(
        exclude_dirs=set(
            common_config["exclude_dir"]
            + current_config["exclude_dir"]
            + (additional_exclude_dirs or [])
        ),
        exclude_files=set(
            common_config["exclude_file"] + current_config["exclude_file"]
        ),
        exclude_extensions=set(
            common_config["exclude_extension"] + current_config["exclude_extension"]
        ),
        include_files=set(
            common_config["include_file"] + current_config["include_file"]
        ),
    )


def should_include_file(filename: str, extension: str, config: FileConfig) -> bool:
    if filename in config.exclude_files:
        return False

    if any(filename.endswith(ext) for ext in config.exclude_extensions):
        return False

    return (
        filename.endswith(f".{extension}") or filename.lower() in config.include_files
    )


def collect_files(
    directory: str, target_extension: str, config: FileConfig
) -> Tuple[List[str], List[str]]:
    target_files = []
    infrastructure_files = []
    abs_directory = os.path.abspath(directory)

    for root, dirs, files in os.walk(abs_directory):
        # Filter directories using exclude_dirs
        dirs[:] = [d for d in dirs if d not in config.exclude_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            if should_include_file(file, target_extension, config):
                if file.endswith(f".{target_extension}"):
                    target_files.append(file_path)
                else:
                    infrastructure_files.append(file_path)

    return target_files, infrastructure_files


def generate_metadata_section(
    abs_directory: str,
    target_files: List[str],
    infrastructure_files: List[str],
    target_extension: str,
    config: FileConfig,
) -> str:
    content = "## Metadata\n\n"
    content += f"- Total number of '{target_extension}' files: {len(target_files)}\n"
    content += (
        f"- Total number of Infrastructure files: {len(infrastructure_files)}\n\n"
    )
    content += "```\n"

    for root, dirs, files in os.walk(abs_directory):
        dirs[:] = [d for d in dirs if d not in config.exclude_dirs]

        level = root.replace(abs_directory, "").count(os.sep)
        indent = " " * 4 * level
        content += f"{indent}{Path(root).name}/\n"

        sub_indent = " " * 4 * (level + 1)
        included_files = [
            f for f in files if should_include_file(f, target_extension, config)
        ]
        for file in sorted(included_files):
            content += f"{sub_indent}{file}\n"

    content += "```\n\n"
    return content


def generate_code_section(
    abs_directory: str, files: List[str], target_extension: str
) -> str:
    content = "## Code\n\n"

    for file_path in sorted(files):
        relative_path = os.path.relpath(file_path, abs_directory)
        file_name = Path(file_path).name
        extension = get_file_extension(file_name, target_extension)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            content += f"### {relative_path}\n\n"
            content += f"```{extension}\n{file_content}\n```\n\n"
        except Exception as e:
            content += f"### {relative_path}\n\n"
            content += f"Error reading file: {str(e)}\n\n"

    return content


def get_file_extension(file_name: str, target_extension: str) -> str:
    if file_name.lower() == "dockerfile":
        return "docker"
    elif file_name.lower() in ["docker-compose.yml", "docker-compose.yaml"]:
        return "yaml"
    elif file_name.lower() == "makefile":
        return "makefile"
    return target_extension


def read_files_in_directory(
    directory: Union[str, os.PathLike],
    target_extension: str,
    title: str = None,
    additional_exclude_dirs: list = None,
) -> str:
    # Validate inputs
    validate_inputs(directory, target_extension)

    # Initialize configurations
    config = get_file_config(target_extension, additional_exclude_dirs)
    abs_directory = os.path.abspath(directory)
    last_directory = os.path.basename(os.path.normpath(abs_directory))
    header_title = title if title else last_directory

    # Collect files
    target_files, infrastructure_files = collect_files(
        directory, target_extension, config
    )

    # Generate markdown content
    markdown_content = f"# Files for {header_title}\n\n"
    markdown_content += generate_metadata_section(
        abs_directory, target_files, infrastructure_files, target_extension, config
    )
    markdown_content += generate_code_section(
        abs_directory, target_files + infrastructure_files, target_extension
    )

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
    if not input_file:
        raise typer.BadParameter("Please provide a YAML configuration file.")

    config = ProjectConfig.from_yaml(input_file)

    # Generate timestamp for the output file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    last_directory = os.path.basename(os.path.normpath(config.path))
    output_directory = "output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file_title = config.title if config.title else last_directory
    output_file = os.path.join(output_directory, f"{output_file_title}_{timestamp}.md")

    try:
        markdown_content = read_files_in_directory(
            config.path, config.extension, config.title, config.exclude_dir
        )
        save_markdown(markdown_content, output_file)
        print(f"Markdown file '{output_file}' created successfully.")
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    typer.run(main)
