#!/usr/bin/env python3
"""Assess password quality locally without storing the password.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import getpass
import math
import re

# Common bases, not complete passwords. Appending digits or punctuation to one
# of these ("password123", "Qwerty!") does not make it unpredictable, because
# that is precisely the mutation cracking tools apply first.
COMMON_BASES = {
    "123456", "password", "qwerty", "admin", "letmein", "welcome", "abc",
    "iloveyou", "monkey", "dragon", "football", "master", "sunshine",
    "princess", "login", "passw0rd", "starwars", "superman", "trustno",
}
SEQUENCES = ("1234", "2345", "3456", "abcd", "bcde", "qwerty", "asdf", "zxcv", "0000", "1111")
LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})


def _base_form(password: str) -> str:
    """Reduce a password to the base an attacker would start from."""
    folded = password.casefold().translate(LEET)
    return re.sub(r"[^a-z]", "", folded)


def is_common(password: str) -> bool:
    """True when the password is a known weak base, possibly with decorations."""
    folded = password.casefold()
    base = _base_form(password)
    if folded in COMMON_BASES or base in COMMON_BASES:
        return True
    # "password123", "Admin!2024", "P@ssw0rd" all reduce to a known base.
    return any(base.startswith(common) or common in base for common in COMMON_BASES if len(common) >= 5)


def analyze(password: str) -> dict[str, object]:
    """Return transparent checks, an approximate entropy value, and advice."""
    pools = sum(size for pattern, size in ((r"[a-z]", 26), (r"[A-Z]", 26),
                (r"\d", 10), (r"[^\w\s]", 33)) if re.search(pattern, password))
    common = is_common(password)
    checks = {
        "at_least_12_characters": len(password) >= 12,
        "at_least_16_characters": len(password) >= 16,
        "not_common": not common,
        "no_obvious_sequence": not any(x in password.casefold() for x in SEQUENCES),
    }
    # Character-set entropy is an upper bound that assumes every character was
    # chosen at random. It is meaningless for a dictionary word plus a suffix,
    # so a recognisably common password is capped regardless of its length.
    entropy = round(len(password) * math.log2(pools), 1) if pools else 0.0
    score = min(100, len(password) * 4 + 15 * sum(checks.values()))
    if common:
        score = min(score, 20)

    advice = []
    if len(password) < 12:
        advice.append("Use at least 12 characters; a long passphrase is preferable.")
    if common:
        advice.append("This is a well-known password or a decorated version of one; choose an unrelated phrase.")
    if not checks["no_obvious_sequence"]:
        advice.append("Remove predictable keyboard or numeric sequences.")
    return {
        "length": len(password),
        "entropy_bits": entropy,
        "entropy_note": "upper bound; assumes every character was chosen at random",
        "score": score,
        "checks": checks,
        "advice": advice,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--password", help="Avoid this option on shared systems; it may enter shell history")
    args = parser.parse_args()
    report = analyze(args.password if args.password is not None else getpass.getpass("Password: "))
    print(
        f"Length: {report['length']} | "
        f"Estimated entropy: {report['entropy_bits']} bits (upper bound) | "
        f"Score: {report['score']}/100"
    )
    for name, passed in report["checks"].items():
        print(f"[{'PASS' if passed else 'FAIL'}] {name.replace('_', ' ')}")
    for item in report["advice"]:
        print(f"Advice: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
