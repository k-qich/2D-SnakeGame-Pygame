import sys
from cx_Freeze import setup, Executable

# python3 setup.py build

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], "include_files": ["sounds"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
        name = "Snake",
        version = "1.2",
        description = "Simple Snake Game",
        options = {"build_exe": build_exe_options},
        executables = [Executable("game.py", base=base)]
)
