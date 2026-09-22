# Usage guide

Complete command reference for every tool in the portfolio. All tools require
Python 3.10+ and use only the standard library.

Every tool supports `--help`, validates its input, and returns a meaningful exit
code (`0` success, `1` findings or failure, `2` invalid arguments).

- [Packaged projects](#packaged-projects)
- [Blue team tools](#blue-team-tools)
- [Red team / network tools](#red-team--network-tools)
- [Utilities](#utilities)
- [Exit codes](#exit-codes)

---

## Packaged projects

### Mini SOC Toolkit

Offline authentication-log triage producing a JSON evidence report.

```bash
python -m soc_toolkit <logfile> [--ioc-file FILE] [--threshold N]
```

| Argument | Default | Description |
|---|---|---|
| `logfile` | required | Authentication log export to analyze |
| `--ioc-file` | none | Newline-delimited indicators to correlate |
| `--threshold` | `3` | Failed logins from one source before a brute-force alert |

```bash
python -m soc_toolkit soc_toolkit/samples/auth.log \
  --ioc-file soc_toolkit/samples/iocs.txt \
  --threshold 3 > report.json
```

The report contains `report` metadata, a `summary` with severity counts, the
parsed `events`, and the generated `alerts`. A committed example lives at
[`../reports/soc_toolkit_sample_report.json`](../reports/soc_toolkit_sample_report.json).

### Secure Configuration Auditor

Read-only hardening checks against an exported configuration snapshot. It never
reads live system state, which makes it safe to run anywhere.

```bash
python -m security_auditor <snapshot-file>
```

The snapshot is a plain `key=value` file. See
[`../security_auditor/samples/linux_snapshot.txt`](../security_auditor/samples/linux_snapshot.txt).

| Check | Key | Expected |
|---|---|---|
| `SSH-001` | `ssh_root_login` | `no` |
| `SSH-002` | `ssh_password_auth` | `no` |
| `FW-001` | `firewall` | `active` |
| `AUD-001` | `audit_logging` | `yes` |

### Threat Intelligence Analyzer

Normalizes, deduplicates, and classifies indicators, then matches them against an
evidence export.

```bash
python -m threat_intel <ioc-file> <evidence-file>
```

Indicators are classified as `ipv4`, `domain`, `url`, or `hash`.

---

## Blue team tools

### `password_strength_analyzer.py`

Scores password quality and estimated entropy. The password is never echoed and
never appears in the report.

The reported entropy is an **upper bound**: it assumes every character was chosen
at random. A dictionary word with a suffix (`password123`) therefore gets a high
nominal entropy but is capped to a score of 20, because leetspeak and trailing
digits are the first mutations a cracking tool applies.

```bash
python blue_team/password_strength_analyzer.py            # prompts securely
python blue_team/password_strength_analyzer.py --password "..."   # avoid on shared hosts
```

`--password` is offered for scripting, but it can land in shell history. Prefer
the interactive prompt.

### `password_generator.py`

```bash
python blue_team/password_generator.py [--length 20] [--count 1] [--passphrase]
```

| Argument | Default | Description |
|---|---|---|
| `--length` | `20` | Password length (12-256) |
| `--count` | `1` | How many to generate (1-100) |
| `--passphrase` | off | Emit a six-word passphrase instead |

Uses `secrets`, not `random`.

### `file_hash_tool.py`

```bash
python blue_team/file_hash_tool.py --file report.pdf --algorithm sha256
python blue_team/file_hash_tool.py --text "demo" --verify <expected-digest>
```

| Argument | Default | Description |
|---|---|---|
| `--text` / `--file` | one required | Input source (mutually exclusive) |
| `--algorithm` | `sha256` | SHA-2 / SHA-3 family only |
| `--verify` | none | Compare against an expected hex digest |

### `file_integrity_monitor.py`

```bash
python blue_team/file_integrity_monitor.py /etc --init          # create baseline
python blue_team/file_integrity_monitor.py /etc                 # compare
```

| Argument | Default | Description |
|---|---|---|
| `directory` | required | Directory tree to monitor |
| `--baseline` | `fim_baseline.json` | Baseline file location |
| `--init` | off | Create or replace the baseline |

Reports `ADDED`, `REMOVED`, and `CHANGED` paths. The baseline is gitignored.

### `file_entropy_scanner.py`

```bash
python blue_team/file_entropy_scanner.py <paths...> [--threshold 7.5]
```

Shannon entropy in bits per byte. Values at or above the threshold suggest packed
or encrypted content and warrant context review, not an automatic verdict.

### `file_permissions_auditor.py`

```bash
python blue_team/file_permissions_auditor.py <directory>
```

Flags world-writable and otherwise dangerous permission bits.

### `log_analyzer.py`

```bash
python blue_team/log_analyzer.py <logfile> [--top 10]
```

Classifies each line into `authentication_failure`, `access_denied`,
`server_error`, or `injection_probe`, then ranks the most frequent source
addresses.

```console
$ python blue_team/log_analyzer.py soc_toolkit/samples/auth.log --top 3
Lines analyzed: 4
ALERT authentication_failure   4
Top source addresses:
203.0.113.45                            3
198.51.100.24                           1
```

### `failed_login_detector.py`

```bash
python blue_team/failed_login_detector.py <log> [--threshold 5] [--per-user]
```

| Argument | Default | Description |
|---|---|---|
| `log` | required | Authentication log export |
| `--threshold` | `5` | Failures before an alert is raised |
| `--per-user` | off | Count per source/username pair instead of per source address |

By default failures are counted **per source address**, because an attacker
spraying many usernames from one host produces a low count for each individual
pair. `--per-user` narrows the view when you are investigating one account.

### `ioc_matcher.py`

```bash
python blue_team/ioc_matcher.py <log> <indicators>
```

`indicators` is a file with one literal IOC per line.

### `http_security_header_auditor.py`

Sends one request to a URL you are authorized to assess and reviews hardening
headers (HSTS, CSP, X-Content-Type-Options, and related).

```bash
python blue_team/http_security_header_auditor.py https://example.com
python blue_team/http_security_header_auditor.py https://lab.internal --insecure
```

`--insecure` disables TLS validation and is intended for lab systems with
self-signed certificates only.

### `tls_certificate_inspector.py`

```bash
python blue_team/tls_certificate_inspector.py <host> [--port 443] [--warning-days 30]
```

Prints subject, issuer, and days remaining. Exits non-zero when the certificate
expires within the warning window, which makes it usable as a monitoring check.

---

## Red team / network tools

> These tools generate real network traffic. Run them only against systems you
> own or are explicitly authorized to assess.

### `tcp_port_scanner.py`

```bash
python red_team/tcp_port_scanner.py <host> [--ports 1-1024] [--timeout 0.4] [--workers 100]
```

`--ports` accepts comma-separated values and ranges: `80,443,8000-8010`.
Duplicates are removed and the result is sorted.

### `service_banner_grabber.py`

```bash
python red_team/service_banner_grabber.py <host> [ports...] [--timeout 3.0]
```

Defaults to ports 22, 25, 80, and 443.

Reachability and banner retrieval are reported separately. A service that accepts
the connection but sends nothing is reported as `OPEN (open, no banner returned)`,
not as closed — many services stay silent until spoken to first.

### `tcp_service_probe.py`

```bash
python red_team/tcp_service_probe.py <host> <ports...> [--timeout 2.0]
```

Reports reachability and connection latency per port.

### `dns_recon.py`

```bash
python red_team/dns_recon.py <hostname-or-ip>
```

Forward and reverse resolution for a single target.

### `subdomain_enumerator.py`

```bash
python red_team/subdomain_enumerator.py <domain> [--wordlist FILE] [--workers 20]
```

Resolution only: no zone transfers, no brute-force against the target service.

### `http_methods_auditor.py`

```bash
python red_team/http_methods_auditor.py <url>
```

Issues one `OPTIONS` request and flags advertised `PUT`, `DELETE`, `TRACE`,
`CONNECT`, and `PATCH`. Exits `1` when risky methods are advertised.

A `405` or `501` response is a valid answer, not a tool failure: the server is
saying it does not implement `OPTIONS`. The tool reports the status and any
`Allow` header it still returned. Exit `2` is reserved for a genuinely
unreachable host.

### `robots_sitemap_auditor.py`

```bash
python red_team/robots_sitemap_auditor.py <url>
```

Retrieves `robots.txt` and `sitemap.xml`, capped at 128 KB per file.

### `cidr_host_inventory.py`

```bash
python red_team/cidr_host_inventory.py <network> [--limit 4096]
```

Enumerates usable hosts in a CIDR range. The tool refuses to expand a network
larger than `--limit` so an accidental `/8` cannot flood the terminal.

---

## Utilities

### `ip_subnet_calculator.py`

```bash
python utilities/ip_subnet_calculator.py 192.168.10.25/24
python utilities/ip_subnet_calculator.py 2001:db8::1/64
```

Prints network, netmask, hostmask, total addresses, broadcast, and scope flags
for IPv4 and IPv6.

---

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Completed with no findings requiring attention |
| `1` | Completed, but findings were reported (risky methods, expiring certificate, integrity drift) |
| `2` | Invalid arguments or unreadable input |

This makes the tools composable in shell pipelines and CI checks.
