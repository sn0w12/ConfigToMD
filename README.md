# ConfigToMD

ConfigToMD is a Python utility that scans through Python code to extract configuration settings and automatically generate documentation in Markdown format.

## Description

This tool helps developers maintain up-to-date documentation for their configuration settings by automatically scanning their codebase. ConfigToMD identifies various patterns of configuration usage in Python files and compiles them into organized Markdown tables, grouped by configuration categories.

## Features

-   Extracts configuration settings from Python files
-   Detects different configuration access patterns (direct access, get methods, type-specific methods)
-   Identifies default values and their types
-   Generates organized Markdown tables by configuration category
-   Supports verbose mode with source file information
-   Customizable header levels for Markdown output

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ConfigToMD.git
cd ConfigToMD

# Install the package
pip install .

# Or install in development mode
pip install -e .
```

## Usage

### Basic Usage

```bash
configtomd /path/to/your/project
```

This will scan all Python files in the specified directory and its subdirectories, then output Markdown tables to the console.

### Options

```
usage: configtomd [-h] [-o OUTPUT] [-c CONFIG_NAME] [-v] [-l {1,2,3,4,5,6}] directory

Extract config settings from Python files and generate markdown tables.

positional arguments:
  directory             Directory to scan for Python files

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output markdown file (if not specified, prints to stdout)
  -c CONFIG_NAME, --config-name CONFIG_NAME
                        Name of the config variable (default: 'config')
  -v, --verbose         Print source file in output
  -l {1,2,3,4,5,6}, --header-level {1,2,3,4,5,6}
                        Markdown header level to use (1-6, default: 1)
```

### Supported Configuration Patterns

ConfigToMD recognizes the following configuration access patterns:

-   `config["Category"].get("name", default)`
-   `config.getboolean("Category", "name", fallback=default)`
-   `config.getint("Category", "name", fallback=default)`
-   `config.getfloat("Category", "name", fallback=default)`
-   `config["Category"]["name"]`
-   `config["Category"].getboolean("name", default)`
-   `config["Category"].getint("name", default)`
-   `config["Category"].getfloat("name", default)`

### Example Output

```markdown
# Configuration Settings

## Database

| Setting  | Type    | Default Value |
| -------- | ------- | ------------- |
| host     | string  | `localhost`   |
| port     | integer | `5432`        |
| username | string  | `admin`       |

## Logging

| Setting | Type    | Default Value |
| ------- | ------- | ------------- |
| level   | string  | `INFO`        |
| file    | string  | `app.log`     |
| console | boolean | `True`        |
```

### License

This project is licensed under the MIT License. See the LICENSE file for details.
