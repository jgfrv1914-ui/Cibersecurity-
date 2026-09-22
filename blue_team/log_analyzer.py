#!/usr/bin/env python3
"""Summarize IP activity and suspicious patterns in text logs.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path

IP_PATTERN = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
RULES = {
    "authentication_failure": re.compile(r"failed|invalid user|authentication failure", re.I),
    "access_denied": re.compile(r"forbidden|denied|\b403\b", re.I),
    "server_error": re.compile(r"\b5\d\d\b|exception|traceback", re.I),
    "injection_probe": re.compile(r"union(?:\s|%20)+select|<script|\.\./", re.I),
}


def analyze(lines: list[str]) -> tuple[collections.Counter[str], collections.Counter[str]]:
    addresses: collections.Counter[str] = collections.Counter()
    alerts: collections.Counter[str] = collections.Counter()
    for line in lines:
        addresses.update(IP_PATTERN.findall(line))
        alerts.update(name for name, pattern in RULES.items() if pattern.search(line))
    return addresses, alerts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logfile", type=Path)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()
    try:
        lines = args.logfile.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        parser.error(str(exc))
    addresses, alerts = analyze(lines)
    print(f"Lines analyzed: {len(lines)}")
    for name, count in alerts.most_common():
        print(f"ALERT {name:24} {count}")
    print("Top source addresses:")
    for address, count in addresses.most_common(max(1, args.top)):
        print(f"{address:39} {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
