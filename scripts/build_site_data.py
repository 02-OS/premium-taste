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


def parse_direction_notes(text: str) -> dict:
    choose: list[str] = []
    register: list[str] = []
    mode: str | None = None
    for line in text.splitlines():
        if line.strip() == "choose:":
            mode = "choose"
            continue
        if line.startswith("register_note:"):
            mode = "register"
            rest = line.split(":", 1)[1].strip()
            register = [] if rest in {">", "|", ""} else [strip_quotes(rest)]
            if rest not in {">", "|", ""}:
                mode = None
            continue
        if mode == "choose" and line.startswith("  - "):
            choose.append(strip_quotes(line[4:].strip()))
            continue
        if mode == "register":
            if not line.strip():
                continue
            if line.startswith("  "):
                register.append(line.strip())
                continue
            mode = None
    return {"choose": choose, "register_note": " ".join(register).strip()}


def parse_simple_yaml(text: str) -> dict:
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if ":" not in line or line.startswith("- "):
            continue
        key, rest = line.split(":", 1)
        key = key.strip()
        rest = rest.strip()
        if rest in {"", ">", "|"}:
            node: dict = {}
            parent[key] = node
            stack.append((indent, node))
        else:
            parent[key] = strip_quotes(rest)
    return root


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


def parse_design_frontmatter(text: str) -> dict:
    end = text.find("\n---", 3)
    matter = text[3:end] if text.startswith("---") and end != -1 else ""
    return parse_simple_yaml(matter)


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
        parsed = parse_design_frontmatter(text)
        colors = parsed.get("colors") if isinstance(parsed.get("colors"), dict) else {}
        typography = parsed.get("typography") if isinstance(parsed.get("typography"), dict) else {}
        rounded = parsed.get("rounded") if isinstance(parsed.get("rounded"), dict) else {}
        spacing = parsed.get("spacing") if isinstance(parsed.get("spacing"), dict) else {}
        imagery = parsed.get("imagery") if isinstance(parsed.get("imagery"), dict) else {}
        surface_rows = [
            {"role": key, "hex": value}
            for key, value in colors.items()
            if str(key).startswith("surface")
        ]
        pack = {
            "name": parsed.get("name") or direction_id,
            "file": f"tokens/{filename}",
            "colors": colors,
            "typography": typography,
            "rounded": rounded,
            "spacing": spacing,
            "surfaceRows": surface_rows,
        }
        if imagery:
            pack["imagery"] = imagery
        out[direction_id] = pack
    return out


def render_dtcg(pack: dict) -> dict:
    color = {
        key: {"$type": "color", "$value": value}
        for key, value in (pack.get("colors") or {}).items()
    }
    typography = {}
    for role, spec in (pack.get("typography") or {}).items():
        if isinstance(spec, dict):
            typography[role] = {"$type": "typography", "$value": dict(spec)}
    return {
        "color": color,
        "typography": typography,
        "spacing": {
            key: {"$type": "dimension", "$value": value}
            for key, value in (pack.get("spacing") or {}).items()
        },
        "radius": {
            key: {"$type": "dimension", "$value": value}
            for key, value in (pack.get("rounded") or {}).items()
        },
    }


def render_design_md(pack: dict) -> str:
    lines = ["---", f"name: {pack.get('name', '')}", "colors:"]
    for key, value in (pack.get("colors") or {}).items():
        lines.append(f"  {key}: \"{value}\"")
    if pack.get("typography"):
        lines.append("typography:")
        for role, spec in pack["typography"].items():
            lines.append(f"  {role}:")
            if isinstance(spec, dict):
                for field, value in spec.items():
                    lines.append(f"    {field}: {value}")
    if pack.get("rounded"):
        lines.append("rounded:")
        for key, value in pack["rounded"].items():
            lines.append(f"  {key}: {value}")
    if pack.get("spacing"):
        lines.append("spacing:")
        for key, value in pack["spacing"].items():
            lines.append(f"  {key}: {value}")
    if pack.get("imagery"):
        lines.append("imagery:")
        for key, value in pack["imagery"].items():
            lines.append(f"  {key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def build_payload() -> dict:
    direction_text = (ROOT / "taste" / "directions.yaml").read_text(encoding="utf-8")
    directions = parse_directions(direction_text)
    notes = parse_direction_notes(direction_text)
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
    return {
        "counts": {
            "principles": principle_count,
            "antiPatterns": len(anti_patterns),
            "references": len(references),
            "directions": len(directions),
        },
        "directions": directions,
        "choose": notes["choose"],
        "registerNote": notes["register_note"],
        "references": references,
        "antiPatterns": anti_patterns,
        "tokens": parse_tokens(),
    }


def render_data_js(payload: dict | None = None) -> str:
    data = payload if payload is not None else build_payload()
    header = "// Generated from taste/ and tokens/ by scripts/build_site_data.py.\n"
    return f"{header}window.PREMIUM_TASTE_DATA = {json.dumps(data, indent=2, ensure_ascii=False)};\n"


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    check = "--check" in argv
    payload = build_payload()
    rendered = render_data_js(payload)
    out_path = ROOT / "site" / "data.js"
    counts = payload["counts"]
    if check:
        current = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
        if current != rendered:
            print("site/data.js is stale. Run python3 scripts/build_site_data.py", file=sys.stderr)
            return 1
        print(
            "site/data.js is fresh "
            f"({counts['principles']} principles, {counts['antiPatterns']} anti-patterns, "
            f"{counts['references']} references, {counts['directions']} directions)"
        )
        return 0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(
        f"wrote {out_path} ({counts['principles']} principles, {counts['antiPatterns']} anti-patterns, "
        f"{counts['references']} references, {counts['directions']} directions)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
