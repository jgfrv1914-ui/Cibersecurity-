#!/usr/bin/env python3
"""Generate cryptographically secure passwords or passphrases.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import secrets
import string

WORDS = (
    "anchor bamboo canyon comet copper eagle forest harbor "
    "lunar maple orchid pixel river solar velvet winter"
).split()


def random_password(length: int) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    while True:
        value = "".join(secrets.choice(alphabet) for _ in range(length))
        if all(any(c in group for c in value) for group in (string.ascii_lowercase,
               string.ascii_uppercase, string.digits, "!@#$%^&*()-_=+")):
            return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=int, default=20)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--passphrase", action="store_true", help="Generate six random words")
    args = parser.parse_args()
    if not 12 <= args.length <= 256 or not 1 <= args.count <= 100:
        parser.error("length must be 12-256 and count must be 1-100")
    for _ in range(args.count):
        print("-".join(secrets.choice(WORDS) for _ in range(6)) if args.passphrase else random_password(args.length))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
