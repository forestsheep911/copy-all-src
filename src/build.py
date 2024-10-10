import os
import shutil
import stat


def build():
    os.system("pyinstaller --onefile --distpath dist src/main.py")
    if os.name == "nt":
        shutil.move("dist/main.exe", "dist/executable-windows-latest.exe")
        os.system(
            "powershell Compress-Archive -Path dist/executable-windows-latest.exe -DestinationPath dist/executable-windows-latest.zip"
        )
    else:
        shutil.move("dist/main", "dist/executable-linux-macos-latest")
        os.chmod("dist/executable-linux-macos-latest", stat.S_IRWXU)
        os.system(
            "zip -j dist/executable-linux-macos-latest.zip dist/executable-linux-macos-latest"
        )


if __name__ == "__main__":
    build()
