#!/usr/bin/env python3
"""Audit common HTTP response security headers on an authorized website.

Author: Fernando Tafurt Pinto
"""
from __future__ import annotations

import argparse
import ssl
import urllib.error
import urllib.request

EXPECTED = {
    "strict-transport-security": "Enable HSTS on HTTPS responses.",
    "content-security-policy": "Define a restrictive content security policy.",
    "x-content-type-options": "Set to nosniff.",
    "x-frame-options": "Set DENY or SAMEORIGIN, or use CSP frame-ancestors.",
    "referrer-policy": "Define an explicit referrer policy.",
    "permissions-policy": "Disable unnecessary browser capabilities.",
}


def fetch_headers(url: str, verify_tls: bool = True) -> tuple[int, dict[str, str]]:
    request = urllib.request.Request(url, headers={"User-Agent": "Fernando-Security-Audit/1.0"})
    context = ssl.create_default_context() if verify_tls else ssl._create_unverified_context()
    with urllib.request.urlopen(request, timeout=10, context=context) as response:
        return response.status, {key.casefold(): value for key, value in response.headers.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--insecure", action="store_true", help="Lab only: disable TLS certificate validation")
    args = parser.parse_args()
    url = args.url if "://" in args.url else f"https://{args.url}"
    try:
        status, headers = fetch_headers(url, not args.insecure)
    except (urllib.error.URLError, ValueError) as exc:
        parser.error(f"request failed: {exc}")
    print(f"HTTP status: {status}")
    missing = 0
    for header, recommendation in EXPECTED.items():
        if header in headers:
            print(f"[PASS] {header}: {headers[header]}")
        else:
            missing += 1
            print(f"[MISS] {header} -> {recommendation}")
    for leaked in ("server", "x-powered-by", "x-aspnet-version"):
        if leaked in headers:
            print(f"[INFO] Technology disclosure: {leaked}: {headers[leaked]}")
    print(f"Score: {round((len(EXPECTED) - missing) / len(EXPECTED) * 100)}/100")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
