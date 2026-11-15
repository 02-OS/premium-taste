"""site/auditor.js and scripts/audit.py report the same rule, line, and severity."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit  # noqa: E402

NODE = shutil.which("node")

JS = r"""
const fs = require("fs");
const vm = require("vm");
const spec = JSON.parse(fs.readFileSync(0, "utf8"));
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(process.env.AUDITOR, "utf8"), sandbox);
const result = sandbox.PremiumTasteAudit.auditCode(spec.text, spec.label, {allowFonts: spec.allowFonts || []});
const slim = result.findings.map(function (finding) {
  return {rule: finding.rule, line: finding.line, severity: finding.severity};
});
process.stdout.write(JSON.stringify(slim));
"""

CASES = {
    "empower": ("<p>This product will empower every team.</p>\n", "copy.html", []),
    "families": (
        '.a { font-family: "IBM Plex Sans", sans-serif; }\n.b { font-family: "ibm plex sans", sans-serif; }\n',
        "type.css",
        [],
    ),
    "contrast": (
        ":root { --ink: #ffffff; --paper: #ffffff; }\n"
        ".hex { color: #ffffffff; background: #ffffff; }\n"
        ".rgb { color: rgb(255, 255, 255); background-color: rgba(255, 255, 255, 0.9); }\n"
        ".hsl { color: hsl(0, 0%, 100%); background: hsl(0 0% 100%); }\n"
        ".var { color: var(--ink); background: var(--paper); }\n",
        "contrast.css",
        [],
    ),
    "htmlFor": (
        '<label htmlFor="email">Email</label>\n<input id="email" placeholder="name@studio.test" />\n',
        "form.jsx",
        [],
    ),
    "quoted-gt": (
        '<div class="actions">\n  <a class="btn" title="next > item">One</a>\n  <a class="btn">Two</a>\n</div>\n',
        "actions.html",
        [],
    ),
    "nested": (
        '<div class="actions">\n  <div class="card">\n    <a class="btn">One</a>\n  </div>\n  <a class="btn">Two</a>\n</div>\n',
        "nested.html",
        [],
    ),
    "unlock": (
        '<script>\nconst pitch = "unlock your potential";\n</script>\n<p>unlock the kiln schedule</p>\n',
        "copy.html",
        [],
    ),
    "ignore": (
        "/* header\n   still a comment */\n.bad { color: #ffffff; background-color: #ffffff; } /* taste-ignore: color.contrast */\n",
        "ignored.css",
        [],
    ),
    "css-div": (
        '/* <div class="actions"> */\n.bad { color: #ffffff; background: #ffffff; }\n',
        "widget.css",
        [],
    ),
    "allow": ("body { font-family: Inter, sans-serif; }\n", "face.css", ["Inter"]),
}


@unittest.skipUnless(NODE, "node is required to execute site/auditor.js")
class AuditorParityTests(unittest.TestCase):
    def findings(self, text: str, label: str, allow: list[str]) -> list[dict]:
        python = [
            {"rule": item.rule, "line": item.line, "severity": item.severity}
            for item in audit.audit_text(text, label, allow_fonts=set(allow))
        ]
        proc = subprocess.run(
            [NODE, "-e", JS],
            input=json.dumps({"text": text, "label": label, "allowFonts": allow}).encode(),
            capture_output=True,
            check=False,
            env={**os.environ, "AUDITOR": str(ROOT / "site" / "auditor.js")},
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode())
        javascript = json.loads(proc.stdout.decode())
        self.assertEqual(javascript, python)
        return python

    def test_shared_snippets_match(self) -> None:
        for name, (text, label, allow) in CASES.items():
            with self.subTest(name=name):
                self.findings(text, label, allow)

    def test_allow_font_removes_the_costume_finding(self) -> None:
        blocked = self.findings(CASES["allow"][0], "face.css", [])
        allowed = self.findings(CASES["allow"][0], "face.css", ["Inter"])
        self.assertIn("type.avoid-tells", [item["rule"] for item in blocked])
        self.assertNotIn("type.avoid-tells", [item["rule"] for item in allowed])


if __name__ == "__main__":
    unittest.main()
