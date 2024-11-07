import os
from rich.console import Console
from file_utils import calculate_total_size
import pathspec

console = Console()

from indentation import get_indentation, get_sub_indentation


def generate_directory_structure(path, spec, verbose=False):
    directory_structure = ""
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

        level = root.replace(path, "").count(os.sep)
        indent = get_indentation(level)
        directory_structure += "{}{}/\n".format(
            indent, os.path.basename(root) if root != path else ""
        )

        subindent = get_sub_indentation(level)
        for f in files:
            # Skip ignored files
            if spec.match_file(os.path.relpath(os.path.join(root, f), path)):
                continue

            directory_structure += "{}{}\n".format(subindent, f)

    return directory_structure


def get_directory_structure_with_file_contents(
    root_dir, ignore_patterns, verbose=False
):
    tree_str = root_dir + "\n"
    file_contents = "\n"
    total_folders = 0
    total_files = 0
    total_lines = 0
    total_bytes = 0
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

    # 先计算总大小，输出每个文件的大小
    total_bytes = calculate_total_size(root_dir, spec, verbose)

    for root, dirs, files in os.walk(root_dir):
        # Skip ignored directories
        dirs[:] = [
            d
            for d in dirs
            if not spec.match_file(os.path.relpath(os.path.join(root, d), root_dir))
        ]

        # Check if the current directory itself should be ignored
        if spec.match_file(os.path.relpath(root, root_dir)):
            continue

        # Increment folder count
        total_folders += 1

        level = root.replace(root_dir, "").count(os.sep)
        indent = get_indentation(level)
        tree_str += "{}{}/\n".format(
            indent, os.path.basename(root) if root != root_dir else ""
        )

        subindent = get_sub_indentation(level)
        for f in files:
            # Skip ignored files
            if spec.match_file(os.path.relpath(os.path.join(root, f), root_dir)):
                continue

            # Increment file count
            total_files += 1

            file_path = os.path.join(root, f)
            tree_str += "{}{}\n".format(subindent, f)

            # Read file content, calculate lines and size
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    file_contents += f"\n=== {f} ===\n"
                    file_contents += content + "\n"

                    # Count lines and bytes
                    total_lines += content.count("\n")
                    total_bytes += os.path.getsize(file_path)
            except Exception as e:
                console.print(f"Error reading file {file_path}: {e}")
                continue

    return tree_str, file_contents, total_folders, total_files, total_bytes


def read_file_contents(file_path, verbose=False):
    """读取文件内容并统计字节数"""
    total_bytes = 0
    file_contents = ""

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()
            file_contents += f"\n=== {file_path} ===\n"
            file_contents += content + "\n"

            # Count bytes
            total_bytes += os.path.getsize(file_path)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

    return file_contents, total_bytes
