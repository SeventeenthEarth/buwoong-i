# Directory Markdown Generator

## Overview

This project is a Python-based utility that reads all files with specific extensions (currently `dart`, `py`, `sql`), as well as `Dockerfile` and `docker-compose.yaml/yml`, from a given directory and generates a Markdown (`.md`) document. This Markdown document contains metadata, including a file count and directory tree, as well as the content of each file.

The utility is useful for documenting code directories, providing a readable format of the source code within a project, and archiving current states of codebases in a clear, structured manner.

## Features

- **Supported Extensions**: Reads `.dart`, `.py`, `.sql` files, and also `Dockerfile`, `docker-compose.yaml/yml`.
- **Metadata Generation**: Generates metadata about the directory, including file counts and a directory structure tree.
- **Markdown Output**: Produces an output Markdown file with headers, file paths, and code blocks for easy readability.
- **Custom Title**: Optionally add a title to the output Markdown file, replacing the default directory name in the document header and output filename.
- **Input Configuration**: Supports an `input.yaml` file for easy specification of directories and file extensions.
- **Output Directory**: Saves the Markdown file in an `output` directory, ensuring neat organization of generated files.

## Installation

To run this utility, ensure you have Python 3.7 or higher installed on your machine.

Additionally, you will need the `typer` package for command-line interaction. Install it using:

```sh
pip install typer
```

## Configuration

The input to the script is controlled via an `input.yaml` file. Below is a guide to its structure:

```yaml
title: PROJECT_NAME
extension: PROJECT_LANGUAGE
path: PROJECT_PATH
exclude_dir:
  - setup
  - ...
```

## Usage

Run the program from the command line with the following command:

```sh
python main.py -i input.yaml
```

### Arguments in input.yaml:
- `title`: (Optional) Custom title for the Markdown file. If omitted, the last directory name will be used.
- `extension`: The file extension to filter files (`dart`, `py`, or `sql`).
- `path`: The path to the directory you wish to scan for files.
- `exclude_dir`: (Optional) List of directories to exclude from the documentation.

## Output

The output file is saved in an `output` directory within the current working directory. The file naming convention is as follows:

```
[title_or_last_directory]_[timestamp].md
```

Where `title_or_last_directory` is the provided title or the name of the target directory and `timestamp` is the current date and time in the format `YYYYMMDD_HHMMSS`.

## Directory Structure

The generated Markdown document contains:

1. **Header**: Indicates the directory being documented or the provided title.
2. **Metadata Section**: Shows the total number of files matching the extension and a directory tree view.
3. **Code Section**: Displays the contents of each file, with file names and paths included as headers.

## Development

This project was written using Python and is designed to be simple and lightweight, making use of the `os`, `datetime`, `pathlib`, `yaml`, and `typer` libraries.

Feel free to modify the code to add support for additional file types or change the output format as needed.

## License

This project is open-source. Feel free to use it and adapt it to suit your needs.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with a clear description of your changes.

## Contact

If you have any questions or issues, feel free to open an issue on the project's GitHub repository or reach out to the maintainer.

