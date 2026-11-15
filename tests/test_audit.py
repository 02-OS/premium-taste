"""Static auditor behavior that the open issues require."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit  # noqa: E402


class AuditTests(unittest.TestCase):
    def test_empower_is_in_the_shared_cliche_list(self) -> None:
        self.assertTrue(any("empower" in pattern for pattern in audit.ABSTRACT_CLICHES))

    def test_score_dimensions_are_the_six_named_axes(self) -> None:
        scores = audit.score_dimensions([])
        self.assertEqual(
            set(scores),
            {"hierarchy", "spacing", "uniqueness", "restraint", "accessibility", "product_fit"},
        )

    def test_case_insensitive_font_families_count_once(self) -> None:
        text = (
            '.a { font-family: "IBM Plex Sans", sans-serif; }\n'
            '.b { font-family: "ibm plex sans", sans-serif; }\n'
        )
        rules = [item.rule for item in audit.audit_text(text, "type.css")]
        self.assertNotIn("type.two-families", rules)

    def test_hex_rgb_hsl_and_one_var_hop_share_a_contrast_finding(self) -> None:
        text = (
            ":root { --ink: #ffffff; --paper: #ffffff; }\n"
            ".hex { color: #ffffffff; background: #ffffff; }\n"
            ".rgb { color: rgb(255, 255, 255); background-color: rgba(255, 255, 255, 0.9); }\n"
            ".hsl { color: hsl(0, 0%, 100%); background: hsl(0 0% 100%); }\n"
            ".var { color: var(--ink); background: var(--paper); }\n"
        )
        findings = [item for item in audit.audit_text(text, "contrast.css") if item.rule == "color.contrast"]
        self.assertGreaterEqual(len(findings), 4)

    def test_html_for_counts_as_a_label(self) -> None:
        text = (
            '<label htmlFor="email">Email</label>\n'
            '<input id="email" placeholder="name@studio.test" />\n'
        )
        rules = [item.rule for item in audit.audit_text(text, "form.jsx")]
        self.assertNotIn("a11y.placeholder-label", rules)

    def test_greater_than_inside_quotes_does_not_split_the_tag(self) -> None:
        text = (
            '<div class="actions">\n'
            '  <a class="btn" title="next > item">One</a>\n'
            '  <a class="btn">Two</a>\n'
            "</div>\n"
        )
        rules = [item.rule for item in audit.audit_text(text, "actions.html")]
        self.assertIn("chrome.two-primaries", rules)

    def test_balanced_divs_see_both_primary_actions(self) -> None:
        text = (
            '<div class="actions">\n'
            '  <div class="card">\n'
            '    <a class="btn">One</a>\n'
            "  </div>\n"
            '  <a class="btn">Two</a>\n'
            "</div>\n"
        )
        rules = [item.rule for item in audit.audit_text(text, "nested.html")]
        self.assertIn("chrome.two-primaries", rules)

    def test_script_copy_is_not_a_visible_cliche(self) -> None:
        text = (
            "<script>\n"
            'const pitch = "unlock your potential";\n'
            "</script>\n"
            "<p>unlock the kiln schedule</p>\n"
        )
        findings = [item for item in audit.audit_text(text, "copy.html") if item.rule == "content.abstract-verbs"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line, 4)

    def test_css_comment_newlines_keep_taste_ignore_on_the_rule_line(self) -> None:
        text = (
            "/* header\n"
            "   still a comment */\n"
            ".bad { color: #ffffff; background-color: #ffffff; } /* taste-ignore: color.contrast */\n"
        )
        rules = [item.rule for item in audit.audit_text(text, "ignored.css")]
        self.assertNotIn("color.contrast", rules)

    def test_css_file_with_a_div_comment_is_still_css(self) -> None:
        text = "/* <div class=\"actions\"> */\n.bad { color: #ffffff; background: #ffffff; }\n"
        rules = [item.rule for item in audit.audit_text(text, "widget.css")]
        self.assertIn("color.contrast", rules)

    def test_allow_font_skips_a_named_costume_face(self) -> None:
        text = "body { font-family: Inter, sans-serif; }\n"
        blocked = [item.rule for item in audit.audit_text(text, "face.css")]
        allowed = [item.rule for item in audit.audit_text(text, "face.css", allow_fonts={"Inter"})]
        self.assertIn("type.avoid-tells", blocked)
        self.assertNotIn("type.avoid-tells", allowed)

    def test_empty_directory_is_not_a_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(audit.main([tmp]), 2)

    def test_fail_on_error_ignores_warnings_and_exclude_skips_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "warn.css").write_text("a { color: #4f46e5; }\n", encoding="utf-8")
            (root / "bad.html").write_text("<p>unlock the thing</p>\n", encoding="utf-8")
            (root / "ok.html").write_text("<p>A bowl from this firing.</p>\n", encoding="utf-8")
            self.assertEqual(audit.main([str(root / "warn.css"), "--fail-on", "error"]), 0)
            self.assertEqual(audit.main([str(root / "warn.css")]), 1)
            self.assertEqual(audit.main([tmp, "--exclude", "bad.html", "--exclude", "warn.css"]), 0)

    def test_before_specimens_fail_and_after_specimens_pass(self) -> None:
        before = list((ROOT / "examples").glob("*-before.html"))
        after = list((ROOT / "examples").glob("*-after.html"))
        self.assertTrue(before)
        self.assertTrue(after)
        for path in before:
            self.assertTrue(audit.audit_text(path.read_text(encoding="utf-8"), path.name), path.name)
        for path in after:
            findings = audit.audit_text(path.read_text(encoding="utf-8"), str(path))
            self.assertEqual([(item.rule, item.line) for item in findings], [], path.name)

    def test_line_for_offset_counts_newlines_before_the_offset(self) -> None:
        text = "a\nb\nc"
        newlines = audit.newline_index(text)
        self.assertEqual(audit.line_for_offset(text, 0, newlines), 1)
        self.assertEqual(audit.line_for_offset(text, 2, newlines), 2)
        self.assertEqual(audit.line_for_offset(text, 4, newlines), 3)


if __name__ == "__main__":
    unittest.main()
