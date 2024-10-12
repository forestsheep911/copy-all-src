import os
import mimetypes
import pathspec


def load_ignore_patterns(file_path):
    patterns = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns


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

            # Detect if file is binary
            mime_type, _ = mimetypes.guess_type(f)
            if mime_type and not mime_type.startswith("text/"):
                continue

            tree_str += "{}{}\n".format(subindent, f)

            # Read file content, calculate lines and size
            file_path = os.path.join(root, f)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()
                file_contents += f"\n=== {f} ===\n"
                file_contents += content + "\n"

                # Count lines and bytes
                total_lines += content.count("\n")
                total_bytes += os.path.getsize(file_path)

    return tree_str, file_contents, total_folders, total_files, total_lines, total_bytes
