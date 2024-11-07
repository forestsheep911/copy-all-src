# include.py

import os
from ds import generate_directory_structure
from fc import collect_file_contents
from pre_check import calculate_total_size


def process_include_paths(paths, ignore_patterns, verbose=False, max_size_kb=64):
    directory_structure = ""
    total_bytes = 0
    total_folders = 0
    total_files = 0

    for path in paths:
        if os.path.isdir(path):
            directory_structure += generate_directory_structure(
                path, ignore_patterns, verbose
            )
            total_bytes += calculate_total_size(path, ignore_patterns, verbose)
            total_folders += 1
            total_files += sum([len(files) for _, _, files in os.walk(path)])
        elif os.path.isfile(path):
            directory_structure += f"{path}\n"
            total_bytes += os.path.getsize(path)
            total_files += 1

    total_kilobytes = total_bytes / 1024

    # 在这里检查总大小是否超过限制
    if total_kilobytes > max_size_kb:
        return directory_structure, "", total_folders, total_files, total_bytes

    # 如果没有超过限制，才收集文件内容
    file_contents, _ = collect_file_contents(paths, ignore_patterns, verbose)
    return directory_structure, file_contents, total_folders, total_files, total_bytes
