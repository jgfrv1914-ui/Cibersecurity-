"""Offline tests for the standalone command-line tools.

The tools are single-file scripts rather than packages, so they are loaded
by path. All assertions stay offline: no network, no filesystem mutation.
"""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).parents[1]


def load(relative_path: str):
    """Import a standalone script by path and return the module object."""
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class PortScannerTests(unittest.TestCase):
    def test_port_ranges_are_parsed_and_deduplicated(self):
        module = load("red_team/tcp_port_scanner.py")
        self.assertEqual(
            module.parse_ports("80,443,80,8000-8002"), [80, 443, 8000, 8001, 8002]
        )


class PasswordStrengthTests(unittest.TestCase):
    def test_report_never_echoes_the_password(self):
        module = load("blue_team/password_strength_analyzer.py")
        report = module.analyze("Correct-Horse-Battery-Staple-2040")
        self.assertGreaterEqual(report["length"], 12)
        self.assertNotIn("password", report)


class EntropyScannerTests(unittest.TestCase):
    def test_entropy_extremes(self):
        module = load("blue_team/file_entropy_scanner.py")
        self.assertEqual(module.entropy(b""), 0.0)
        self.assertEqual(module.entropy(b"A" * 100), 0.0)
        self.assertGreater(module.entropy(bytes(range(256))), 7.9)


class LogAnalyzerTests(unittest.TestCase):
    def test_flags_authentication_failures_and_counts_addresses(self):
        module = load("blue_team/log_analyzer.py")
        addresses, alerts = module.analyze(
            [
                "Failed password for invalid user root from 203.0.113.45",
                "GET /?id=1 UNION SELECT 1 HTTP/1.1 403 from 198.51.100.24",
            ]
        )
        self.assertEqual(addresses["203.0.113.45"], 1)
        self.assertEqual(alerts["authentication_failure"], 1)
        self.assertEqual(alerts["injection_probe"], 1)


if __name__ == "__main__":
    unittest.main()
