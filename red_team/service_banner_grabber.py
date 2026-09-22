#!/usr/bin/env python3
"""Collect a limited service banner from an explicitly authorized target.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import socket
import ssl

PROBES = {21: b"", 22: b"", 25: b"EHLO audit.local\r\n", 80: b"HEAD / HTTP/1.0\r\n\r\n",
          110: b"", 143: b"", 443: b"HEAD / HTTP/1.0\r\nHost: target\r\n\r\n",
          6379: b"PING\r\n", 8080: b"HEAD / HTTP/1.0\r\n\r\n"}


def grab(host: str, port: int, timeout: float) -> str:
    """Send a minimal protocol probe and return at most 1 KiB of response."""
    with socket.create_connection((host, port), timeout=timeout) as raw:
        connection = raw
        if port == 443:
            context = ssl.create_default_context()
            connection = context.wrap_socket(raw, server_hostname=host)
        probe = PROBES.get(port, b"")
        if probe:
            connection.sendall(probe)
        return connection.recv(1024).decode("utf-8", errors="replace").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host")
    parser.add_argument("ports", nargs="*", type=int, default=[22, 25, 80, 443])
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()
    for port in args.ports:
        if not 1 <= port <= 65535:
            parser.error("ports must be between 1 and 65535")
        try:
            banner = grab(args.host, port, args.timeout)
            clean = " | ".join(banner.splitlines()[:5]) or "(no banner returned)"
            print(f"{port:5}/tcp OPEN  {clean}")
        except (OSError, ssl.SSLError) as exc:
            print(f"{port:5}/tcp CLOSED/FILTERED  {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
