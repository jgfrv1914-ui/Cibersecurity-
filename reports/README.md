# Sample reports

Committed output artifacts produced by the tools in this repository. They exist
so a reviewer can see real results without running anything, and so changes in
output format show up in a diff.

| File | Produced by |
|---|---|
| [`soc_toolkit_sample_report.json`](soc_toolkit_sample_report.json) | `python -m soc_toolkit soc_toolkit/samples/auth.log --ioc-file soc_toolkit/samples/iocs.txt --threshold 3` |

All input is synthetic. Addresses come from the documentation ranges reserved by
RFC 5737 (`203.0.113.0/24`, `198.51.100.0/24`), so nothing here points at a real
host.

## Regenerating

```bash
python -m soc_toolkit soc_toolkit/samples/auth.log \
  --ioc-file soc_toolkit/samples/iocs.txt \
  --threshold 3 > reports/soc_toolkit_sample_report.json
```

The `generated_at_utc` timestamp changes on every run; that is the only expected
difference.
