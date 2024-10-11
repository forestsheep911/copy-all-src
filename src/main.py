import os
import pyperclip
import argparse
from utils import load_ignore_patterns, get_directory_structure_with_file_contents


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="additional patterns to ignore (files and directories)",
    )
    parser.add_argument(
        "--ignore-config", type=str, help="path to additional ignore config file"
    )
    args = parser.parse_args()

    additional_ignore_patterns = set(args.ignore)

    # Load patterns from default ignore file
    default_ignore_patterns = load_ignore_patterns("src/default_ignore")
    additional_ignore_patterns.update(default_ignore_patterns)

    # Load patterns from .gitignore if it exists
    gitignore_patterns = load_ignore_patterns(".gitignore")
    additional_ignore_patterns.update(gitignore_patterns)

    # Load patterns from specified ignore config file if provided
    if args.ignore_config:
        user_ignore_patterns = load_ignore_patterns(args.ignore_config)
        additional_ignore_patterns.update(user_ignore_patterns)

    ignore_patterns = list(additional_ignore_patterns)

    current_dir = os.getcwd()
    directory_structure, file_contents = get_directory_structure_with_file_contents(
        current_dir, ignore_patterns
    )
    final_output = directory_structure + file_contents
    pyperclip.copy(final_output)
    print("Directory structure and file contents copied to clipboard.")
