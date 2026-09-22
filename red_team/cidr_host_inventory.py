#!/usr/bin/env python3
"""Generate a host-address inventory from a small CIDR block (no probing).

Author: Fernando Tafurt Pinto
"""
import argparse
import ipaddress


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("network", help="Example: 192.0.2.0/28")
    parser.add_argument("--limit", type=int, default=4096)
    args = parser.parse_args()
    try:
        network = ipaddress.ip_network(args.network, strict=False)
    except ValueError as exc:
        parser.error(str(exc))
    count = max(0, network.num_addresses - (2 if network.version == 4 and network.prefixlen < 31 else 0))
    if count > args.limit:
        parser.error(f"network has {count} usable hosts; increase --limit intentionally")
    print(f"Network: {network.network_address} | Broadcast: {network.broadcast_address} | Hosts: {count}")
    for host in network.hosts():
        print(host)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
