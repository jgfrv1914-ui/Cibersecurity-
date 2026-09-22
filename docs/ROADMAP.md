# Future cybersecurity portfolio tools

## Best next projects

1. **Mini SIEM dashboard** — ingest JSON events, normalize them, apply rules,
   and display a searchable incident timeline.
2. **YARA rule lab** — scan a harmless sample corpus, explain matches, and test
   false positives with automated fixtures.
3. **PCAP traffic analyzer** — summarize protocols, conversations, DNS queries,
   and suspicious beacon-like intervals from offline packet captures.
4. **Cloud configuration auditor** — evaluate exported AWS, Azure, or GCP
   configuration against a small CIS-inspired rule set without changing it.
5. **Dependency risk reporter** — parse lockfiles, create an SBOM, query a
   vulnerability source, and produce a severity-ranked report.
6. **Phishing-email analyzer** — parse `.eml` files, inspect authentication
   headers, extract URLs, and explain risk signals without opening links.
7. **Honeypot telemetry visualizer** — collect events from a lab honeypot and
   map source trends, credentials attempted, and targeted services.
8. **Windows event-log detector** — analyze exported EVTX/JSON for suspicious
   PowerShell, new services, account creation, and privilege changes.
9. **Secrets scanner** — inspect a local Git working tree for likely tokens,
   private keys, and high-entropy credentials, with allowlists and redaction.
10. **Detection-as-code repository** — Sigma-style rules, sample events, unit
    tests, MITRE ATT&CK mappings, and coverage reporting.

## How to make each project portfolio-ready

- Include a threat model and a clear authorized-use statement.
- Add sample input made from synthetic or sanitized data.
- Include unit tests, type hints, structured JSON output, and CI checks.
- Document limitations and false-positive/false-negative tradeoffs.
- Add screenshots or a short demo GIF and a one-page technical write-up.
- Map defensive detections to MITRE ATT&CK techniques where appropriate.
