#!/usr/bin/env python3
"""Perform basic forward and reverse DNS reconnaissance with authorization.

Author: Fernando Tafurt Pinto
"""
import argparse
import socket


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Hostname or IP address")
    args = parser.parse_args()
    try:
        records = socket.getaddrinfo(args.target, None)
        addresses = sorted({record[4][0] for record in records})
    except socket.gaierror as exc:
        parser.error(str(exc))
    for address in addresses:
        try:
            reverse = socket.gethostbyaddr(address)[0]
        except (socket.herror, socket.gaierror):
            reverse = "(no PTR record)"
        print(f"{address:39} PTR {reverse}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
