# Fernando Tafurt SOC Toolkit

An offline, dependency-free mini SOC project for defensive triage of authorized
authentication-log exports. It parses failed SSH logins, detects repeated
failures, matches known indicators, and produces a JSON investigation report.

## Why this project matters

This turns the portfolio's individual Blue Team scripts into one coherent
workflow:

1. Collect a local log export.
2. Parse security-relevant events.
3. Prioritize suspicious activity.
4. Preserve evidence in a machine-readable report.

## Quick start

From the repository root:

```bash
python -m soc_toolkit soc_toolkit/samples/auth.log \
  --ioc-file soc_toolkit/samples/iocs.txt \
  --threshold 3 \
  --output soc_toolkit/samples/report.json
```

The sample data uses documentation-only IP ranges. Do not run this against
systems or logs you are not authorized to access.

## Output

The report includes:

- Number of events analyzed
- Severity counts
- Source IP and affected users
- First and last observed event
- Exact IOC matches
- Evidence suitable for follow-up investigation

## Limitations

This is an intentionally small portfolio project, not a production SIEM. It
currently focuses on SSH-style failed-login records and exact IOC matching.
Future work could add Windows Event Log normalization, Sigma rule support, and
an HTML dashboard.
