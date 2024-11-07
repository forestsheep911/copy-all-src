# ds.py

import os
from indentation import get_indentation, get_sub_indentation
import pathspec


def generate_directory_structure(path, ignore_patterns, verbose=False):
    directory_structure = ""
    spec = pathspec.PathSpec.from_lines("gitwildmatch", ignore_patterns)

    for root, dirs, files in os.walk(path):
        dirs[:] = [
            d
            for d in dirs
            if not spec.match_file(os.path.relpath(os.path.join(root, d), path))
        ]

        if spec.match_file(os.path.relpath(root, path)):
            continue

        level = root.replace(path, "").count(os.sep)
        indent = get_indentation(level)
        directory_structure += "{}{}/\n".format(
            indent, os.path.basename(root) if root != path else ""
        )

        subindent = get_sub_indentation(level)
        for f in files:
            if spec.match_file(os.path.relpath(os.path.join(root, f), path)):
                continue
            directory_structure += "{}{}\n".format(subindent, f)

    return directory_structure
