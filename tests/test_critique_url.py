"""URL critique: masking, mobile metrics, and HTTP safety. No browser is launched."""

from __future__ import annotations

import sys
import unittest
import urllib.error
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import critique_url  # noqa: E402


CATALOG = (ROOT / "taste" / "principles.yaml").read_text(encoding="utf-8") + (
    ROOT / "taste" / "anti-patterns.yaml"
).read_text(encoding="utf-8")


class CritiqueUrlTests(unittest.TestCase):
    def test_unmask_matches_bytewise_xor(self) -> None:
        payload = b"hello world!!"
        mask = b"\x01\x02\x03\x04"
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        self.assertEqual(critique_url._unmask_payload(masked, mask), payload)

    def test_mobile_findings_cover_contrast_and_do_not_invent_body_size(self) -> None:
        findings = critique_url.dom_metrics_to_findings(
            "https://example.com/",
            {
                "h1Count": 1,
                "bodyFontSize": None,
                "targetWidth": 1280,
                "innerWidth": 1280,
                "scrollWidth": 1280,
            },
            {
                "h1Count": 1,
                "bodyFontSize": None,
                "targetWidth": 375,
                "innerWidth": 375,
                "scrollWidth": 375,
                "contrastFailures": [
                    {"ratio": 2.1, "threshold": 4.5, "element": "p", "text": "muted"}
                ],
            },
            set(),
        )
        contrast = [item for item in findings if item.rule == "color.contrast"]
        self.assertTrue(contrast)
        self.assertTrue(any(item.message.startswith("mobile:") for item in contrast))
        self.assertFalse(any(item.rule == "a11y.size" for item in findings))
        absent = critique_url.dom_metrics_to_findings(
            "https://example.com/",
            {},
            {"h1Count": 1},
            set(),
        )
        self.assertFalse(any(item.rule == "a11y.size" for item in absent))

    def test_reported_rule_ids_exist_in_the_catalog(self) -> None:
        findings = critique_url.dom_metrics_to_findings(
            "https://example.com/",
            {
                "h1Count": 2,
                "overflowX": True,
                "targetWidth": 1280,
                "innerWidth": 1280,
                "scrollWidth": 1400,
                "fonts": ["Inter", "Newsreader", "IBM Plex Sans"],
                "bodyFontSize": 12,
                "radii": ["2px", "4px", "8px", "16px"],
                "inFlowShadows": ["card"],
                "contrastFailures": [{"ratio": 2, "threshold": 4.5, "element": "p", "text": "x"}],
                "smallTargets": [{"element": "a", "text": "go", "size": "10x10"}],
                "unlabeledControls": [{"element": "input", "name": "email"}],
                "firstFoldButtons": ["Buy", "Learn"],
            },
            {},
            set(),
        )
        self.assertTrue(findings)
        for item in findings:
            self.assertIn(item.rule, CATALOG)
            self.assertNotEqual(item.dimension, "typography")

    def test_assert_http_url_rejects_non_http_and_path_escape(self) -> None:
        for url in ("file:///etc/passwd", "javascript:alert(1)", "http://example.com//secret", "http://example.com/a\\b"):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    critique_url.assert_http_url(url)

    def test_http_fallback_reports_url_errors(self) -> None:
        with mock.patch("critique_url.urllib.request.urlopen", side_effect=urllib.error.URLError("down")):
            meta, findings = critique_url.inspect_http_fallback("https://example.com/", set())
        self.assertIn("error", meta)
        self.assertEqual(findings, [])

        def fail_document(*_args, **_kwargs):
            raise urllib.error.HTTPError("https://example.com/", 500, "nope", hdrs=None, fp=None)

        with mock.patch("critique_url.urllib.request.urlopen", side_effect=fail_document):
            meta, findings = critique_url.inspect_http_fallback("https://example.com/page", set())
        self.assertIn("error", meta)
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
