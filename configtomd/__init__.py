"""
ConfigToMD - A tool to extract config settings from Python files and generate markdown documentation.
"""

from .scan import extract_config_settings, generate_markdown_tables, main

__version__ = "0.1.0"
__all__ = ["extract_config_settings", "generate_markdown_tables", "main"]
