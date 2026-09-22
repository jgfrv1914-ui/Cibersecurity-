#!/usr/bin/env python3
"""Resolve a small, configurable subdomain list for an authorized domain.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import socket
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DEFAULT_NAMES = "www mail api app dev staging test vpn portal admin docs status".split()


def resolve(name: str) -> tuple[str, list[str]] | None:
    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(name, None)})
        return name, addresses
    except socket.gaierror:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("domain", help="Domain you own or are authorized to assess")
    parser.add_argument("--wordlist", type=Path)
    parser.add_argument("--workers", type=int, default=20)
    args = parser.parse_args()
    names = DEFAULT_NAMES
    if args.wordlist:
        try:
            names = [line.strip() for line in args.wordlist.read_text(encoding="utf-8").splitlines()
                     if line.strip() and not line.startswith("#")]
        except OSError as exc:
            parser.error(str(exc))
    candidates = [f"{name}.{args.domain.strip('.')}" for name in names[:10000]]
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 100))) as pool:
        findings = sorted(item for item in pool.map(resolve, candidates) if item)
    for hostname, addresses in findings:
        print(f"{hostname:50} {', '.join(addresses)}")
    print(f"Resolved: {len(findings)} of {len(candidates)} candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
