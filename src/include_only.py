import os
from rich.console import Console
from file_utils import calculate_total_size, collect_file_contents
from directory_structure import generate_directory_structure

console = Console()


from directory_structure import generate_directory_structure


def process_include_only_paths(include_only_paths, spec, verbose=False):
    total_folders = 0
    total_files = 0
    total_bytes = 0
    directory_structure = ""

    for path in include_only_paths:
        if os.path.isdir(path):
            total_folders += sum([len(dirs) for _, dirs, _ in os.walk(path)])
            total_files += sum([len(files) for _, _, files in os.walk(path)])
            total_bytes += calculate_total_size(path, spec, verbose)
            directory_structure += generate_directory_structure(path, spec, verbose)
        elif os.path.isfile(path):
            try:
                file_size = os.path.getsize(path)
                total_bytes += file_size
                directory_structure += f"{path}\n"
                if verbose:
                    console.print(f"File: {path}, Size: {file_size / 1024:.2f} KB")
            except Exception as e:
                console.print(f"Error processing file {path}: {e}")

    return directory_structure, total_folders, total_files, total_bytes


def collect_include_only_contents(include_only_paths, spec, verbose=False):
    directory_structure = ""
    file_contents = ""
    total_bytes = 0

    for path in include_only_paths:
        if os.path.isdir(path):
            # 只解包两个返回值
            contents, bytes_collected = collect_file_contents(path, spec, verbose)
            directory_structure += generate_directory_structure(path, spec, verbose)
            file_contents += contents
            total_bytes += bytes_collected
        elif os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    file_contents += f"\n=== {path} ===\n"
                    file_contents += content + "\n"
                    total_bytes += os.path.getsize(path)
            except Exception as e:
                console.print(f"Error reading file {path}: {e}")

    return directory_structure, file_contents, total_bytes
