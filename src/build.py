import os

def build():
    os.system("pyinstaller --onefile src/main.py")

if __name__ == "__main__":
    build()