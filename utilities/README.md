# Utilities

Supporting networking and addressing helpers.

Full argument reference: [`../docs/USAGE.md`](../docs/USAGE.md).

| Tool | Purpose |
|---|---|
| [`ip_subnet_calculator.py`](ip_subnet_calculator.py) | IPv4/IPv6 subnet, netmask, hostmask, broadcast, and scope details |

## Example

```bash
python utilities/ip_subnet_calculator.py 192.168.10.25/24
```

```console
IP address:       192.168.10.25
Network:          192.168.10.0/24
Netmask:          255.255.255.0
Hostmask:         0.0.0.255
Total addresses:  256
Broadcast:        192.168.10.255
Private:          True
Global:           False
```

Built on the standard library `ipaddress` module, so IPv6 works the same way:

```bash
python utilities/ip_subnet_calculator.py 2001:db8::1/64
```
