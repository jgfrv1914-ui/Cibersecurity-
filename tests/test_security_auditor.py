"""Tests for the read-only Linux hardening auditor."""
import unittest

from security_auditor.core import audit_snapshot


class SecurityAuditorTests(unittest.TestCase):
    def test_flags_weak_snapshot(self):
        findings = audit_snapshot(["ssh_root_login=yes", "firewall=inactive"])
        failed = {finding.check_id for finding in findings if finding.status == "FAIL"}
        self.assertIn("SSH-001", failed)
        self.assertIn("FW-001", failed)

    def test_hardened_snapshot_has_no_ssh_root_login_failure(self):
        findings = audit_snapshot(["ssh_root_login=no", "firewall=active"])
        failed = {finding.check_id for finding in findings if finding.status == "FAIL"}
        self.assertNotIn("SSH-001", failed)
        self.assertNotIn("FW-001", failed)


if __name__ == "__main__":
    unittest.main()
