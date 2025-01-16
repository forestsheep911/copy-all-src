# exclude.py

import os
import pathspec  # 添加这行导入
from ds import generate_directory_structure
from fc import collect_file_contents
from pre_check import calculate_total_size


def process_exclude_paths(path, ignore_patterns, verbose=False, max_size_kb=64):
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

    # 修改统计逻辑
    total_folders = 0
    total_files = 0

    # 统计实际会被拷贝的文件夹和文件数量
    for root, dirs, files in os.walk(path):
        rel_root = os.path.relpath(root, path)

        # 如果当前文件夹不被忽略，计数加1（根目录除外）
        if root != path and not spec.match_file(rel_root):
            total_folders += 1

        # 过滤不被忽略的文件并计数
        for f in files:
            if not spec.match_file(os.path.join(rel_root, f)):
                total_files += 1

    directory_structure = generate_directory_structure(path, ignore_patterns, verbose)
    total_bytes = calculate_total_size(path, ignore_patterns, verbose)

    total_kilobytes = total_bytes / 1024
    if total_kilobytes > max_size_kb:
        return directory_structure, "", 0, 0, total_bytes

    file_contents, _ = collect_file_contents(path, ignore_patterns, verbose)

    return directory_structure, file_contents, total_folders, total_files, total_bytes
