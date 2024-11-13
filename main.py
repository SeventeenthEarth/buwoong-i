from typing import Union
import os
import datetime
from pathlib import Path
import typer


def read_files_in_directory(
    directory: Union[str, os.PathLike], target_extension: str, title: str = None
) -> str:
    if target_extension not in ["dart", "py", "sql"]:
        raise ValueError("Only 'dart', 'py', 'sql' file extensions are allowed.")

    if not os.path.exists(directory):
        raise FileNotFoundError(f"The provided path '{directory}' does not exist.")

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
    for root, dirs, files in os.walk(abs_directory):
        # Exclude venv, .venv directories, __init__.py, and cache files
        dirs[:] = [
            d
            for d in dirs
            if d not in [".venv", "venv", ".idea", ".vscode", "__pycache__"]
        ]
        for file in files:
            if (
                file.endswith(f".{target_extension}")
                and file != "__init__.py"
                and not file.endswith(".pyc")
            ):
                target_files.append(os.path.join(root, file))
            elif file.lower() in [
                "dockerfile",
                "docker-compose.yml",
                "docker-compose.yaml",
                "makefile",
            ]:
                infrastructure_files.append(os.path.join(root, file))

    # Add metadata section with file count and directory tree
    markdown_content += "## Metadata\n\n"
    markdown_content += (
        f"- Total number of '{target_extension}' files: {len(target_files)}\n"
    )
    markdown_content += (
        f"- Total number of Infrastructure files: {len(infrastructure_files)}\n\n"
    )
    markdown_content += "```\n"

    for root, dirs, files in os.walk(abs_directory):
        # Exclude venv, .venv directories, .idea, .vscode, __init__.py, and cache files
        dirs[:] = [
            d
            for d in dirs
            if d not in [".venv", "venv", ".idea", ".vscode", "__pycache__"]
        ]
        level = root.replace(abs_directory, "").count(os.sep)
        indent = " " * 4 * level
        markdown_content += f"{indent}{Path(root).name}/\n"
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            if (
                file.endswith(f".{target_extension}")
                and file != "__init__.py"
                and not file.endswith(".pyc")
            ):
                markdown_content += f"{sub_indent}{file}\n"
            elif file.lower() in [
                "dockerfile",
                "docker-compose.yml",
                "docker-compose.yaml",
                "makefile",
            ]:
                markdown_content += f"{sub_indent}{file}\n"
    markdown_content += "```\n\n"

    # Add code section header
    markdown_content += "## Code\n\n"

    # Add each file's content
    for file_path in target_files + infrastructure_files:
        relative_path = os.path.relpath(file_path, abs_directory)
        file_name = Path(file_path).name
        with open(file_path, "r") as f:
            file_content = f.read()

        # Determine the file extension for code block
        if file_name.lower() == "dockerfile":
            extension = "docker"
        elif file_name.lower() in ["docker-compose.yml", "docker-compose.yaml"]:
            extension = "yaml"
        elif file_name.lower() == "makefile":
            extension = "makefile"
        else:
            extension = target_extension

        # Add H3 with file name including internal directory path and code block with the file content
        markdown_content += f"### {relative_path}\n\n"
        markdown_content += f"```{extension}\n{file_content}\n```\n\n"

    return markdown_content


def save_markdown(content: str, output_file: str):
    with open(output_file, "w") as f:
        f.write(content)


def main(
    directory: str,
    extension: str,
    title: str = typer.Option(None, "--title", help="Title for the markdown output"),
):
    # Generate timestamp for the output file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    last_directory = os.path.basename(os.path.normpath(directory))
    output_directory = "output"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file_title = title if title else last_directory
    output_file = os.path.join(output_directory, f"{output_file_title}_{timestamp}.md")

    try:
        markdown_content = read_files_in_directory(directory, extension, title)
        save_markdown(markdown_content, output_file)
        print(f"Markdown file '{output_file}' created successfully.")
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    typer.run(main)
