#!/usr/bin/env python3
"""Inspect the TLS certificate and expiry of an authorized service.

Author: Fernando Tafurt Pinto
"""
import argparse
import datetime as dt
import socket
import ssl


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host")
    parser.add_argument("--port", type=int, default=443)
    parser.add_argument("--warning-days", type=int, default=30)
    args = parser.parse_args()
    try:
        with socket.create_connection((args.host, args.port), timeout=10) as raw:
            with ssl.create_default_context().wrap_socket(raw, server_hostname=args.host) as secure:
                cert = secure.getpeercert()
                cipher = secure.cipher()
    except (OSError, ssl.SSLError) as exc:
        parser.error(str(exc))
    expires = dt.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=dt.timezone.utc)
    remaining = (expires - dt.datetime.now(dt.timezone.utc)).days
    print(f"Subject: {dict(x[0] for x in cert.get('subject', []))}")
    print(f"Issuer: {dict(x[0] for x in cert.get('issuer', []))}")
    print(f"Expires: {expires.isoformat()} ({remaining} days)")
    print(f"Cipher: {cipher}")
    return 1 if remaining < args.warning_days else 0


if __name__ == "__main__":
    raise SystemExit(main())
