# Directory Markdown Generator

## Overview

This project is a Python-based utility that reads all files with specific extensions (currently `dart` or `py`), as well as `Dockerfile` and `docker-compose.yaml/yml`, from a given directory and generates a Markdown (`.md`) document. This Markdown document contains metadata, including a file count and directory tree, as well as the content of each file.

The utility is useful for documenting code directories, providing a readable format of the source code within a project, and archiving current states of codebases in a clear, structured manner.

## Features

- **Supported Extensions**: Reads `.dart`, `.py` files, and also `Dockerfile` and `docker-compose.yaml/yml`.
- **Metadata Generation**: Generates metadata about the directory, including file counts and a directory structure tree.
- **Markdown Output**: Produces an output Markdown file with headers, file paths, and code blocks for easy readability.
- **Custom Title**: Optionally add a title to the output Markdown file, replacing the default directory name in the document header and output filename.
- **Output Directory**: Saves the Markdown file in an `output` directory, ensuring neat organization of generated files.

## Installation

To run this utility, ensure you have Python 3.7 or higher installed on your machine.

Additionally, you will need the `typer` package for command-line interaction. Install it using:

```sh
pip install typer
```

## Usage

Run the program from the command line with the following command:

```sh
python main.py DIRECTORY_PATH EXTENSION [--title TITLE]
```

### Arguments:
- `DIRECTORY_PATH`: The path to the directory you wish to scan for files.
- `EXTENSION`: The file extension to filter files (`dart` or `py`).
- `--title TITLE`: (Optional) Custom title for the Markdown file. If omitted, the last directory name will be used.

### Example:

```sh
python main.py ./my_project py --title "My Project Documentation"
```

This command will generate a Markdown file containing all `.py` files from the `my_project` directory, with the custom title "My Project Documentation".

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

## Example Output

Below is an excerpt of the structure generated by the program:

```markdown
# My Project Documentation

## Metadata

- Total number of 'py' files: 5

```
my_project/
    file1.py
    file2.py
    subfolder/
        file3.py
```

## Code

### file1.py

```py
# File content here
```
```

## Error Handling

- **Invalid Extension**: If the provided file extension is not `dart` or `py`, the program raises a `ValueError`.
- **Invalid Directory**: If the provided directory path does not exist, a `FileNotFoundError` is raised.

## Development

This project was written using Python and is designed to be simple and lightweight, making use of the `os`, `datetime`, `pathlib`, and `typer` libraries.

Feel free to modify the code to add support for additional file types or change the output format as needed.

## License

This project is open-source. Feel free to use it and adapt it to suit your needs.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with a clear description of your changes.

## Contact

If you have any questions or issues, feel free to open an issue on the project's GitHub repository or reach out to the maintainer.

