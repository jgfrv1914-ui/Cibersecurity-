#!/usr/bin/env python3
"""Detect repeated failed SSH logins in Linux authentication logs.

Author: Fernando Tafurt Pinto
"""
import argparse
import collections
import re
from pathlib import Path

FAILED = re.compile(r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>[0-9a-fA-F:.]+)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--threshold", type=int, default=5)
    args = parser.parse_args()
    try:
        matches = FAILED.finditer(args.log.read_text(encoding="utf-8", errors="replace"))
    except OSError as exc:
        parser.error(str(exc))
    counts = collections.Counter((m["ip"], m["user"]) for m in matches)
    alerts = [(ip, user, count) for (ip, user), count in counts.items() if count >= args.threshold]
    for ip, user, count in sorted(alerts, key=lambda item: item[2], reverse=True):
        print(f"ALERT {count:5} failures  source={ip} user={user}")
    print(f"Alert pairs: {len(alerts)}")
    return 1 if alerts else 0


if __name__ == "__main__":
    raise SystemExit(main())
