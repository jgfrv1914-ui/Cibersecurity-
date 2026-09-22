#!/usr/bin/env python3
"""Calculate Shannon entropy to triage compressed, encrypted, or packed files.

Author: Fernando Tafurt Pinto
"""
import argparse
import collections
import math
from pathlib import Path


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = collections.Counter(data)
    return -sum((n / len(data)) * math.log2(n / len(data)) for n in counts.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--threshold", type=float, default=7.5)
    args = parser.parse_args()
    for path in args.paths:
        try:
            score = entropy(path.read_bytes())
        except OSError as exc:
            print(f"ERROR {path}: {exc}")
            continue
        note = "high entropy; investigate context" if score >= args.threshold else "normal/low entropy"
        print(f"{score:.3f} bits/byte  {note:32} {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
