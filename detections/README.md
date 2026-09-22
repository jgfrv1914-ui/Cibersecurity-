# Detection Rules

Two Sigma-style defensive rules for lab validation and future SIEM integration:

- `brute_force_ssh.yml` maps repeated SSH failures to MITRE ATT&CK T1110.
- `new_admin_user.yml` highlights suspicious administrative account creation.

These rules are intentionally marked experimental and require tuning against
the target log source before production use.
