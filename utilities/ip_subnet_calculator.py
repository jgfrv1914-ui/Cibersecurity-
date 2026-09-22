#!/usr/bin/env python3
"""Explain an IPv4 or IPv6 address and subnet using the standard library.

Author: Fernando Tafurt Pinto
"""
import argparse
import ipaddress


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("interface", help="Example: 192.168.1.10/24")
    args = parser.parse_args()
    try:
        interface = ipaddress.ip_interface(args.interface)
    except ValueError as exc:
        parser.error(str(exc))
    network = interface.network
    print(f"IP address:       {interface.ip}")
    print(f"Network:          {network.network_address}/{network.prefixlen}")
    print(f"Netmask:          {network.netmask}")
    print(f"Hostmask:         {network.hostmask}")
    print(f"Total addresses:  {network.num_addresses}")
    if network.version == 4:
        print(f"Broadcast:        {network.broadcast_address}")
    print(f"Private:          {interface.ip.is_private}")
    print(f"Global:           {interface.ip.is_global}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
