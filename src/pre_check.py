# pre_check.py

import os
import pathspec
from rich.console import Console
from rich.markup import escape

console = Console()


def print_file_info(file_path, file_size):
    escaped_file_path = escape(file_path)
    console.print(f"File: {escaped_file_path}, Size: {file_size / 1024:.2f} KB")


def calculate_total_size(path, ignore_patterns, verbose=False):
    total_bytes = 0
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

    # 用于存储每个目录的大小
    directory_sizes = {}

    for root, dirs, files in os.walk(path):
        if spec.match_file(os.path.relpath(root, path)):
            continue

        # 计算当前目录的大小
        directory_size = 0
        for f in files:
            file_path = os.path.join(root, f)
            if spec.match_file(os.path.relpath(file_path, path)):
                continue

            try:
                file_size = os.path.getsize(file_path)
                directory_size += file_size
                if verbose:
                    # 输出每个文件的大小
                    print_file_info(file_path, file_size)
            except Exception as e:
                if verbose:
                    console.print(f"Error processing file {file_path}: {e}")

        # 将当前目录的大小加入到总大小中
        total_bytes += directory_size

        # 存储当前目录的大小
        directory_sizes[root] = directory_size

        # 输出当前目录的总大小
        if verbose:
            console.print(
                f"Directory: {root}, Total Size: {directory_size / 1024:.2f} KB"
            )

    return total_bytes
