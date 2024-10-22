import os
import pyperclip
import argparse
from rich.console import Console
import pathspec
from directory_structure import get_directory_structure_with_file_contents
from include_only import process_include_only_paths
from ignore_loader import get_combined_ignore_patterns  # 导入新的忽略模式加载器

# Initialize rich console
console = Console()


def main():
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
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="display detailed debug information",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=64,
        help="maximum size (in KB) to copy to clipboard (default: 64KB)",
    )
    args = parser.parse_args()

    ignore_patterns = get_combined_ignore_patterns(args.ignore, args.ignore_config)
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

    if args.include_only:
        # If include-only is specified, only process specified files or directories
        include_only_paths = set(args.include_only)
        (
            directory_structure,
            file_contents,
            total_folders,
            total_files,
            total_bytes,
        ) = process_include_only_paths(include_only_paths, args.verbose)

        final_output = directory_structure + file_contents
    else:
        current_dir = os.getcwd()
        (
            directory_structure,
            file_contents,
            total_folders,
            total_files,
            total_bytes,
        ) = get_directory_structure_with_file_contents(current_dir, spec, args.verbose)

        final_output = directory_structure + file_contents

    # Convert total_bytes to kilobytes
    total_kilobytes = total_bytes / 1024

    # Check if the total size exceeds the max size
    if total_kilobytes > args.max_size:
        console.print(
            f"[orange1]Warning: The content size is [bold red]{total_kilobytes:.2f} KB[/bold red], which exceeds the maximum allowed size of {args.max_size} KB.\nThe content was [bold red]not copied[/bold red] to the clipboard.[/orange1]\n"
            f"[orange1]You can change the maximum allowed size using the [bold]--max-size[/bold] parameter.[/orange1]"
        )
    else:
        pyperclip.copy(final_output)
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


if __name__ == "__main__":
    main()
