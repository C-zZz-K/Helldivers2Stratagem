# build.py
import os
import subprocess
import platform  # 导入 platform 模块


def build_exe():
    command = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--icon=./icons/icon.png",
        "--name=HELLDIVERS2 Stratagems",
    ]

    data_folders = [
        "sounds",
        "music",
        "menu",
        "arrow",
        "icons",
        "stratagem",
        "fonts",
    ]

    # 根据操作系统选择正确的分隔符
    path_separator = ":" if platform.system() != "Windows" else ";" # Corrected separator logic

    for folder in data_folders:
        # 正确的 --add-data 格式： SOURCE:DEST
        command.append(f"--add-data={folder}{path_separator}{folder}")

    command.append("main.py")

    subprocess.run(command)
    print(command)


if __name__ == "__main__":
    build_exe()