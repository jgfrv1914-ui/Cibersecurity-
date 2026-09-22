#!/usr/bin/env python3
"""Assess password quality locally without storing the password.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import getpass
import math
import re

COMMON = {"123456", "password", "qwerty", "admin", "letmein", "welcome", "password1"}


def analyze(password: str) -> dict[str, object]:
    """Return transparent checks, an approximate entropy value, and advice."""
    pools = sum(size for pattern, size in ((r"[a-z]", 26), (r"[A-Z]", 26),
                (r"\d", 10), (r"[^\w\s]", 33)) if re.search(pattern, password))
    checks = {
        "at_least_12_characters": len(password) >= 12,
        "at_least_16_characters": len(password) >= 16,
        "not_common": password.casefold() not in COMMON,
        "no_obvious_sequence": not any(x in password.casefold() for x in ("1234", "abcd", "qwerty")),
    }
    score = min(100, len(password) * 4 + 15 * sum(checks.values()))
    advice = []
    if len(password) < 12:
        advice.append("Use at least 12 characters; a long passphrase is preferable.")
    if not checks["not_common"]:
        advice.append("Replace this commonly used password.")
    if not checks["no_obvious_sequence"]:
        advice.append("Remove predictable keyboard or numeric sequences.")
    return {"length": len(password), "entropy_bits": round(len(password) * math.log2(pools), 1) if pools else 0,
            "score": score, "checks": checks, "advice": advice}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--password", help="Avoid this option on shared systems; it may enter shell history")
    args = parser.parse_args()
    report = analyze(args.password if args.password is not None else getpass.getpass("Password: "))
    print(
        f"Length: {report['length']} | "
        f"Estimated entropy: {report['entropy_bits']} bits | "
        f"Score: {report['score']}/100"
    )
    for name, passed in report["checks"].items():
        print(f"[{'PASS' if passed else 'FAIL'}] {name.replace('_', ' ')}")
    for item in report["advice"]:
        print(f"Advice: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
