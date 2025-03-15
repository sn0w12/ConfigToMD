#!/usr/bin/env python
import argparse
import os
import re
from collections import defaultdict


def extract_config_settings(directory, config_name="config"):
    """Extract all config settings from .py files in the given directory."""

    # Escape the config name for regex
    config_regex = re.escape(config_name)

    # Regex patterns to extract config settings
    patterns = [
        # Pattern for config["Category"].get("name", default)
        rf'{config_regex}\["([^"]+)"\]\.get\("([^"]+)",\s*("([^"]*)"|\'([^\']*)\'|([^"\'\)\s,]+))\)',
        # Pattern for config.getboolean("Category", "name", fallback=default)
        rf'{config_regex}\.getboolean\("([^"]+)",\s*"([^"]+)"(?:,\s*fallback=([^)]+))?\)',
        # Pattern for config.getint("Category", "name", fallback=default)
        rf'{config_regex}\.getint\("([^"]+)",\s*"([^"]+)"(?:,\s*fallback=([^)]+))?\)',
        # Pattern for config.getfloat("Category", "name", fallback=default)
        rf'{config_regex}\.getfloat\("([^"]+)",\s*"([^"]+)"(?:,\s*fallback=([^)]+))?\)',
        # Pattern for direct access: config["Category"]["name"]
        rf'{config_regex}\["([^"]+)"\]\["([^"]+)"\]',
        # Pattern for config["Category"].getboolean("name", default)
        rf'{config_regex}\["([^"]+)"\]\.getboolean\("([^"]+)",\s*([^)]+)\)',
        # Pattern for config["Category"].getint("name", default)
        rf'{config_regex}\["([^"]+)"\]\.getint\("([^"]+)",\s*([^)]+)\)',
        # Pattern for config["Category"].getfloat("name", default)
        rf'{config_regex}\["([^"]+)"\]\.getfloat\("([^"]+)",\s*([^)]+)\)',
    ]

    # Initialize dictionary for config settings, file paths, and types
    config_settings = defaultdict(dict)
    file_paths = defaultdict(dict)
    value_types = defaultdict(dict)

    # Map pattern indices to value types
    type_map = {
        0: None,  # config["Category"].get() - type determined from value
        1: "boolean",  # config.getboolean()
        2: "integer",  # config.getint()
        3: "float",  # config.getfloat()
        4: None,  # direct access - type unknown
        5: "boolean",  # config["Category"].getboolean()
        6: "integer",  # config["Category"].getint()
        7: "float",  # config["Category"].getfloat()
    }

    # Walk through all Python files in the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                        # Process each pattern
                        for pattern_index, pattern in enumerate(patterns):
                            matches = re.findall(pattern, content)

                            for match in matches:
                                category = match[0]

                                if pattern_index == 4:  # Direct access pattern
                                    name = match[1]
                                    default_value = "N/A"  # No default provided with direct access
                                    value_type = "Unknown"
                                elif pattern_index >= 5:  # config["Category"].getX("name", default) patterns
                                    name = match[1]
                                    default_value = match[2]
                                    value_type = type_map[pattern_index]
                                else:  # All other patterns
                                    name = match[1]
                                    value_type = type_map[pattern_index]

                                    # Handle different pattern formats
                                    if pattern_index == 0:  # config["Category"].get()
                                        # Extract the default value based on which group matched
                                        if match[3]:  # Double quoted string
                                            default_value = match[3]
                                            if value_type is None:
                                                value_type = "string"
                                        elif match[4]:  # Single quoted string
                                            default_value = match[4]
                                            if value_type is None:
                                                value_type = "string"
                                        elif match[5]:  # Unquoted value
                                            default_value = match[5]
                                            # Try to determine type from value
                                            if value_type is None:
                                                if default_value.lower() in ("true", "false"):
                                                    value_type = "boolean"
                                                elif default_value.isdigit():
                                                    value_type = "integer"
                                                elif default_value.replace(".", "", 1).isdigit():
                                                    value_type = "float"
                                                else:
                                                    value_type = "Unknown"
                                        else:
                                            default_value = match[2]  # Fallback
                                            value_type = "Unknown"
                                    else:  # config.getX() patterns
                                        # For getboolean, getint, getfloat
                                        default_value = match[2] if len(match) > 2 and match[2] else "None"

                                # Store the setting if not already recorded or if has default value
                                if name not in config_settings[category] or default_value != "N/A":
                                    config_settings[category][name] = default_value
                                    file_paths[category][name] = file_path
                                    value_types[category][name] = value_type

                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

    return config_settings, file_paths, value_types


def generate_markdown_tables(config_settings, file_paths=None, value_types=None, verbose=False, header_level=1):
    """Generate markdown tables for each config category."""

    # Create header markers based on header level
    main_header = "#" * header_level
    category_header = "#" * (header_level + 1)

    markdown = f"{main_header} Configuration Settings\n\n"

    for category, settings in sorted(config_settings.items()):
        markdown += f"{category_header} {category}\n\n"

        if verbose and file_paths:
            markdown += "| Setting | Type | Default Value | Source File |\n"
            markdown += "|---------|------|---------------|-------------|\n"

            for name, default_value in sorted(settings.items()):
                source_file = file_paths.get(category, {}).get(name, "Unknown")
                value_type = value_types.get(category, {}).get(name, "Unknown")

                # Get just the filename, not full path
                if source_file != "Unknown":
                    source_file = os.path.basename(source_file)

                markdown += f"| {name} | {value_type} | `{default_value}` | `{source_file}` |\n"
        else:
            markdown += "| Setting | Type | Default Value |\n"
            markdown += "|---------|------|---------------|\n"

            for name, default_value in sorted(settings.items()):
                value_type = value_types.get(category, {}).get(name, "Unknown")
                markdown += f"| {name} | {value_type} | `{default_value}` |\n"

        markdown += "\n"

    return markdown


def main():
    parser = argparse.ArgumentParser(
        description="Extract config settings from Python files and generate markdown tables."
    )
    parser.add_argument("directory", help="Directory to scan for Python files")
    parser.add_argument("-o", "--output", help="Output markdown file (if not specified, prints to stdout)")
    parser.add_argument("-c", "--config-name", default="config", help="Name of the config variable (default: 'config')")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print source file in output")
    parser.add_argument(
        "-l",
        "--header-level",
        type=int,
        default=1,
        choices=range(1, 7),
        help="Markdown header level to use (1-6, default: 1)",
    )

    args = parser.parse_args()

    # Extract config settings
    config_settings, file_paths, value_types = extract_config_settings(args.directory, args.config_name)

    # Generate markdown tables
    markdown = generate_markdown_tables(config_settings, file_paths, value_types, args.verbose, args.header_level)

    # Output results
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
        print(f"Markdown tables written to {args.output}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
