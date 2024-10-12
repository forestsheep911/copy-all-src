import os
import pyperclip
import argparse
from utils import load_ignore_patterns, get_directory_structure_with_file_contents

# ANSI color codes for blue text
BLUE = '\033[94m'
RESET = '\033[0m'

def format_bytes_to_kb(bytes_size):
    """Convert bytes to kilobytes (KB) with 2 decimal precision."""
    return bytes_size / 1024

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
    directory_structure, file_contents, total_folders, total_files, total_lines, total_bytes = get_directory_structure_with_file_contents(
        current_dir, ignore_patterns
    )

    final_output = directory_structure + file_contents
    pyperclip.copy(final_output)

    print("Directory structure and file contents copied to clipboard.")
    
    # Convert total_bytes to kilobytes
    total_kilobytes = format_bytes_to_kb(total_bytes)

    # Print statistics with colored numbers (blue)
    print(f"  Total folders: {BLUE}{total_folders}{RESET}")
    print(f"  Total files: {BLUE}{total_files}{RESET}")
    print(f"  Total lines: {BLUE}{total_lines}{RESET}")
    print(f"  Total size: {BLUE}{total_kilobytes:.2f} KB{RESET}")