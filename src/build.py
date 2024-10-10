import os
import shutil
import stat


def build():
    os.system("pyinstaller --onefile --distpath dist src/main.py")
    if os.name == "nt":
        shutil.move("dist/main.exe", "dist/cpsrc.exe")
        shutil.move("dist/main.exe", "dist/cpsrc-win.exe")
    elif os.name == "posix":
        if "darwin" in os.uname().sysname.lower():
            shutil.move("dist/main", "dist/cpsrc")
            os.chmod("dist/cpsrc", stat.S_IRWXU)
            shutil.move("dist/main", "dist/cpsrc-mac")
            os.chmod("dist/cpsrc-mac", stat.S_IRWXU)
        else:
            shutil.move("dist/main", "dist/cpsrc")
            os.chmod("dist/cpsrc", stat.S_IRWXU)
            shutil.move("dist/main", "dist/cpsrc-linux")
            os.chmod("dist/cpsrc-linux", stat.S_IRWXU)
