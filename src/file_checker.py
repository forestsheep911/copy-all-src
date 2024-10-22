import magic  # 导入 python-magic-bin 库


def is_binary_file(file_path):
    """使用 python-magic 检测文件是否是二进制文件"""
    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)
        return not mime_type.startswith("text/")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return True  # 认为文件是二进制文件
