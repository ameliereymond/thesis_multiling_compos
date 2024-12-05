import os
from pathlib import Path
import stat

def assert_exists(file_path: Path):
    if not file_path.exists():
        raise Exception(f"Expected {file_path.absolute()} to exist")

def mkdirp(folder_path: Path):
    os.makedirs(folder_path, exist_ok=True)

def chmodx(file_path: Path):
    st = os.stat(file_path).st_mode
    os.chmod(file_path, st | stat.S_IEXEC)