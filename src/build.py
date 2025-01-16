import os
import shutil
import stat


def build():
    # 根据操作系统确定路径分隔符
    separator = ";" if os.name == "nt" else ":"

    # 构建 add-data 参数
    add_data = f"src{os.sep}version.py{separator}."

    # 构建完整的命令
    command = (
        f"pyinstaller --onefile "
        f"--add-data {add_data} "
        f"--hidden-import version "
        f"--distpath dist src{os.sep}main.py"
    )

    os.system(command)

    if os.name == "nt":
        shutil.move("dist/main.exe", "dist/cpsrc-win.exe")
    elif os.name == "posix":
        if "darwin" in os.uname().sysname.lower():
            shutil.move("dist/main", "dist/cpsrc-mac")
            os.chmod("dist/cpsrc-mac", stat.S_IRWXU)
        else:
            shutil.move("dist/main", "dist/cpsrc-linux")
            os.chmod("dist/cpsrc-linux", stat.S_IRWXU)


if __name__ == "__main__":
    build()
