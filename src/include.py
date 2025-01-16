# include.py

import os
import pathspec
from ds import generate_directory_structure
from fc import collect_file_contents
from pre_check import calculate_total_size


def process_include_paths(paths, ignore_patterns, verbose=False, max_size_kb=64):
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)
    directory_structure = ""
    total_bytes = 0
    total_folders = 0
    total_files = 0

    # 确保 paths 是列表
    if isinstance(paths, str):
        paths = [paths]

    for path in paths:
        if os.path.isdir(path):
            # 处理目录
            for root, dirs, files in os.walk(path):
                rel_root = os.path.relpath(root, path)

                # 如果当前文件夹不被忽略，计数加1（根目录除外）
                if root != path and not spec.match_file(rel_root):
                    total_folders += 1

                # 过滤不被忽略的文件并计数
                for f in files:
                    if not spec.match_file(os.path.join(rel_root, f)):
                        total_files += 1
                        total_bytes += os.path.getsize(os.path.join(root, f))

            # 生成目录结构
            directory_structure += generate_directory_structure(
                path, ignore_patterns, verbose
            )

        elif os.path.isfile(path):
            # 处理单个文件
            # 检查文件是否被忽略
            if not spec.match_file(path):
                directory_structure += f"{path}\n"
                total_files += 1
                total_bytes += os.path.getsize(path)

    total_kilobytes = total_bytes / 1024

    # 检查是否超过大小限制
    if total_kilobytes > max_size_kb:
        return directory_structure, "", total_folders, total_files, total_bytes

    # 收集文件内容
    file_contents, _ = collect_file_contents(paths, ignore_patterns, verbose)

    return directory_structure, file_contents, total_folders, total_files, total_bytes
