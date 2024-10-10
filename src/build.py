import os
import shutil
import stat


def build():
    os.system("pyinstaller --onefile --distpath dist src/main.py")
    if os.name == "nt":
        shutil.move("dist/main.exe", "dist/cpsrc.exe")
    else:
        shutil.move("dist/main", "dist/cpsrc")
        os.chmod("dist/cpsrc", stat.S_IRWXU)


if __name__ == "__main__":
    build()
