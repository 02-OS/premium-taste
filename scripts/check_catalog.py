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

    linked = re.findall(r"^\s+- ([a-z0-9-]+)\s*$", direction_text, re.M)
    # The direction file also lists jobs as "- a phrase". Keep only ids that exist as references.
    for ref_id in linked:
        if ref_id in files or ref_id in index_ids:
            if ref_id not in index_ids:
                fail(errors, f"directions.yaml lists unknown reference {ref_id}")
    for ref_id in index_ids:
        if f"- {ref_id}" not in direction_text and f"- {ref_id}\n" not in direction_text:
            # referenced from the references: block, which uses "  - id" form inside directions
            if f"      - {ref_id}" not in direction_text:
                fail(errors, f"reference {ref_id} is not listed under a direction")

    # Validate screen & flow patterns
    pat_dir = ROOT / "taste" / "patterns"
    pat_index = pat_dir / "index.yaml"
    if not pat_index.exists():
        fail(errors, "missing taste/patterns/index.yaml")
        pat_ids: list[str] = []
    else:
        pat_index_text = read(pat_index)
        pat_ids = re.findall(r"^\s+- id:\s*([a-z0-9-]+)\s*$", pat_index_text, re.M)
        if len(pat_ids) != len(set(pat_ids)):
            fail(errors, "duplicate id in taste/patterns/index.yaml")
        pat_files = {
            p.stem for p in pat_dir.glob("*.md") if p.name not in {"README.md", "_template.md"}
        }
        if set(pat_ids) != pat_files:
            missing = pat_files - set(pat_ids)
            extra = set(pat_ids) - pat_files
            if missing:
                fail(errors, f"pattern files not in index: {sorted(missing)}")
            if extra:
                fail(errors, f"pattern index ids with no file: {sorted(extra)}")
        for pat_id in pat_ids:
            path = pat_dir / f"{pat_id}.md"
            if not path.exists():
                continue
            text = read(path)
            matter = frontmatter(text)
            m_ids = re.findall(r"^id:\s*(\S+)\s*$", matter, re.M)
            if m_ids != [pat_id]:
                fail(errors, f"patterns/{path.name} frontmatter id is {m_ids}, expected {pat_id}")
            t_match = re.search(r"^type:\s*(\S+)\s*$", matter, re.M)
            if not t_match or t_match.group(1) not in {"screen", "flow"}:
                fail(errors, f"patterns/{path.name} must declare type: screen or flow")
            for key in ("title:", "directions:", "job:", "tags:"):
                if key not in matter:
                    fail(errors, f"patterns/{path.name} frontmatter missing {key[:-1]}")
            dir_block = re.search(r"^directions:\s*\n((?:\s+-\s+.+\n?)+)", matter, re.M)
            if dir_block:
                for d_ln in dir_block.group(1).splitlines():
                    d_val = d_ln.strip().lstrip("- ").strip()
                    if d_val and d_val not in DIRECTIONS:
                        fail(errors, f"patterns/{path.name} references unknown direction {d_val}")
            for heading in (
                "## Layout & Hierarchy",
                "## Required States & Mechanics",
                "## What to Include",
                "## What to Refuse",
                "## Litmus Check",
            ):
                if heading not in text:
                    fail(errors, f"patterns/{path.name} missing section {heading}")

    # Validate Extended DESIGN.md token files
    for direction in DIRECTIONS:
        tpath = ROOT / "tokens" / f"{direction}.DESIGN.md"
        if not tpath.exists():
            fail(errors, f"missing tokens/{direction}.DESIGN.md")
            continue
        ttext = read(tpath)
        tmatter = frontmatter(ttext)
        for key in ("name:", "direction:", "scale:", "opentype:", "surfaces:", "colors:", "typography:"):
            if key not in tmatter:
                fail(errors, f"{tpath.name} frontmatter missing {key[:-1]}")
        for heading in ("## Surfaces", "## Type Scale Detail", "## Imagery", "## Agent Prompt Guide"):
            if heading not in ttext:
                fail(errors, f"{tpath.name} missing section {heading}")

    # Validate multi-platform plugin manifests if present
    for rel in (
        ".mcp.json",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
        ".cursor-plugin/plugin.json",
        ".codex-plugin/plugin.json",
        "gemini-extension.json",
    ):
        mpath = ROOT / rel
        if mpath.exists():
            try:
                json.loads(read(mpath))
            except json.JSONDecodeError as exc:
                fail(errors, f"invalid JSON in {rel}: {exc}")

    if errors:
        print(f"{len(errors)} catalog error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1

    print(
        f"ok: {len(principle_ids)} principles, {len(anti_ids)} anti-patterns, "
        f"{len(index_ids)} references, {len(pat_ids)} patterns"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
