# Buwoong-i 🦉

> The name "Buwoong-i" (부엉이) is the Korean word for owl.

## Overview

A Python-based utility that scans project directories to find files with specific extensions (`dart`, `py`, `sql`) as well as `Dockerfile` and `docker-compose.yaml/yml`. It compiles these findings into a comprehensive Markdown (`.md`) document containing metadata (file counts and directory trees) along with the content of each file.

This tool is particularly valuable for documenting code directories, providing a readable format of source code, and creating clear, structured archives of codebases. It's especially useful for code reviews and analysis with AI, as it facilitates easy sharing of entire codebases.

## Features

- **File Discovery**
  - Scans for `.dart`, `.py`, `.sql` extensions
  - Locates `Dockerfile` and `docker-compose.yaml/yml` files

- **Metadata Generation**
  - Creates comprehensive directory statistics
  - Generates clear directory structure trees
  - Collects and organizes file contents

- **Document Organization**
  - Produces well-structured Markdown output
  - Supports custom title configuration
  - Enables easy setup through `input.yaml`
  - Neatly organizes output in a dedicated directory

## Installation

Ensure you have Python 3.7 or higher installed on your machine.

Install the required packages using:

```sh
pip install -r requirements.txt
```

## Configuration

Configure the tool through an `input.yaml` file:

```yaml
title: PROJECT_NAME
extension: PROJECT_LANGUAGE
path: PROJECT_PATH
exclude_dir:
  - setup
  - ...
```

## Usage

Run the tool with this command:

```sh
python main.py -i input/[input].yaml
```

### Arguments in input.yaml:
- `title`: (Optional) Custom title for your Markdown file. If omitted, uses the last directory name
- `extension`: File extension to search for (`dart`, `py`, or `sql`)
- `path`: Directory path to scan
- `exclude_dir`: (Optional) Directories to exclude from documentation

## Output

Generated files are saved in an `output` directory, following this naming convention:

```
[title_or_last_directory]_[timestamp].md
```

Where `title_or_last_directory` is your chosen title or directory name, and `timestamp` marks the creation time in `YYYYMMDD_HHMMSS` format.

## Directory Structure

The generated Markdown document contains:

1. **Header**: Identifies the documented directory or custom title
2. **Metadata Section**: Presents file counts and directory structure
3. **Code Section**: Displays file contents with clear headers showing paths

## Development

Built with Python using the `os`, `datetime`, `pathlib`, `yaml`, and `typer` libraries. The lightweight design makes it simple to maintain and modify.

Feel free to adapt the code to support additional file types or modify the output format according to your needs.

## License

MIT License

```
Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contributing

Contributions are welcome! Fork the repository and submit a pull request with your improvements clearly described.

## Contact

If you spot something that needs attention, open an issue on our GitHub repository or reach out to the maintainer directly.
