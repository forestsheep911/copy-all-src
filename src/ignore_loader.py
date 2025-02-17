# ignore_loader.py

import os
from default_ignore import default_ignore_patterns


def load_ignore_patterns(file_path):
    patterns = []
    if os.path.exists(file_path):
        print(f"Loading ignore patterns from: {file_path}")  # 调试信息
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    else:
        print(f"Ignore config file not found: {file_path}")  # 调试信息
    return patterns


def get_combined_ignore_patterns(additional_ignore, ignore_config_path=None):
    additional_ignore_patterns = set(additional_ignore)

    # 加载默认忽略模式
    additional_ignore_patterns.update(default_ignore_patterns)

    # Load patterns from specified ignore config file if provided
    if ignore_config_path:
        ignore_config_abs_path = os.path.abspath(ignore_config_path)
        print(f"Using ignore config file: {ignore_config_abs_path}")  # 调试信息
        user_ignore_patterns = load_ignore_patterns(ignore_config_abs_path)
        additional_ignore_patterns.update(user_ignore_patterns)

    return list(additional_ignore_patterns)
