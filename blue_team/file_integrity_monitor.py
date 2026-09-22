#!/usr/bin/env python3
"""Create and compare SHA-256 file-integrity baselines.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def snapshot(root: Path, baseline: Path) -> dict[str, str]:
    """Return hashes indexed by stable, root-relative paths."""
    data: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.resolve() != baseline.resolve():
            try:
                data[str(path.relative_to(root))] = file_hash(path)
            except (OSError, PermissionError):
                continue
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--baseline", type=Path, default=Path("fim_baseline.json"))
    parser.add_argument("--init", action="store_true", help="Create or replace the baseline")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error("directory does not exist")
    current = snapshot(args.directory.resolve(), args.baseline)
    if args.init:
        args.baseline.write_text(json.dumps(current, indent=2), encoding="utf-8")
        print(f"Baseline created for {len(current)} files: {args.baseline}")
        return 0
    if not args.baseline.is_file():
        parser.error("baseline not found; run with --init first")
    previous = json.loads(args.baseline.read_text(encoding="utf-8"))
    added, removed = sorted(current.keys() - previous.keys()), sorted(previous.keys() - current.keys())
    changed = sorted(key for key in current.keys() & previous.keys() if current[key] != previous[key])
    for label, items in (("ADDED", added), ("REMOVED", removed), ("CHANGED", changed)):
        for item in items:
            print(f"{label:7} {item}")
    print(f"Summary: {len(added)} added, {len(removed)} removed, {len(changed)} changed")
    return 1 if added or removed or changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
