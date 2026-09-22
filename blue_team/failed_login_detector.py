#!/usr/bin/env python3
"""Detect repeated failed SSH logins in Linux authentication logs.

Author: Fernando Tafurt Pinto
"""
import argparse
import collections
import re
from pathlib import Path

# Matches both sshd variants: "Failed password for bob from ..." and
# "Failed password for invalid user bob from ...".
FAILED = re.compile(
    r"Failed password for (?:invalid user |user )?(?P<user>\S+) from (?P<ip>[0-9a-fA-F:.]+)"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("--threshold", type=int, default=5)
    parser.add_argument(
        "--per-user",
        action="store_true",
        help="Count per source/username pair instead of per source address",
    )
    args = parser.parse_args()
    if args.threshold < 1:
        parser.error("threshold must be at least 1")
    try:
        text = args.log.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        parser.error(str(exc))

    matches = list(FAILED.finditer(text))
    if args.per_user:
        counts = collections.Counter((m["ip"], m["user"]) for m in matches)
        alerts = [
            (ip, count, [user]) for (ip, user), count in counts.items() if count >= args.threshold
        ]
    else:
        # Default: count per source address. An attacker spraying many usernames
        # from one host produces a low count for each individual pair, so
        # grouping by (source, user) would miss exactly the pattern this tool
        # exists to catch.
        counts: collections.Counter[str] = collections.Counter()
        users: dict[str, set[str]] = {}
        for match in matches:
            counts[match["ip"]] += 1
            users.setdefault(match["ip"], set()).add(match["user"])
        alerts = [
            (ip, count, sorted(users[ip])) for ip, count in counts.items() if count >= args.threshold
        ]

    for ip, count, targeted in sorted(alerts, key=lambda item: item[1], reverse=True):
        print(f"ALERT {count:5} failures  source={ip} users={','.join(targeted)}")
    print(f"Failed logins parsed: {len(matches)}")
    print(f"Alerts: {len(alerts)}")
    return 1 if alerts else 0


if __name__ == "__main__":
    raise SystemExit(main())
