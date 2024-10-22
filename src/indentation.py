def get_indentation(level):
    """
    根据层级返回相应的缩进字符串。
    """
    return "│   " * level + "├── " if level > 0 else ""


def get_sub_indentation(level):
    """
    根据层级返回相应的子缩进字符串。
    """
    return "│   " * (level + 1) + "├── "
