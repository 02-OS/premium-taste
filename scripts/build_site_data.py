#!/usr/bin/env python3
"""Generate site/data.js directly from taste/ and tokens/ using stdlib only.

Run whenever references, patterns, directions, anti-patterns, or tokens change:

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


def split_frontmatter(text: str) -> tuple[str, str]:
    end = text.find("\n---", 3)
    if text.startswith("---") and end != -1:
        return text[3:end], text[end + 4 :]
    return "", text


def parse_fm_list(matter: str, key: str) -> list[str]:
    m = re.search(rf"^{re.escape(key)}:\s*\n((?:\s+-\s+.+\n?)+)", matter, re.M)
    if not m:
        return []
    return [strip_quotes(ln.strip()[2:]) for ln in m.group(1).splitlines() if ln.strip().startswith("- ")]


def parse_yaml_map(matter: str, key: str) -> dict[str, str]:
    m = re.search(rf"^{re.escape(key)}:\s*\n((?:  [a-z0-9-]+:\s*.+\n?)+)", matter, re.M)
    if not m:
        return {}
    out: dict[str, str] = {}
    for ln in m.group(1).strip().splitlines():
        if ":" in ln:
            k, v = ln.strip().split(":", 1)
            out[k.strip()] = strip_quotes(v)
    return out


def parse_nested_yaml_map(matter: str, key: str) -> dict[str, dict[str, str]]:
    m = re.search(rf"^{re.escape(key)}:\s*\n((?:  .+\n?)+)", matter, re.M)
    if not m:
        return {}
    out: dict[str, dict[str, str]] = {}
    cur_sub: str | None = None
    for ln in m.group(1).splitlines():
        if re.match(r"^  [a-z0-9-]+:\s*$", ln):
            cur_sub = ln.strip()[:-1]
            out[cur_sub] = {}
        elif cur_sub and re.match(r"^    [A-Za-z0-9-]+:\s*.+$", ln):
            k, v = ln.strip().split(":", 1)
            out[cur_sub][k.strip()] = strip_quotes(v)
    return out


def section_body(body: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\n+(.*?)(?=\n## |\Z)", body, re.S | re.M)
    return m.group(1).strip() if m else ""


def section_bullets(body: str, heading: str) -> list[str]:
    sec = section_body(body, heading)
    if not sec:
        return []
    bullets: list[str] = []
    for ln in sec.splitlines():
        s = ln.strip()
        if s.startswith("- "):
            bullets.append(s[2:].strip())
    return bullets


def section_para(body: str, heading: str) -> str:
    sec = section_body(body, heading)
    if not sec:
        return ""
    paras = [p.strip().replace("\n", " ") for p in sec.split("\n\n") if p.strip()]
    return paras[0] if paras else ""


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
    matter, body = split_frontmatter(path.read_text(encoding="utf-8"))

    def fm(key: str) -> str:
        m = re.search(rf"^{key}:\s*(.+)$", matter, re.M)
        return strip_quotes(m.group(1)) if m else ""

    return {
        "id": fm("id"),
        "title": fm("title"),
        "url": fm("url"),
        "direction": fm("direction"),
        "job": fm("job"),
        "tags": parse_fm_list(matter, "tags"),
        "summary": section_para(body, "Description"),
        "steal": section_bullets(body, "What to steal"),
        "avoid": section_bullets(body, "What not to copy"),
    }


def parse_pattern(path: Path) -> dict:
    matter, body = split_frontmatter(path.read_text(encoding="utf-8"))

    def fm(key: str) -> str:
        m = re.search(rf"^{key}:\s*(.+)$", matter, re.M)
        return strip_quotes(m.group(1)) if m else ""

    intro_m = re.search(r"^#\s+.+?\n+(.*?)(?=\n## |\Z)", body.strip(), re.S)
    summary = ""
    if intro_m:
        paras = [p.strip().replace("\n", " ") for p in intro_m.group(1).strip().split("\n\n") if p.strip()]
        summary = paras[0] if paras else ""

    return {
        "id": fm("id"),
        "title": fm("title"),
        "type": fm("type") or "screen",
        "directions": parse_fm_list(matter, "directions"),
        "job": fm("job"),
        "tags": parse_fm_list(matter, "tags"),
        "summary": summary,
        "layout": section_bullets(body, "Layout & Hierarchy"),
        "states": section_bullets(body, "Required States & Mechanics"),
        "include": section_bullets(body, "What to Include"),
        "refuse": section_bullets(body, "What to Refuse"),
        "litmus": section_bullets(body, "Litmus Check"),
    }


def parse_surface_rows(body: str) -> list[dict]:
    sec = section_body(body, "Surfaces")
    rows: list[dict] = []
    for ln in sec.splitlines():
        s = ln.strip()
        if not s.startswith("|") or s.startswith("| Step") or s.startswith("| ---"):
            continue
        cells = [c.strip().strip("`") for c in s.strip("|").split("|")]
        if len(cells) >= 4:
            rows.append(
                {
                    "step": cells[0],
                    "token": cells[1],
                    "hex": cells[2],
                    "purpose": cells[3],
                }
            )
    return rows


def parse_agent_prompts(body: str) -> list[str]:
    sec = section_body(body, "Agent Prompt Guide")
    if not sec:
        return []
    prompts: list[str] = []
    for ln in sec.splitlines():
        m = re.match(r"^\d+\.\s+(.+)$", ln.strip())
        if m:
            prompts.append(m.group(1).strip())
    return prompts


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
        matter, body = split_frontmatter(text)
        name_m = re.search(r"^name:\s*(.+)$", matter, re.M)
        out[direction_id] = {
            "name": strip_quotes(name_m.group(1)) if name_m else direction_id,
            "direction": direction_id,
            "file": f"tokens/{filename}",
            "scale": parse_yaml_map(matter, "scale"),
            "opentype": parse_yaml_map(matter, "opentype"),
            "surfaces": parse_yaml_map(matter, "surfaces"),
            "colors": parse_yaml_map(matter, "colors"),
            "typography": parse_nested_yaml_map(matter, "typography"),
            "rounded": parse_yaml_map(matter, "rounded"),
            "spacing": parse_yaml_map(matter, "spacing"),
            "surfaceRows": parse_surface_rows(body),
            "dosDonts": section_bullets(body, "Do's and Don'ts"),
            "agentPrompts": parse_agent_prompts(body),
        }
    return out


def render_dtcg_tokens(direction_id: str, pack: dict) -> dict:
    """Render a W3C Design Tokens Community Group (DTCG) JSON payload."""
    color_tokens = {
        k: {"$type": "color", "$value": v}
        for k, v in (pack.get("colors") or {}).items()
    }
    surface_tokens = {
        k: {"$type": "color", "$value": v}
        for k, v in (pack.get("surfaces") or {}).items()
    }
    type_tokens: dict[str, dict] = {}
    for role, props in (pack.get("typography") or {}).items():
        type_tokens[role] = {
            "$type": "typography",
            "$value": {
                "fontFamily": props.get("fontFamily", ""),
                "fontSize": props.get("fontSize", "16px"),
                "fontWeight": int(props["fontWeight"]) if str(props.get("fontWeight", "")).isdigit() else 400,
                "lineHeight": float(props["lineHeight"]) if re.match(r"^\d+(\.\d+)?$", str(props.get("lineHeight", ""))) else 1.5,
                "letterSpacing": props.get("letterSpacing", "0em"),
            },
        }
    return {
        "$description": f"Premium Taste starter token pack — {pack.get('name', direction_id)} ({direction_id})",
        "$extensions": {
            "premium-taste": {
                "direction": direction_id,
                "scale": pack.get("scale", {}),
                "opentype": pack.get("opentype", {}),
            }
        },
        "color": color_tokens,
        "surface": surface_tokens,
        "typography": type_tokens,
        "dimension": {
            "spacing": {
                k: {"$type": "dimension", "$value": v}
                for k, v in (pack.get("spacing") or {}).items()
            },
            "radius": {
                k: {"$type": "dimension", "$value": v}
                for k, v in (pack.get("rounded") or {}).items()
            },
        },
    }


def render_design_md(direction_id: str, pack: dict, verbosity: str = "extended") -> str:
    """Return either the full Extended DESIGN.md source or a concise Compact brief."""
    if verbosity == "extended":
        return (ROOT / pack["file"]).read_text(encoding="utf-8")

    colors = pack.get("colors") or {}
    scale = pack.get("scale") or {}
    surfaces = pack.get("surfaces") or {}
    typo = pack.get("typography") or {}
    dos = [d for d in (pack.get("dosDonts") or []) if d.lower().startswith("do ")][:3]
    donts = [d for d in (pack.get("dosDonts") or []) if d.lower().startswith("don't ")][:3]
    prompts = pack.get("agentPrompts") or []

    lines = [
        f"# {pack.get('name', direction_id)} (`{direction_id}`) — Compact DESIGN.md",
        "",
        f"Scale: {scale.get('name', 'custom')} ({scale.get('ratio', '')} from {scale.get('base', '16px')}) · OpenType: `{(pack.get('opentype') or {}).get('numeric', 'tabular-nums')}`",
        "",
        "## Surfaces & Colors",
        *(f"- `{k}`: `{v}`" for k, v in surfaces.items()),
        "- Semantic ink/accent: " + ", ".join(
            f"`{k}={colors[k]}`" for k in ("ink", "ink-muted", "hairline", "line", "accent", "on-accent") if k in colors
        ),
        "",
        "## Type Roles",
        *(
            f"- `{role}`: {p.get('fontFamily', '').split(',')[0]} · {p.get('fontSize')} / {p.get('lineHeight')} · w{p.get('fontWeight')} · ls {p.get('letterSpacing', '0em')}"
            for role, p in typo.items()
        ),
        "",
        "## Guardrails",
        *(f"- {item}" for item in dos),
        *(f"- {item}" for item in donts),
    ]
    if prompts:
        lines.extend(["", "## Starter Component Prompt", f"- {prompts[0]}"])
    return "\n".join(lines) + "\n"


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

    pat_index_text = (ROOT / "taste" / "patterns" / "index.yaml").read_text(encoding="utf-8")
    pat_ids = re.findall(r"^\s+- id:\s*([a-z0-9-]+)\s*$", pat_index_text, re.M)
    patterns = [
        parse_pattern(ROOT / "taste" / "patterns" / f"{pat_id}.md")
        for pat_id in pat_ids
    ]

    tokens = parse_tokens()

    payload = {
        "counts": {
            "principles": principle_count,
            "antiPatterns": len(anti_patterns),
            "references": len(references),
            "patterns": len(patterns),
            "directions": len(directions),
        },
        "directions": directions,
        "references": references,
        "patterns": patterns,
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
        f"{len(references)} references, {len(patterns)} patterns, {len(directions)} directions)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
