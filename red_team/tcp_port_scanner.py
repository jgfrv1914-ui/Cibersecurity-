#!/usr/bin/env python3
"""Concurrent TCP connect scanner for authorized security assessments.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor

SERVICES = {21: "FTP", 22: "SSH", 25: "SMTP", 53: "DNS", 80: "HTTP",
            110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt"}


def parse_ports(spec: str) -> list[int]:
    """Convert a comma-separated list of ports and ranges into sorted ports."""
    ports: set[int] = set()
    for item in spec.split(","):
        bounds = item.strip().split("-", 1)
        start, end = (int(bounds[0]), int(bounds[-1]))
        if not 1 <= start <= end <= 65535:
            raise argparse.ArgumentTypeError("ports must be between 1 and 65535")
        ports.update(range(start, end + 1))
    return sorted(ports)


def scan_port(host: str, port: int, timeout: float) -> tuple[int, str] | None:
    """Return port metadata when a TCP connection succeeds."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, SERVICES.get(port, "unknown")
    except (OSError, TimeoutError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", help="Authorized hostname or IP address")
    parser.add_argument("--ports", default="1-1024", type=parse_ports)
    parser.add_argument("--timeout", type=float, default=0.4)
    parser.add_argument("--workers", type=int, default=100)
    args = parser.parse_args()
    try:
        target = socket.gethostbyname(args.host)
        ipaddress.ip_address(target)
    except (socket.gaierror, ValueError) as exc:
        parser.error(f"cannot resolve target: {exc}")
    print(f"Authorized scan target: {args.host} ({target})")
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 300))) as pool:
        results = pool.map(lambda p: scan_port(target, p, args.timeout), args.ports)
    open_ports = sorted(result for result in results if result)
    for port, service in open_ports:
        print(f"{port:5}/tcp  open  {service}")
    print(f"Open ports: {len(open_ports)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
