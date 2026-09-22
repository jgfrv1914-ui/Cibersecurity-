#!/usr/bin/env python3
"""Check methods advertised by an authorized HTTP server using OPTIONS.

Author: Fernando Tafurt Pinto
"""
import argparse
import urllib.error
import urllib.request

RISKY_METHODS = {"PUT", "DELETE", "TRACE", "CONNECT", "PATCH"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    args = parser.parse_args()
    request = urllib.request.Request(
        args.url, method="OPTIONS", headers={"User-Agent": "Authorized-Audit/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            status, headers = response.status, response.headers
    except urllib.error.HTTPError as exc:
        # A 405 or 501 is a legitimate answer, not a tool failure: the server is
        # telling us it does not implement OPTIONS. It may still send an Allow
        # header, so the response is worth reading rather than discarding.
        status, headers = exc.code, exc.headers
    except urllib.error.URLError as exc:
        print(f"ERROR could not reach {args.url}: {exc.reason}")
        return 2

    allowed = headers.get("Allow")
    print(f"HTTP status: {status}")
    if allowed is None:
        print("Allow: (not advertised)")
        print("The server does not advertise its methods via OPTIONS.")
        return 0

    print(f"Allow: {allowed}")
    advertised = {method.strip().upper() for method in allowed.split(",") if method.strip()}
    risky = sorted(advertised & RISKY_METHODS)
    print(f"Review potentially risky methods: {', '.join(risky) if risky else 'none advertised'}")
    return 1 if risky else 0


if __name__ == "__main__":
    raise SystemExit(main())
