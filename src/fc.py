import os
import pathspec
from rich.console import Console
import time

console = Console()


def collect_file_contents(paths, ignore_patterns, verbose=False):
    file_contents = ""
    total_bytes = 0
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)
    # 如果 paths 是字符串（单个路径），将其转换为列表
    if isinstance(paths, str):
        paths = [paths]
    for path in paths:
        for root, _, files in os.walk(path):
            if spec.match_file(os.path.relpath(root, path)):
                continue

            for f in files:
                file_path = os.path.join(root, f)
                if spec.match_file(os.path.relpath(file_path, path)):
                    continue

                try:
                    with open(
                        file_path, "r", encoding="utf-8", errors="ignore"
                    ) as file:
                        # Add file path header before the content
                        file_contents += f"\n=== {file_path} ===\n"
                        for line in file:
                            file_contents += line
                    total_bytes += os.path.getsize(file_path)
                except Exception as e:
                    if verbose:
                        console.print(f"Error reading file {file_path}: {e}")

    return file_contents, total_bytes
