# Secure Configuration Auditor

Read-only hardening checks against a local, exported configuration snapshot.
It never changes the host and does not require administrator privileges.

```bash
python -m security_auditor security_auditor/samples/linux_snapshot.txt
```

The sample checks SSH root login, SSH password authentication, firewall state,
and audit logging. Use only snapshots from systems you own or are authorized to
assess.
