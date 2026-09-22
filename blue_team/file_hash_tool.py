#!/usr/bin/env python3
"""Calculate and verify cryptographic file or text digests.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
from pathlib import Path

SAFE_ALGORITHMS = ("sha256", "sha384", "sha512", "sha3_256")


def digest_file(path: Path, algorithm: str) -> str:
    """Hash a file incrementally so large files do not fill memory."""
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    parser.add_argument("--algorithm", choices=SAFE_ALGORITHMS, default="sha256")
    parser.add_argument("--verify", help="Expected hexadecimal digest")
    args = parser.parse_args()
    if args.file and not args.file.is_file():
        parser.error("--file must point to a readable file")
    actual = digest_file(args.file, args.algorithm) if args.file else hashlib.new(
        args.algorithm, args.text.encode("utf-8")).hexdigest()
    print(f"{args.algorithm.upper()}: {actual}")
    if args.verify:
        valid = hmac.compare_digest(actual.casefold(), args.verify.strip().casefold())
        print("VERIFIED" if valid else "MISMATCH")
        return 0 if valid else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
