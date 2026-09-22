# Threat Intelligence Analyzer

Normalizes offline indicators of compromise and matches them against an
authorized evidence export. It supports IPs, domains, URLs, and hashes without
calling external services or leaking evidence.

```bash
python -m threat_intel threat_intel/samples/iocs.txt threat_intel/samples/evidence.log
```
