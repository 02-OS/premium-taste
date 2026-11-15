"""Generated site data keeps direction notes, type styles, and a fresh data.js."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_site_data  # noqa: E402
import check_catalog  # noqa: E402


class BuildSiteDataTests(unittest.TestCase):
    def test_choose_and_register_note_stay_out_of_the_direction_list(self) -> None:
        payload = build_site_data.build_payload()
        self.assertEqual([item["id"] for item in payload["directions"]], [
            "quiet-luxury",
            "cinematic-dark",
            "precise-technical",
            "editorial-print",
        ])
        self.assertEqual(len(payload["choose"]), 6)
        self.assertIn("generic skeleton", payload["registerNote"])
        self.assertEqual(payload["counts"]["principles"], 68)
        self.assertEqual(payload["counts"]["antiPatterns"], 30)
        self.assertEqual(payload["counts"]["references"], 18)
        self.assertEqual(payload["counts"]["patterns"], 12)
        self.assertEqual(payload["counts"]["directions"], 4)

    def test_dtcg_keeps_font_style_and_design_md_keeps_status_colors(self) -> None:
        pack = build_site_data.parse_tokens()["cinematic-dark"]
        exported = build_site_data.render_dtcg(pack)
        self.assertEqual(exported["typography"]["credit"]["$value"]["fontStyle"], "italic")
        rendered = build_site_data.render_design_md(
            "precise-technical",
            build_site_data.parse_tokens()["precise-technical"],
        )
        self.assertIn('danger:', rendered)
        self.assertIn('warning:', rendered)

    def test_check_fails_when_data_js_is_stale(self) -> None:
        path = ROOT / "site" / "data.js"
        original = path.read_text(encoding="utf-8")
        try:
            path.write_text(original + "\n// stale\n", encoding="utf-8")
            self.assertEqual(build_site_data.main(["--check"]), 1)
        finally:
            path.write_text(original, encoding="utf-8")
        self.assertEqual(build_site_data.main(["--check"]), 0)

    def test_catalog_accepts_plugins_tokens_and_reference_ids(self) -> None:
        self.assertEqual(check_catalog.main(), 0)


if __name__ == "__main__":
    unittest.main()
