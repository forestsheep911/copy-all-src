# exclude.py

import os
from ds import generate_directory_structure
from fc import collect_file_contents
from pre_check import calculate_total_size


def process_exclude_paths(path, ignore_patterns, verbose=False, max_size_kb=64):
    directory_structure = generate_directory_structure(path, ignore_patterns, verbose)
    total_bytes = calculate_total_size(path, ignore_patterns, verbose)

    total_kilobytes = total_bytes / 1024

    # 在这里检查总大小是否超过限制
    if total_kilobytes > max_size_kb:
        return directory_structure, "", 0, 0, total_bytes

    # 如果没有超过限制，才收集文件内容
    file_contents, _ = collect_file_contents(path, ignore_patterns, verbose)
    total_files = sum([len(files) for _, _, files in os.walk(path)])
    total_folders = sum([len(dirs) for _, dirs, _ in os.walk(path)])

    return directory_structure, file_contents, total_folders, total_files, total_bytes
