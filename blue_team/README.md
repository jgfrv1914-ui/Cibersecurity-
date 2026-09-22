# Blue team tools

Defensive command-line tools for detection, monitoring, hardening review, and
file triage. Every tool here is **read-only**: it inspects evidence you provide
and never modifies the system under review.

Full argument reference: [`../docs/USAGE.md`](../docs/USAGE.md).

## Tools

| Tool | Purpose | Network access |
|---|---|---|
| [`password_strength_analyzer.py`](password_strength_analyzer.py) | Score password quality and estimated entropy; the secret is never echoed or returned | none |
| [`password_generator.py`](password_generator.py) | Generate passwords and passphrases with `secrets` | none |
| [`file_hash_tool.py`](file_hash_tool.py) | Compute and verify SHA-2 / SHA-3 digests | none |
| [`file_integrity_monitor.py`](file_integrity_monitor.py) | Detect added, removed, and modified files against a baseline | none |
| [`file_entropy_scanner.py`](file_entropy_scanner.py) | Surface high-entropy files that may be packed or encrypted | none |
| [`file_permissions_auditor.py`](file_permissions_auditor.py) | Flag world-writable and otherwise dangerous permissions | none |
| [`log_analyzer.py`](log_analyzer.py) | Classify auth failures, denials, errors, and injection probes; rank source IPs | none |
| [`failed_login_detector.py`](failed_login_detector.py) | Identify repeated authentication failures by source | none |
| [`ioc_matcher.py`](ioc_matcher.py) | Match indicators of compromise against logs and artifacts | none |
| [`http_security_header_auditor.py`](http_security_header_auditor.py) | Review HTTP response hardening headers | one request |
| [`tls_certificate_inspector.py`](tls_certificate_inspector.py) | Inspect certificate subject, issuer, and days to expiry | one TLS handshake |

The last two contact a host you name. Use them only against systems you own or
are authorized to assess.

## Example

```bash
python blue_team/log_analyzer.py soc_toolkit/samples/auth.log --top 3
```

```console
Lines analyzed: 4
ALERT authentication_failure   4
Top source addresses:
203.0.113.45                            3
198.51.100.24                           1
```

## Design notes

- **Secrets never enter a report.** `password_strength_analyzer.py` prompts with
  `getpass` and its report dictionary deliberately omits the password itself — a
  property pinned by a unit test.
- **Entropy is a signal, not a verdict.** A high score means "review the
  context", not "this is malware".
- **The FIM baseline is gitignored.** It describes a specific host and does not
  belong in version control.
