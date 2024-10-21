import os
import pyperclip
import argparse
from rich.console import Console
from utils import load_ignore_patterns, get_directory_structure_with_file_contents
from include_only import process_include_only_paths
from default_ignore import default_ignore_patterns  # 导入默认忽略模式

# Initialize rich console
console = Console()

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
    parser.add_argument(
        "--include-only",
        nargs="*",
        help="specific files or directories to include exclusively",
    )
    args = parser.parse_args()

    additional_ignore_patterns = set(args.ignore)

    # 加载默认忽略模式
    additional_ignore_patterns.update(default_ignore_patterns)

    # Load patterns from .gitignore if it exists
    gitignore_patterns = load_ignore_patterns(".gitignore")
    additional_ignore_patterns.update(gitignore_patterns)

    # Load patterns from specified ignore config file if provided
    if args.ignore_config:
        user_ignore_patterns = load_ignore_patterns(args.ignore_config)
        additional_ignore_patterns.update(user_ignore_patterns)

    ignore_patterns = list(additional_ignore_patterns)

    if args.include_only:
        # If include-only is specified, only process specified files or directories
        include_only_paths = set(args.include_only)
        (
            directory_structure,
            file_contents,
            total_folders,
            total_files,
            total_lines,
            total_bytes,
        ) = process_include_only_paths(include_only_paths)

        final_output = directory_structure + file_contents
        pyperclip.copy(final_output)
    else:
        current_dir = os.getcwd()
        (
            directory_structure,
            file_contents,
            total_folders,
            total_files,
            total_lines,
            total_bytes,
        ) = get_directory_structure_with_file_contents(current_dir, ignore_patterns)

        final_output = directory_structure + file_contents
        pyperclip.copy(final_output)

    # Convert total_bytes to kilobytes
    total_kilobytes = total_bytes / 1024

    # Custom color
    custom_color1 = "#398BFF"
    custom_color2 = "#A82FCC"
    custom_color3 = "#FFA209"

    # Print simplified statistics with custom colored numbers using rich
    console.print(
        f"[{custom_color1}]{total_folders}[/{custom_color1}] folders "
        f"[{custom_color2}]{total_files}[/{custom_color2}] files "
        f"[{custom_color3}]{total_kilobytes:.2f}[/{custom_color3}] KB copied"
    )
