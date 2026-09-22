# Fernando Tafurt Pinto — Cybersecurity Portfolio

[![CI](https://github.com/jgfrv1914-ui/Cibersecurity-/actions/workflows/ci.yml/badge.svg)](https://github.com/jgfrv1914-ui/Cibersecurity-/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Dependencies: none](https://img.shields.io/badge/Dependencies-Standard%20Library-lightgrey)](https://docs.python.org/3/library/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Live portfolio → <https://jgfrv1914-ui.github.io/Cibersecurity-/>**

Defensive security tooling, offline SOC triage, threat intelligence enrichment,
and authorized assessment utilities — written in pure Python with no third-party
dependencies, validated by an automated test suite on every push.

---

## Table of contents

- [Why this repository exists](#why-this-repository-exists)
- [Flagship project: Mini SOC Toolkit](#flagship-project-mini-soc-toolkit)
- [Repository layout](#repository-layout)
- [Project catalogue](#project-catalogue)
- [Command-line tools](#command-line-tools)
- [Quick start](#quick-start)
- [Testing and quality gates](#testing-and-quality-gates)
- [Engineering principles](#engineering-principles)
- [Credentials](#credentials)
- [Ethical use](#ethical-use)
- [Roadmap](#roadmap)
- [License and contact](#license-and-contact)

---

## Why this repository exists

This is not a collection of loose scripts. It is a working demonstration of how I
approach security engineering:

- **Evidence over claims.** Every packaged project ships sample input, a
  reproducible command, and a committed output artifact you can diff.
- **Offline and non-destructive by default.** Analysis tools read exported
  evidence; they never mutate the system under review.
- **Tested.** 17 unit tests cover parsing, detection logic, scoring, and report
  shape, including regression tests for three real defects found by running
  every tool end to end.
- **Linted and CI-gated.** `ruff` and the test suite run on Python 3.10, 3.11,
  and 3.12 for every push and pull request.

---

## Flagship project: Mini SOC Toolkit

[`soc_toolkit/`](soc_toolkit/) is a complete offline triage workflow: parse an
authentication log export, detect brute-force patterns, correlate indicators of
compromise, and emit structured JSON evidence for an investigation.

```bash
python -m soc_toolkit soc_toolkit/samples/auth.log \
  --ioc-file soc_toolkit/samples/iocs.txt \
  --threshold 3
```

Real output (full artifact committed at
[`reports/soc_toolkit_sample_report.json`](reports/soc_toolkit_sample_report.json)):

```json
{
  "summary": {
    "events_analyzed": 4,
    "alerts": 4,
    "severity_counts": { "high": 1, "critical": 3 }
  },
  "alerts": [
    {
      "alert_type": "brute_force",
      "severity": "high",
      "title": "Repeated failed logins from 203.0.113.45",
      "evidence": {
        "source_ip": "203.0.113.45",
        "attempts": 3,
        "target_users": ["admin", "fernando"],
        "first_seen": "Sep 22 09:10:01",
        "last_seen": "Sep 22 09:10:15"
      }
    }
  ]
}
```

**Detection detail worth noting.** IOC correlation is delimiter-aware, not a
substring search: the indicator `10.0.0.1` does not alert on `10.0.0.11` or
`210.0.0.1`. A naive containment check produces exactly that class of false
positive, and [`tests/test_soc_toolkit.py`](tests/test_soc_toolkit.py) pins the
correct behaviour.

---

## Repository layout

```
.
├── index.html, styles.css, script.js   Bilingual portfolio site (GitHub Pages)
├── assets/                             Site images and favicon
├── soc_toolkit/                        Flagship: offline log triage to JSON evidence
├── security_auditor/                   Read-only Linux hardening checks
├── threat_intel/                       Offline IOC normalization and matching
├── detections/sigma/                   Sigma rules mapped to MITRE ATT&CK
├── blue_team/                          11 defensive command-line tools
├── red_team/                           8 authorized reconnaissance tools
├── utilities/                          Networking and addressing helpers
├── reports/                            Committed sample output artifacts
├── tests/                              Unit test suite (offline, no network)
└── docs/                               Usage guide and roadmap
```

---

## Project catalogue

| Project | What it does | Entry point |
|---|---|---|
| **[Mini SOC Toolkit](soc_toolkit/)** | Parses auth logs, detects brute force, correlates IOCs, emits JSON evidence | `python -m soc_toolkit` |
| **[Secure Configuration Auditor](security_auditor/)** | Read-only hardening checks for SSH, firewall, and audit logging from exported snapshots | `python -m security_auditor` |
| **[Threat Intelligence Analyzer](threat_intel/)** | Normalizes and classifies IPs, domains, URLs, and hashes, then matches them against evidence | `python -m threat_intel` |
| **[Sigma Detection Rules](detections/)** | SSH brute force and suspicious admin account creation, mapped to MITRE ATT&CK | `detections/sigma/*.yml` |

### Secure Configuration Auditor

```bash
python -m security_auditor security_auditor/samples/linux_snapshot.txt
```

```json
{
  "check_id": "SSH-001",
  "severity": "info",
  "status": "PASS",
  "title": "SSH root login disabled",
  "evidence": "ssh_root_login=no; remediation: Disable PermitRootLogin."
}
```

### Threat Intelligence Analyzer

```bash
python -m threat_intel threat_intel/samples/iocs.txt threat_intel/samples/evidence.log
```

```json
{
  "indicators": [
    { "value": "malware.example", "kind": "domain", "confidence": "medium" },
    { "value": "44d88612fea8a8f36de82e1278abb02f", "kind": "hash", "confidence": "medium" },
    { "value": "203.0.113.45", "kind": "ipv4", "confidence": "medium" }
  ]
}
```

---

## Command-line tools

Every tool is a single, self-contained file with `--help`, explicit validation,
and meaningful exit codes. Full usage guide: **[`docs/USAGE.md`](docs/USAGE.md)**.

### Blue team — detection, monitoring, and hardening

| Tool | Purpose |
|---|---|
| [`password_strength_analyzer.py`](blue_team/password_strength_analyzer.py) | Score password quality and estimated entropy without echoing the secret |
| [`password_generator.py`](blue_team/password_generator.py) | Generate strong passwords and passphrases using `secrets` |
| [`file_hash_tool.py`](blue_team/file_hash_tool.py) | Compute and verify SHA-2 / SHA-3 digests |
| [`file_integrity_monitor.py`](blue_team/file_integrity_monitor.py) | Track added, removed, and modified files against a known-good baseline |
| [`file_entropy_scanner.py`](blue_team/file_entropy_scanner.py) | Surface high-entropy files that may be packed or encrypted |
| [`file_permissions_auditor.py`](blue_team/file_permissions_auditor.py) | Flag world-writable and otherwise dangerous permissions |
| [`log_analyzer.py`](blue_team/log_analyzer.py) | Classify auth failures, access denials, errors, and injection probes; rank source IPs |
| [`failed_login_detector.py`](blue_team/failed_login_detector.py) | Identify repeated authentication failures by source |
| [`ioc_matcher.py`](blue_team/ioc_matcher.py) | Match indicators of compromise against logs and artifacts |
| [`http_security_header_auditor.py`](blue_team/http_security_header_auditor.py) | Review HTTP response hardening headers |
| [`tls_certificate_inspector.py`](blue_team/tls_certificate_inspector.py) | Inspect certificate subject, issuer, and days until expiry |

### Red team / network — authorized targets only

| Tool | Purpose |
|---|---|
| [`tcp_port_scanner.py`](red_team/tcp_port_scanner.py) | Concurrent TCP port scanning with range parsing |
| [`service_banner_grabber.py`](red_team/service_banner_grabber.py) | Collect service banners from reachable hosts |
| [`tcp_service_probe.py`](red_team/tcp_service_probe.py) | Measure reachability and latency for a service |
| [`dns_recon.py`](red_team/dns_recon.py) | Forward and reverse DNS inspection |
| [`subdomain_enumerator.py`](red_team/subdomain_enumerator.py) | Resolve candidate names from a wordlist |
| [`http_methods_auditor.py`](red_team/http_methods_auditor.py) | Review advertised HTTP methods and flag risky ones |
| [`robots_sitemap_auditor.py`](red_team/robots_sitemap_auditor.py) | Retrieve `robots.txt` and `sitemap.xml` discovery files |
| [`cidr_host_inventory.py`](red_team/cidr_host_inventory.py) | Build a host inventory from a CIDR range with an explicit size guard |

### Utilities

| Tool | Purpose |
|---|---|
| [`ip_subnet_calculator.py`](utilities/ip_subnet_calculator.py) | IPv4/IPv6 subnet, netmask, broadcast, and scope details |

```console
$ python utilities/ip_subnet_calculator.py 192.168.10.25/24
IP address:       192.168.10.25
Network:          192.168.10.0/24
Netmask:          255.255.255.0
Total addresses:  256
Broadcast:        192.168.10.255
Private:          True
```

---

## Quick start

Python 3.10 or newer. No third-party packages required.

```bash
git clone https://github.com/jgfrv1914-ui/Cibersecurity-.git
cd Cibersecurity-

# Flagship workflow
python -m soc_toolkit soc_toolkit/samples/auth.log --ioc-file soc_toolkit/samples/iocs.txt --threshold 3

# Individual tools
python blue_team/log_analyzer.py soc_toolkit/samples/auth.log --top 5
python utilities/ip_subnet_calculator.py 10.0.0.0/22
python blue_team/password_strength_analyzer.py --help
```

---

## Testing and quality gates

```bash
python -m unittest discover -s tests -v   # 17 tests, fully offline
python -m compileall -q .                 # byte-compile every module
ruff check .                              # lint (config in pyproject.toml)
```

All three run in CI against Python 3.10, 3.11, and 3.12
([`.github/workflows/ci.yml`](.github/workflows/ci.yml)). The badge at the top of
this file reflects the real result of that workflow.

---

## Engineering principles

- **Standard library only** — portable, auditable, and free of supply-chain risk.
- **Read-only analysis** — defensive tools never modify the evidence they inspect.
- **Explicit guardrails** — for example, `cidr_host_inventory.py` refuses to
  enumerate an oversized network unless the operator raises `--limit` on purpose.
- **Secrets stay out of argv** — the password analyzer prompts via `getpass` and
  never echoes or returns the password in its report.
- **Deterministic, serializable output** — JSON reports are stable and diffable,
  which makes them usable as evidence and as test fixtures.

---

## Credentials

Cybersecurity and networking credentials only, verifiable on Credly:

| Credential | Issuer |
|---|---|
| Ethical Hacker | Cisco Networking Academy |
| Networking Basics | Cisco Networking Academy |
| Networking Devices and Initial Configuration | Cisco Networking Academy |
| Junior Cybersecurity Analyst Career Path | Cisco Networking Academy |
| Cyber Threat Management | Cisco Networking Academy |
| Getting Started in Cybersecurity 3.0 | Fortinet |
| Google Cybersecurity Certificate | Coursera / Google |
| Security Analyst Fundamentals Specialization | Coursera / IBM |
| IBM and ISC2 Cybersecurity Specialist Professional Certificate | Coursera / IBM and ISC2 |

Verify: [Credly profile 1](https://www.credly.com/users/fernando-tafurt/badges/credly) ·
[Credly profile 2](https://www.credly.com/users/fernando-tafurt-pinto/badges/credly)

---

## Ethical use

> Use these tools only against systems you own, are explicitly authorized to
> test, or have written permission to assess.

The reconnaissance tools in `red_team/` generate real network traffic. Everything
in `blue_team/`, `soc_toolkit/`, `security_auditor/`, and `threat_intel/` operates
on local files you provide. This repository is not intended for unauthorized
scanning or exploitation. See [`SECURITY.md`](SECURITY.md).

---

## Roadmap

Planned work is tracked in [`docs/ROADMAP.md`](docs/ROADMAP.md).

---

## License and contact

Released under the [MIT License](LICENSE).

- **Portfolio:** <https://jgfrv1914-ui.github.io/Cibersecurity-/>
- **LinkedIn:** <https://www.linkedin.com/in/fernandotafurtag9a00/>
- **Email:** fernandotafurtpinto@gmail.com
