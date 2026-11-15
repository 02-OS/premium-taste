#!/usr/bin/env python3
"""Check that Premium Taste ids, directions, and reference files agree.

No dependencies beyond the standard library. Run from anywhere:

    python3 scripts/check_catalog.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit  # noqa: E402
import build_site_data  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DIRECTIONS = ("quiet-luxury", "cinematic-dark", "precise-technical", "editorial-print")
ID_LINE = re.compile(r"^[\s-]*id:\s*([a-z0-9][a-z0-9.-]*)\s*$", re.M)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ids_in(path: Path) -> list[str]:
    return ID_LINE.findall(read(path))


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[:end]


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def direction_reference_ids(text: str) -> list[str]:
    found: list[str] = []
    in_refs = False
    for line in text.splitlines():
        if re.match(r"^    references:\s*$", line):
            in_refs = True
            continue
        if not in_refs:
            continue
        match = re.match(r"^      - ([a-z0-9-]+)\s*$", line)
        if match:
            found.append(match.group(1))
            continue
        if line.strip() and not line.startswith("      "):
            in_refs = False
    return found


def check_plugins(errors: list[str]) -> None:
    manifests = {
        ".claude-plugin/plugin.json": "${CLAUDE_PLUGIN_ROOT}",
        ".cursor-plugin/plugin.json": "${CURSOR_PLUGIN_ROOT}",
        ".codex-plugin/plugin.json": "mcpServers",
        "gemini-extension.json": "${extensionPath}",
    }
    for rel, marker in manifests.items():
        path = ROOT / rel
        if not path.is_file():
            fail(errors, f"missing plugin manifest {rel}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            fail(errors, f"{rel} is not valid JSON")
            continue
        if not isinstance(data, dict):
            fail(errors, f"{rel} must be a JSON object")
            continue
        if data.get("version") != "1.1.0":
            fail(errors, f"{rel} version is {data.get('version')}, expected 1.1.0")
        if "mcpServers" not in data:
            fail(errors, f"{rel} is missing mcpServers")
        blob = json.dumps(data)
        if re.search(r'"scripts/mcp_server\.py"', blob):
            fail(errors, f"{rel} uses a bare scripts/mcp_server.py path")
        if marker not in blob:
            fail(errors, f"{rel} is missing {marker}")
        skills = data.get("skills")
        if isinstance(skills, str):
            skill_root = (ROOT / skills.lstrip("./")).resolve()
            if not skill_root.is_dir() or not any(skill_root.glob("*/SKILL.md")):
                fail(errors, f"{rel} skills path {skills} has no skill directory")
    server = (ROOT / "scripts" / "mcp_server.py").read_text(encoding="utf-8")
    if 'SERVER_VERSION = "1.1.0"' not in server:
        fail(errors, "mcp_server.py version is not 1.1.0")


def check_token_packs(errors: list[str]) -> None:
    packs = build_site_data.parse_tokens()
    for direction, pack in packs.items():
        colors = pack.get("colors") or {}
        for fg_name, bg_name in (("ink", "surface"), ("ink-muted", "surface"), ("on-accent", "accent")):
            fg = colors.get(fg_name)
            bg = colors.get(bg_name)
            if not fg or not bg:
                continue
            ratio = audit.contrast_ratio(str(fg), str(bg))
            if ratio is not None and ratio < 4.5:
                fail(
                    errors,
                    f"{direction} primary text {fg_name} on {bg_name} is {ratio:.2f}:1, under WCAG AA 4.5:1",
                )
        dtcg = build_site_data.render_dtcg(pack)
        if not dtcg.get("color"):
            fail(errors, f"{direction} DTCG export has no color tokens")
        for role, spec in (pack.get("typography") or {}).items():
            if isinstance(spec, dict) and "fontStyle" in spec:
                exported = ((dtcg.get("typography") or {}).get(role) or {}).get("$value") or {}
                if exported.get("fontStyle") != spec["fontStyle"]:
                    fail(errors, f"{direction} DTCG dropped fontStyle on {role}")
        rendered = build_site_data.render_design_md(pack)
        for key in ("danger", "warning"):
            if key in colors and f"{key}:" not in rendered:
                fail(errors, f"{direction} DESIGN.md export dropped {key}")


def main() -> int:
    errors: list[str] = []

    principles_yaml = ROOT / "taste" / "principles.yaml"
    principles_md = ROOT / "taste" / "principles.md"
    anti_yaml = ROOT / "taste" / "anti-patterns.yaml"
    index = ROOT / "taste" / "references" / "index.yaml"
    directions = ROOT / "taste" / "directions.yaml"
    ref_dir = ROOT / "taste" / "references"

    principle_ids = ids_in(principles_yaml)
    if len(principle_ids) != len(set(principle_ids)):
        fail(errors, "duplicate id in taste/principles.yaml")
    md = read(principles_md)
    for rule_id in principle_ids:
        if rule_id not in md:
            fail(errors, f"principle id missing from principles.md: {rule_id}")

    heading_ids = re.findall(r"^### `([a-z0-9.-]+)`", md, re.M)
    for rule_id in heading_ids:
        if rule_id not in principle_ids:
            fail(errors, f"principles.md heading has no yaml rule: {rule_id}")

    anti_ids = ids_in(anti_yaml)
    if len(anti_ids) != len(set(anti_ids)):
        fail(errors, "duplicate id in taste/anti-patterns.yaml")
    for anti_id in anti_ids:
        if anti_id not in md:
            fail(errors, f"anti-pattern id missing from principles.md: {anti_id}")

    direction_text = read(directions)
    for direction in DIRECTIONS:
        if f"id: {direction}" not in direction_text:
            fail(errors, f"direction missing from directions.yaml: {direction}")

    index_text = read(index)
    index_ids = re.findall(r"^\s+- id:\s*([a-z0-9-]+)\s*$", index_text, re.M)
    if len(index_ids) != len(set(index_ids)):
        fail(errors, "duplicate id in references/index.yaml")

    files = {
        path.stem
        for path in ref_dir.glob("*.md")
        if path.name not in {"README.md", "_template.md"}
    }
    if set(index_ids) != files:
        missing = files - set(index_ids)
        extra = set(index_ids) - files
        if missing:
            fail(errors, f"reference files not in index: {sorted(missing)}")
        if extra:
            fail(errors, f"index ids with no file: {sorted(extra)}")

    for ref_id in index_ids:
        path = ref_dir / f"{ref_id}.md"
        if not path.exists():
            continue
        matter = frontmatter(read(path))
        matter_ids = re.findall(r"^id:\s*(\S+)\s*$", matter, re.M)
        if matter_ids != [ref_id]:
            fail(errors, f"{path.name} frontmatter id is {matter_ids}, expected {ref_id}")
        direction_match = re.search(r"^direction:\s*(\S+)\s*$", matter, re.M)
        if not direction_match or direction_match.group(1) not in DIRECTIONS:
            found = direction_match.group(1) if direction_match else "missing"
            fail(errors, f"{path.name} has unknown direction {found}")
        for key in ("title:", "url:", "job:", "confidence:", "observed:"):
            if key not in matter:
                fail(errors, f"{path.name} frontmatter missing {key[:-1]}")
        body = read(path)
        for heading in (
            "## Description",
            "## Key decisions",
            "## Why it works",
            "## What to steal",
            "## What not to copy",
            "## Uniqueness",
            "## Product fit",
            "## Source note",
        ):
            if heading not in body:
                fail(errors, f"{path.name} missing section {heading}")

    for ref_id in direction_reference_ids(direction_text):
        if ref_id not in index_ids or ref_id not in files:
            fail(errors, f"directions.yaml lists unknown reference {ref_id}")
    check_plugins(errors)
    check_token_packs(errors)
    for ref_id in index_ids:
        if f"- {ref_id}" not in direction_text and f"- {ref_id}\n" not in direction_text:
            # referenced from the references: block, which uses "  - id" form inside directions
            if f"      - {ref_id}" not in direction_text:
                fail(errors, f"reference {ref_id} is not listed under a direction")

    if errors:
        print(f"{len(errors)} catalog error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1

    print(
        f"ok: {len(principle_ids)} principles, {len(anti_ids)} anti-patterns, "
        f"{len(index_ids)} references"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
