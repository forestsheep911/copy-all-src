import os
import pyperclip
import argparse
import fnmatch


def get_directory_structure_with_file_contents(
    root_dir, additional_ignored_files=None, additional_ignored_dirs=None
):
    tree_str = root_dir + "\n"
    file_contents = "\n"
    ignored_directories = {".git", "dist", "build"}
    if additional_ignored_dirs:
        ignored_directories.update(additional_ignored_dirs)
    ignored_files = {
        "LICENSE",
        "README.md",
        ".gitignore",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.spec",
    }
    if additional_ignored_files:
        ignored_files.update(additional_ignored_files)

    for root, dirs, files in os.walk(root_dir):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_directories]

        level = root.replace(root_dir, "").count(os.sep)
        indent = "│   " * level + "├── " if level > 0 else ""
        tree_str += "{}{}/\n".format(
            indent, os.path.basename(root) if root != root_dir else ""
        )

        subindent = "│   " * (level + 1) + "├── "
        for f in files:
            # Skip ignored files
            if any(fnmatch.fnmatch(f, pattern) for pattern in ignored_files):
                continue

            tree_str += "{}{}\n".format(subindent, f)
            with open(
                os.path.join(root, f), "r", encoding="utf-8", errors="ignore"
            ) as file:
                file_contents += f"\n=== {f} ===\n"
                file_contents += file.read() + "\n"

    return tree_str, file_contents


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument(
        "--ignore", nargs="*", default=[], help="additional file types to ignore"
    )
    parser.add_argument(
        "--ignore-dir", nargs="*", default=[], help="additional directories to ignore"
    )
    args = parser.parse_args()
    additional_ignored_files = set(args.ignore)
    additional_ignored_dirs = set(args.ignore_dir)
    current_dir = os.getcwd()
    directory_structure, file_contents = get_directory_structure_with_file_contents(
        current_dir, additional_ignored_files
    )
    final_output = directory_structure + file_contents
    pyperclip.copy(final_output)
    print("Directory structure and file contents copied to clipboard.")
