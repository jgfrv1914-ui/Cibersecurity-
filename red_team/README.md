# Red team / network tools

Reconnaissance and discovery utilities for **authorized** assessments and
controlled lab environments.

> These tools generate real network traffic against the target you name. Run them
> only against systems you own, are explicitly authorized to test, or have
> written permission to assess. See [`../SECURITY.md`](../SECURITY.md).

Full argument reference: [`../docs/USAGE.md`](../docs/USAGE.md).

## Tools

| Tool | Purpose | Traffic generated |
|---|---|---|
| [`tcp_port_scanner.py`](tcp_port_scanner.py) | Concurrent TCP connect scan with range parsing | one connection per port |
| [`service_banner_grabber.py`](service_banner_grabber.py) | Collect service banners from open ports | one connection per port |
| [`tcp_service_probe.py`](tcp_service_probe.py) | Measure reachability and latency per port | one connection per port |
| [`dns_recon.py`](dns_recon.py) | Forward and reverse DNS inspection | DNS queries only |
| [`subdomain_enumerator.py`](subdomain_enumerator.py) | Resolve candidate names from a wordlist | DNS queries only |
| [`http_methods_auditor.py`](http_methods_auditor.py) | Review advertised HTTP methods, flag risky ones | one `OPTIONS` request |
| [`robots_sitemap_auditor.py`](robots_sitemap_auditor.py) | Fetch `robots.txt` and `sitemap.xml` | two `GET` requests |
| [`cidr_host_inventory.py`](cidr_host_inventory.py) | Expand a CIDR range into a host inventory | none (local computation) |

## Scope and restraint

These are deliberately conservative tools. They perform discovery, not
exploitation:

- **TCP connect only.** No raw sockets, no SYN scanning, no spoofing — which also
  means no elevated privileges are required.
- **DNS resolution only.** `subdomain_enumerator.py` resolves names; it does not
  attempt zone transfers or brute-force any service.
- **Explicit size guards.** `cidr_host_inventory.py` refuses to expand a network
  larger than `--limit` (default 4096), so an accidental `/8` cannot flood the
  terminal or a downstream scan.
- **Bounded reads.** `robots_sitemap_auditor.py` caps each response at 128 KB.
- **Honest user agents.** The HTTP tools identify themselves rather than
  impersonating a browser.

## Example

```bash
python red_team/tcp_port_scanner.py 127.0.0.1 --ports 22,80,443,8000-8010
```

Port range parsing deduplicates and sorts, and is covered by
[`../tests/test_cli_tools.py`](../tests/test_cli_tools.py):

```python
parse_ports("80,443,80,8000-8002") == [80, 443, 8000, 8001, 8002]
```
