"""Tests for the offline SOC Toolkit."""
import json
import unittest

from soc_toolkit.core import (
    build_report,
    detect_brute_force,
    match_iocs,
    parse_auth_log,
)


class SOCToolkitTests(unittest.TestCase):
    def setUp(self):
        self.lines = [
            "Sep 22 09:10:01 host sshd: Failed password for invalid user admin from 203.0.113.45 port 42001 ssh2",
            "Sep 22 09:10:08 host sshd: Failed password for invalid user admin from 203.0.113.45 port 42002 ssh2",
            "Sep 22 09:10:15 host sshd: Failed password for user fernando from 203.0.113.45 port 42003 ssh2",
            "Sep 22 09:12:21 host sshd: Failed password for user guest from 198.51.100.24 port 43100 ssh2",
        ]

    def test_detects_threshold_and_preserves_users(self):
        events = parse_auth_log(self.lines)
        alerts = detect_brute_force(events, threshold=3)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].evidence["source_ip"], "203.0.113.45")
        self.assertEqual(alerts[0].evidence["target_users"], ["admin", "fernando"])

    def test_matches_exact_indicator(self):
        events = parse_auth_log(self.lines)
        alerts = match_iocs(events, ["203.0.113.45"])
        self.assertEqual(len(alerts), 3)
        self.assertTrue(all(alert.alert_type == "ioc_match" for alert in alerts))

    def test_indicator_does_not_match_a_longer_address(self):
        """Regression: `10.0.0.1` must not match `10.0.0.11` (substring bug)."""
        events = parse_auth_log(
            [
                "Sep 22 09:10:01 host sshd: Failed password for user root from 10.0.0.11 port 42001 ssh2"
            ]
        )
        self.assertEqual(match_iocs(events, ["10.0.0.1"]), [])
        self.assertEqual(len(match_iocs(events, ["10.0.0.11"])), 1)

    def test_report_is_json_serializable_and_counts_severities(self):
        events = parse_auth_log(self.lines)
        alerts = detect_brute_force(events, threshold=3)
        report = build_report(events, alerts, source="auth.log")
        self.assertEqual(report["summary"]["events_analyzed"], 4)
        self.assertEqual(report["summary"]["severity_counts"], {"high": 1})
        json.dumps(report)

    def test_rejects_invalid_threshold(self):
        with self.assertRaises(ValueError):
            detect_brute_force([], threshold=0)


if __name__ == "__main__":
    unittest.main()
