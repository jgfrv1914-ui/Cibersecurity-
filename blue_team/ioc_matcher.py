#!/usr/bin/env python3
"""Match indicators of compromise (IOCs) against a text log.

Author: Fernando Tafurt Pinto
"""
import argparse
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path)
    parser.add_argument("indicators", type=Path, help="One literal IOC per line")
    args = parser.parse_args()
    try:
        text = args.log.read_text(encoding="utf-8", errors="replace")
        iocs = [x.strip() for x in args.indicators.read_text(encoding="utf-8").splitlines()
                if x.strip() and not x.startswith("#")]
    except OSError as exc:
        parser.error(str(exc))
    findings = [(ioc, len(re.findall(re.escape(ioc), text, re.I))) for ioc in iocs]
    for ioc, count in findings:
        if count:
            print(f"MATCH {count:5}  {ioc}")
    print(f"Matched indicators: {sum(bool(count) for _, count in findings)} of {len(iocs)}")
    return 1 if any(count for _, count in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
