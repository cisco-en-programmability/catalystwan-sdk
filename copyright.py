# Copyright 2024 Cisco Systems, Inc. and its affiliates

import re
from datetime import datetime
from pathlib import Path

COPYRIGHT_NOTICE = f"# Copyright {datetime.now().year} Cisco Systems, Inc. and its affiliates"
COPYRIGHT_PATTERN = r"^#.*copyright.*cisco.*$"
SUBDIRS = ["catalystwan", "examples"]


def check_if_copyright_present(file_path):
    try:
        with file_path.open("r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            if re.search(COPYRIGHT_PATTERN, first_line, re.IGNORECASE):
                return True
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return False


def scan_and_update(dir_path):
    directory = Path(dir_path)
    if not directory.is_dir():
        print(f"The provided path '{dir_path}' is not a valid directory.")
        return

    for file_path in directory.rglob("*.py"):
        if file_path.stat().st_size == 0:
            continue
        if not check_if_copyright_present(file_path):
            with open(file_path, "r+") as file:
                content = file.read()
                file.seek(0)
                file.write(COPYRIGHT_NOTICE + "\n" + content)


if __name__ == "__main__":
    for dir in SUBDIRS:
        scan_and_update(dir)
