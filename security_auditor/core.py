"""Dependency-free checks against exported Linux security configuration."""

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    check_id: str
    severity: str
    status: str
    title: str
    evidence: str


def audit_snapshot(lines: Iterable[str]) -> list[Finding]:
    """Audit key-value snapshot lines without changing the host system."""
    values = {}
    for line in lines:
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().lower()

    # check_id, severity, snapshot key, title, expected value, remediation
    checks = [
        (
            "SSH-001", "high", "ssh_root_login",
            "SSH root login disabled", "no",
            "Disable PermitRootLogin.",
        ),
        (
            "SSH-002", "high", "ssh_password_auth",
            "SSH password authentication disabled", "no",
            "Prefer key-based authentication.",
        ),
        (
            "FW-001", "high", "firewall",
            "Host firewall enabled", "active",
            "Enable and verify the host firewall.",
        ),
        (
            "AUD-001", "medium", "audit_logging",
            "Audit logging enabled", "yes",
            "Enable audit logging for investigation.",
        ),
    ]
    findings = []
    for check_id, severity, key, title, expected, remediation in checks:
        actual = values.get(key, "missing")
        passed = actual == expected
        findings.append(
            Finding(
                check_id=check_id,
                severity="info" if passed else severity,
                status="PASS" if passed else "FAIL",
                title=title,
                evidence=f"{key}={actual}; remediation: {remediation}",
            )
        )
    return findings


def load_snapshot(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()
