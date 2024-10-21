import os
from rich.console import Console
from utils import load_ignore_patterns
import pathspec

console = Console()


def process_include_only_paths(include_only_paths):
    directory_structure = ""
    file_contents = ""
    total_folders = 0
    total_files = 0
    total_lines = 0
    total_bytes = 0

    # Load default ignore patterns
    default_ignore_path = os.path.join(os.path.dirname(__file__), "default_ignore.py")
    default_ignore_patterns = load_ignore_patterns(default_ignore_path)
    spec = pathspec.PathSpec.from_lines("gitwildmatch", default_ignore_patterns)

    for path in include_only_paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                # Skip ignored directories
                dirs[:] = [
                    d
                    for d in dirs
                    if not spec.match_file(os.path.relpath(os.path.join(root, d), path))
                ]

                # Check if the current directory itself should be ignored
                if spec.match_file(os.path.relpath(root, path)):
                    continue

                total_folders += 1
                level = root.replace(path, "").count(os.sep)
                indent = "│   " * level + "├── " if level > 0 else ""
                directory_structure += "{}{}/\n".format(
                    indent, os.path.basename(root) if root != path else ""
                )
                subindent = "│   " * (level + 1) + "├── "
                for f in files:
                    # Skip ignored files
                    if spec.match_file(os.path.relpath(os.path.join(root, f), path)):
                        continue

                    total_files += 1
                    file_path = os.path.join(root, f)
                    directory_structure += "{}{}\n".format(subindent, f)
                    with open(
                        file_path, "r", encoding="utf-8", errors="ignore"
                    ) as file:
                        content = file.read()
                        file_contents += f"\n=== {file_path} ===\n"
                        file_contents += content + "\n"
                        total_lines += content.count("\n")
                        total_bytes += os.path.getsize(file_path)
        elif os.path.isfile(path):
            total_files += 1
            directory_structure += "{}\n".format(path)
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                file_contents += f"\n=== {path} ===\n"
                file_contents += content + "\n"
                total_lines += content.count("\n")
                total_bytes += os.path.getsize(path)
        else:
            console.print(
                f"[red]Warning: {path} is not a valid file or directory.[/red]"
            )

    return (
        directory_structure,
        file_contents,
        total_folders,
        total_files,
        total_lines,
        total_bytes,
    )
