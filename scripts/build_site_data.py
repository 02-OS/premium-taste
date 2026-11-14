#!/usr/bin/env python3
"""Generate site/data.js directly from taste/ and tokens/ using stdlib only.

Run whenever references, directions, anti-patterns, or tokens change:

    python3 scripts/build_site_data.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def strip_quotes(val: str) -> str:
    val = val.strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
        return val[1:-1]
    return val


def parse_directions(text: str) -> list[dict]:
    items: list[dict] = []
    cur: dict | None = None
    cur_list_key: str | None = None
    in_folded = False
    folded_key: str | None = None
    folded_lines: list[str] = []

    def flush_folded() -> None:
        nonlocal in_folded, folded_key, folded_lines
        if cur is not None and folded_key is not None:
            cur[folded_key] = " ".join(line.strip() for line in folded_lines).strip()
        in_folded = False
        folded_key = None
        folded_lines = []

    for line in text.splitlines():
        if line.strip() == "choose:":
            flush_folded()
            break
        if line.startswith("  - id: "):
            flush_folded()
            cur = {"id": line.split(":", 1)[1].strip()}
            items.append(cur)
            cur_list_key = None
            continue
        if cur is None:
            continue
        if in_folded:
            if line.startswith("      ") or not line.strip():
                if line.strip():
                    folded_lines.append(line.strip())
                continue
            flush_folded()
        if line.startswith("      - "):
            if cur_list_key:
                cur.setdefault(cur_list_key, []).append(strip_quotes(line[8:]))
            continue
        m = re.match(r"^    ([a-z_]+):\s*(.*)$", line)
        if m:
            key, rest = m.group(1), m.group(2).strip()
            cur_list_key = None
            if rest == ">":
                in_folded = True
                folded_key = key
                folded_lines = []
            elif rest == "":
                cur_list_key = key
                cur[key] = []
            else:
                cur[key] = strip_quotes(rest)
    flush_folded()
    return items


def parse_anti_patterns(text: str) -> list[dict]:
    items: list[dict] = []
    cur: dict | None = None
    cur_list_key: str | None = None

    for line in text.splitlines():
        if line.startswith("  - id: "):
            cur = {"id": line.split(":", 1)[1].strip(), "signals": []}
            items.append(cur)
            cur_list_key = None
            continue
        if cur is None:
            continue
        if line.startswith("      - "):
            if cur_list_key:
                cur.setdefault(cur_list_key, []).append(strip_quotes(line[8:]))
            continue
        m = re.match(r"^    ([a-z_]+):\s*(.*)$", line)
        if m:
            key, rest = m.group(1), m.group(2).strip()
            cur_list_key = None
            if rest == "":
                cur_list_key = key
                cur[key] = []
            else:
                cur[key] = strip_quotes(rest)
    return items


def parse_reference(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 3)
    matter = text[3:end] if text.startswith("---") and end != -1 else ""
    body = text[end + 4 :] if end != -1 else text

    def fm(key: str) -> str:
        m = re.search(rf"^{key}:\s*(.+)$", matter, re.M)
        return strip_quotes(m.group(1)) if m else ""

    tags = re.findall(r"^\s+-\s+(.+)$", matter, re.M)

    def section_bullets(heading: str) -> list[str]:
        m = re.search(rf"## {re.escape(heading)}\n+(.*?)(?=\n## |\Z)", body, re.S)
        if not m:
            return []
        bullets: list[str] = []
        for ln in m.group(1).strip().splitlines():
            s = ln.strip()
            if s.startswith("- "):
                bullets.append(s[2:].strip())
        return bullets

    def section_para(heading: str) -> str:
        m = re.search(rf"## {re.escape(heading)}\n+(.*?)(?=\n## |\Z)", body, re.S)
        if not m:
            return ""
        paras = [p.strip().replace("\n", " ") for p in m.group(1).strip().split("\n\n") if p.strip()]
        return paras[0] if paras else ""

    return {
        "id": fm("id"),
        "title": fm("title"),
        "url": fm("url"),
        "direction": fm("direction"),
        "job": fm("job"),
        "tags": tags,
        "summary": section_para("Description"),
        "steal": section_bullets("What to steal"),
        "avoid": section_bullets("What not to copy"),
    }


def parse_tokens() -> dict[str, dict]:
    mapping = {
        "quiet-luxury": "quiet-luxury.DESIGN.md",
        "cinematic-dark": "cinematic-dark.DESIGN.md",
        "precise-technical": "precise-technical.DESIGN.md",
        "editorial-print": "editorial-print.DESIGN.md",
    }
    out: dict[str, dict] = {}
    for direction_id, filename in mapping.items():
        text = (ROOT / "tokens" / filename).read_text(encoding="utf-8")
        end = text.find("\n---", 3)
        matter = text[3:end] if text.startswith("---") and end != -1 else ""
        name_m = re.search(r"^name:\s*(.+)$", matter, re.M)
        colors_m = re.search(r"^colors:\n((?:  [a-z-]+:\s*.+\n)+)", matter, re.M)
        colors: dict[str, str] = {}
        if colors_m:
            for ln in colors_m.group(1).strip().splitlines():
                k, v = ln.strip().split(":", 1)
                colors[k.strip()] = strip_quotes(v)
        out[direction_id] = {
            "name": strip_quotes(name_m.group(1)) if name_m else direction_id,
            "file": f"tokens/{filename}",
            "colors": colors,
        }
    return out


def main() -> int:
    directions = parse_directions(
        (ROOT / "taste" / "directions.yaml").read_text(encoding="utf-8")
    )
    anti_patterns = parse_anti_patterns(
        (ROOT / "taste" / "anti-patterns.yaml").read_text(encoding="utf-8")
    )
    principles_text = (ROOT / "taste" / "principles.yaml").read_text(encoding="utf-8")
    principle_count = len(re.findall(r"^\s*- id:\s*", principles_text, re.M))

    index_text = (ROOT / "taste" / "references" / "index.yaml").read_text(encoding="utf-8")
    ref_ids = re.findall(r"^\s+- id:\s*([a-z0-9-]+)\s*$", index_text, re.M)
    references = [
        parse_reference(ROOT / "taste" / "references" / f"{ref_id}.md")
        for ref_id in ref_ids
    ]

    tokens = parse_tokens()

    payload = {
        "counts": {
            "principles": principle_count,
            "antiPatterns": len(anti_patterns),
            "references": len(references),
            "directions": len(directions),
        },
        "directions": directions,
        "references": references,
        "antiPatterns": anti_patterns,
        "tokens": tokens,
    }

    out_path = ROOT / "site" / "data.js"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    header = "// Generated from taste/ and tokens/ by scripts/build_site_data.py.\n"
    out_path.write_text(
        f"{header}window.PREMIUM_TASTE_DATA = {json.dumps(payload, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    print(
        f"wrote {out_path} ({principle_count} principles, {len(anti_patterns)} anti-patterns, "
        f"{len(references)} references, {len(directions)} directions)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
