#!/usr/bin/env python3
"""Find world-writable files and directories without changing permissions.

Author: Fernando Tafurt Pinto
"""
import argparse
import stat
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error("directory does not exist")
    findings = 0
    for path in args.directory.rglob("*"):
        try:
            mode = path.stat().st_mode
        except OSError:
            continue
        if mode & stat.S_IWOTH:
            findings += 1
            print(f"WORLD-WRITABLE {stat.filemode(mode)} {path}")
    print(f"Findings: {findings}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
