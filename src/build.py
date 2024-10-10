import os

def build():
    os.system("pyinstaller --onefile --distpath dist src/main.py")

if __name__ == "__main__":
    build()