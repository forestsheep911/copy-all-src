# main.py

import os
import pyperclip
import argparse
from rich.console import Console
from ignore_loader import get_combined_ignore_patterns
from include import process_include_paths
from exclude import process_exclude_paths
from version import VERSION

# Initialize rich console
console = Console()


def main():
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
        help="show program's version number and exit",
    )
    parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="additional patterns to ignore (files and directories)",
    )
    parser.add_argument(
        "--igfile", type=str, help="path to additional ignore config file"
    )
    parser.add_argument(
        "--include",
        nargs="*",
        help="specific files or directories to include exclusively",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="display detailed debug information"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=64,
        help="maximum size (in KB) to copy to clipboard (default: 64KB)",
    )
    args = parser.parse_args()

    ignore_patterns = get_combined_ignore_patterns(args.ignore, args.igfile)
    if args.include:
        include_paths = set(args.include)
        directory_structure, file_contents, total_folders, total_files, total_bytes = (
            process_include_paths(
                include_paths, ignore_patterns, args.verbose, args.max_size
            )
        )
    else:
        current_dir = os.getcwd()
        directory_structure, file_contents, total_folders, total_files, total_bytes = (
            process_exclude_paths(
                current_dir, ignore_patterns, args.verbose, args.max_size
            )
        )

    total_kilobytes = total_bytes / 1024

    if total_kilobytes > args.max_size:
        console.print(
            f"[orange1]Warning: The content size is [bold red]{total_kilobytes:.2f} KB[/bold red], which exceeds the maximum allowed size of {args.max_size} KB.\nThe content was [bold red]not copied[/bold red] to the clipboard.[/orange1]\n[orange1]You can change the maximum allowed size using the [bold light_green]--max-size[/bold light_green] parameter.[/orange1]"
        )
        return

    final_output = directory_structure + file_contents
    pyperclip.copy(final_output)

    # Custom color
    color1 = "#398BFF"
    color2 = "#A82FCC"
    color3 = "#FFA209"
    console.print(
        f"[{color1}]{total_folders}[/{color1}] folders [{color2}]{total_files}[/{color2}] files [{color3}]{total_kilobytes:.2f}[/{color3}] KB copied"
    )


if __name__ == "__main__":
    main()
