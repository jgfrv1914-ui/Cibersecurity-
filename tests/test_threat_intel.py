"""Tests for offline indicator normalization and matching."""
import unittest

from threat_intel.core import classify, find_matches, normalize


class ThreatIntelTests(unittest.TestCase):
    def test_normalize_deduplicates(self):
        indicators = normalize(["203.0.113.45", "203.0.113.45", "malware.example"])
        self.assertEqual(len(indicators), 2)

    def test_classify_recognizes_ipv4(self):
        self.assertEqual(classify("203.0.113.45"), "ipv4")

    def test_find_matches_locates_indicator_in_evidence(self):
        indicators = normalize(["203.0.113.45"])
        self.assertEqual(len(find_matches("source=203.0.113.45", indicators)), 1)


if __name__ == "__main__":
    unittest.main()
