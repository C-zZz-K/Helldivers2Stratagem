# build.py
import os
import subprocess

def build_exe():
    command = [
        "pyinstaller",
        "--onefile",
        "--windowed",  # 如果你的程序没有命令行界面，可以使用 --windowed 隐藏控制台
        # 添加其他选项，如 --icon=your_icon.ico
    ]

    # 添加数据文件夹
    data_folders = [
        "sounds", "music", "menu", "arrow", "icons", "stratagem", "fonts"
    ]
    for folder in data_folders:
        command.append(f"--add-data={folder}{os.sep}*;{folder}")

    command.append("main.py") #放在最后

    # 执行命令
    subprocess.run(command)
    print(command)

if __name__ == "__main__":
    build_exe()