import os
from rich.console import Console
import pathspec
from ignore_loader import get_combined_ignore_patterns  # 使用统一的忽略模式加载器
from directory_structure import (
    generate_directory_structure,
    read_file_contents,
)  # 使用新的目录结构生成器和文件读取器
from file_checker import is_binary_file  # 导入 is_binary_file 函数

console = Console()


def process_include_only_paths(include_only_paths, verbose=False):
    directory_structure = ""
    file_contents = ""
    total_folders = 0
    total_files = 0
    total_bytes = 0

    # Load default ignore patterns
    ignore_patterns = get_combined_ignore_patterns([])  # 不传递额外的忽略模式
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

    for path in include_only_paths:
        if os.path.isdir(path):
            dir_structure, folders, files = generate_directory_structure(
                path, spec, verbose
            )
            directory_structure += dir_structure
            total_folders += folders
            total_files += files

            for root, _, files in os.walk(path):
                # Skip ignored directories
                if spec.match_file(os.path.relpath(root, path)):
                    continue

                for f in files:
                    # Skip ignored files
                    if spec.match_file(os.path.relpath(os.path.join(root, f), path)):
                        continue

                    file_path = os.path.join(root, f)
                    try:
                        if is_binary_file(file_path):
                            if verbose:
                                console.print(f"Ignored binary file: {file_path}")
                            continue
                    except Exception as e:
                        console.print(f"Error processing file {file_path}: {e}")
                        continue

                    content, bytes = read_file_contents(file_path, verbose)
                    file_contents += content
                    total_bytes += bytes
        elif os.path.isfile(path):
            try:
                if is_binary_file(path):
                    if verbose:
                        console.print(f"Ignored binary file: {path}")
                    continue
            except Exception as e:
                console.print(f"Error processing file {path}: {e}")
                continue

            total_files += 1
            directory_structure += "{}\n".format(path)
            content, bytes = read_file_contents(path, verbose)
            file_contents += content
            total_bytes += bytes
        else:
            console.print(
                f"[red]Warning: {path} is not a valid file or directory.[/red]"
            )

    return (
        directory_structure,
        file_contents,
        total_folders,
        total_files,
        total_bytes,
    )
