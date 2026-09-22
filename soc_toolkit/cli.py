"""Command-line entry point for the offline SOC triage toolkit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import (
    build_report,
    detect_brute_force,
    load_lines,
    match_iocs,
    parse_auth_log,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze authorized local authentication-log exports."
    )
    parser.add_argument("logfile", type=Path, help="UTF-8 log export to analyze")
    parser.add_argument("--ioc-file", type=Path, help="Optional newline-delimited IOC file")
    parser.add_argument("--threshold", type=int, default=3, help="Failed-login threshold")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.threshold < 1:
        raise SystemExit("--threshold must be at least 1")
    lines = load_lines(args.logfile)
    events = parse_auth_log(lines, source=str(args.logfile))
    alerts = detect_brute_force(events, threshold=args.threshold)
    if args.ioc_file:
        alerts.extend(match_iocs(events, load_lines(args.ioc_file)))
    report = build_report(events, alerts, source=str(args.logfile))
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
