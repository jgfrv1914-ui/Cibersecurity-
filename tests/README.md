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
| [`test_cli_tools.py`](test_cli_tools.py) | Standalone tools: port parsing, password scoring and commonality, entropy, log classification, sshd log formats |

## Notable regression tests

Each of these pins a real defect found in this codebase, three of them by
running every tool end to end rather than by reading the code:

- `test_indicator_does_not_match_a_longer_address` — IOC correlation used a
  substring check, so `10.0.0.1` alerted on `10.0.0.11` and `210.0.0.1`.
- `test_decorated_common_passwords_are_flagged` — the commonality check compared
  for exact equality against seven words, so `password123` scored 74/100.
- `test_regex_matches_both_sshd_variants` — the failed-login regex handled only
  the `invalid user` form, and counting was grouped per source/username pair,
  which missed password spraying entirely.

## Loading standalone scripts

The tools in `blue_team/`, `red_team/`, and `utilities/` are single-file scripts
rather than packages. `test_cli_tools.py` imports them by path with
`importlib.util`, which is why they are named as valid Python identifiers.
