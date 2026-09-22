# Test suite

Offline unit tests for the portfolio. **No test touches the network or modifies
the filesystem**, so the suite is safe to run anywhere and reproducible in CI.

```bash
python -m unittest discover -s tests -v
```

| File | Covers |
|---|---|
| [`test_soc_toolkit.py`](test_soc_toolkit.py) | Log parsing, brute-force thresholds, IOC correlation, report shape |
| [`test_security_auditor.py`](test_security_auditor.py) | Hardening checks on weak and hardened snapshots |
| [`test_threat_intel.py`](test_threat_intel.py) | Indicator normalization, classification, and matching |
| [`test_cli_tools.py`](test_cli_tools.py) | Standalone tools: port range parsing, password reporting, entropy, log classification |

## Notable regression test

`test_indicator_does_not_match_a_longer_address` pins a real bug found in this
codebase: IOC correlation originally used a substring check, so the indicator
`10.0.0.1` alerted on `10.0.0.11` and `210.0.0.1`. Matching is now
delimiter-aware and the test fails if that regresses.

## Loading standalone scripts

The tools in `blue_team/`, `red_team/`, and `utilities/` are single-file scripts
rather than packages. `test_cli_tools.py` imports them by path with
`importlib.util`, which is why they are named as valid Python identifiers.
