# file_utils.py

import os
from rich.console import Console

console = Console()


def calculate_total_size(path, spec, verbose=False):
    total_bytes = 0
    for root, _, files in os.walk(path):
        if spec.match_file(os.path.relpath(root, path)):
            continue

        for f in files:
            file_path = os.path.join(root, f)
            if spec.match_file(os.path.relpath(file_path, path)):
                continue

            try:
                file_size = os.path.getsize(file_path)
                total_bytes += file_size
                if verbose:
                    console.print(f"File: {file_path}, Size: {file_size / 1024:.2f} KB")
            except Exception as e:
                console.print(f"Error processing file {file_path}: {e}")

    return total_bytes


def collect_file_contents(path, spec, verbose=False):
    file_contents = ""
    total_bytes = 0

    for root, _, files in os.walk(path):
        if spec.match_file(os.path.relpath(root, path)):
            continue

        for f in files:
            file_path = os.path.join(root, f)
            if spec.match_file(os.path.relpath(file_path, path)):
                continue

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    file_contents += f"\n=== {file_path} ===\n"
                    file_contents += content + "\n"
                    total_bytes += os.path.getsize(file_path)
            except Exception as e:
                console.print(f"Error reading file {file_path}: {e}")

    return file_contents, total_bytes
