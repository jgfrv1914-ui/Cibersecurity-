#!/usr/bin/env python3
"""Check methods advertised by an authorized HTTP server using OPTIONS.

Author: Fernando Tafurt Pinto
"""
import argparse
import urllib.error
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    args = parser.parse_args()
    request = urllib.request.Request(args.url, method="OPTIONS", headers={"User-Agent": "Authorized-Audit/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            allowed = response.headers.get("Allow", "(not advertised)")
    except urllib.error.URLError as exc:
        parser.error(str(exc))
    print(f"Allow: {allowed}")
    risky = sorted({m.strip().upper() for m in allowed.split(",")} & {"PUT", "DELETE", "TRACE", "CONNECT"})
    print(f"Review potentially risky methods: {', '.join(risky) if risky else 'none advertised'}")
    return 1 if risky else 0


if __name__ == "__main__":
    raise SystemExit(main())
