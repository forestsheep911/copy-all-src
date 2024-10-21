import os
import mimetypes
import pathspec
import magic  # 导入 python-magic-bin 库


def load_ignore_patterns(file_path):
    patterns = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns


def is_binary_file(file_path):
    """使用 python-magic 检测文件是否是二进制文件"""
    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)
        return not mime_type.startswith("text/")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return True  # 认为文件是二进制文件


def get_directory_structure_with_file_contents(root_dir, ignore_patterns):
    tree_str = root_dir + "\n"
    file_contents = "\n"
    total_folders = 0
    total_files = 0
    total_lines = 0
    total_bytes = 0
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

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
        indent = "│   " * level + "├── " if level > 0 else ""
        tree_str += "{}{}/\n".format(
            indent, os.path.basename(root) if root != root_dir else ""
        )

        subindent = "│   " * (level + 1) + "├── "
        for f in files:
            # Skip ignored files
            if spec.match_file(os.path.relpath(os.path.join(root, f), root_dir)):
                continue

            # Increment file count
            total_files += 1

            file_path = os.path.join(root, f)
            try:
                if is_binary_file(file_path):
                    mime = magic.Magic(mime=True)
                    mime_type = mime.from_file(file_path)
                    print(f"Ignored binary file: {file_path} (MIME type: {mime_type})")
                    continue
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                continue

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
                print(f"Error reading file {file_path}: {e}")
                continue

    return tree_str, file_contents, total_folders, total_files, total_lines, total_bytes
