#!/usr/bin/env python3
"""Retrieve robots.txt and sitemap.xml from a website you may assess.

Author: Fernando Tafurt Pinto
"""
import argparse
import urllib.parse
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    args = parser.parse_args()
    base = args.url if "://" in args.url else f"https://{args.url}"
    parsed = urllib.parse.urlsplit(base)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    for name in ("robots.txt", "sitemap.xml"):
        url = f"{origin}/{name}"
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                text = response.read(128 * 1024).decode("utf-8", errors="replace")
            print(f"\n--- {url} ---\n{text}")
        except OSError as exc:
            print(f"ERROR {url}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
