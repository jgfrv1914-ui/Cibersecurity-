#!/usr/bin/env python3
"""Test TCP reachability and connection latency for approved endpoints.

Author: Fernando Tafurt Pinto
"""
import argparse
import socket
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host")
    parser.add_argument("ports", nargs="+", type=int)
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    failures = 0
    for port in args.ports:
        started = time.perf_counter()
        try:
            with socket.create_connection((args.host, port), timeout=args.timeout):
                elapsed = (time.perf_counter() - started) * 1000
                print(f"OPEN   {port:5}/tcp {elapsed:8.2f} ms")
        except OSError as exc:
            failures += 1
            print(f"CLOSED {port:5}/tcp {str(exc)[:60]}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
