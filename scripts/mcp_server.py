#!/usr/bin/env python3
"""Minimal zero-dependency MCP server for Premium Taste over stdio (JSON-RPC 2.0).

Supports both newline-delimited JSON messages (MCP 2024-11-05+) and HTTP-style
Content-Length framing, replying in whichever framing mode the caller sends.

Tools exposed:
  - pick_direction: Choose 1 direction + best-fit references/patterns + tokens + decision ledger template
  - get_reference: Fetch full 'what to steal' and 'what not to copy' for a reference
  - get_pattern: Fetch screen or flow architecture contracts (hierarchy, states, refuse, litmus check)
  - get_tokens: Export starter tokens as CSS vars, Tailwind v4 @theme, JSON, W3C DTCG JSON, or DESIGN.md
  - audit_ui: Run the deterministic Premium Taste static auditor on code or a file path
  - verify_url: Inspect a live or localhost URL via headless Chromium CDP (or HTTP fallback)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import audit  # noqa: E402
import build_site_data as catalog  # noqa: E402
import critique_url  # noqa: E402


DIRECTION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "precise-technical": (
        "doc", "docs", "documentation", "api", "sdk", "cli", "developer", "tool",
        "dashboard", "metric", "latency", "deploy", "log", "admin", "pricing",
        "table", "workspace", "code", "diff", "schema", "saas", "config", "data",
    ),
    "quiet-luxury": (
        "store", "shop", "product", "brand", "ceramic", "object", "fashion",
        "furniture", "home", "commerce", "cart", "collection", "studio", "craft",
        "gallery", "minimal", "booking", "spa", "hotel",
    ),
    "cinematic-dark": (
        "film", "cinema", "music", "audio", "album", "video", "game", "festival",
        "portfolio", "photo", "trailer", "screening", "exhibit", "stage", "sound",
    ),
    "editorial-print": (
        "article", "essay", "magazine", "news", "newsletter", "journal", "dispatch",
        "blog", "letter", "publication", "longform", "reading", "report", "briefing",
    ),
}


def load_catalog() -> dict:
    directions = catalog.parse_directions(
        (ROOT / "taste" / "directions.yaml").read_text(encoding="utf-8")
    )
    index_text = (ROOT / "taste" / "references" / "index.yaml").read_text(encoding="utf-8")
    ref_ids = re.findall(r"^\s+- id:\s*([a-z0-9-]+)\s*$", index_text, re.M)
    references = [
        catalog.parse_reference(ROOT / "taste" / "references" / f"{ref_id}.md")
        for ref_id in ref_ids
    ]
    pat_index_text = (ROOT / "taste" / "patterns" / "index.yaml").read_text(encoding="utf-8")
    pat_ids = re.findall(r"^\s+- id:\s*([a-z0-9-]+)\s*$", pat_index_text, re.M)
    patterns = [
        catalog.parse_pattern(ROOT / "taste" / "patterns" / f"{pat_id}.md")
        for pat_id in pat_ids
    ]
    tokens = catalog.parse_tokens()
    return {
        "directions": directions,
        "references": references,
        "patterns": patterns,
        "tokens": tokens,
    }


def _as_text(val: object) -> str:
    if isinstance(val, list):
        return " ".join(str(x) for x in val)
    return str(val or "")


def _query_filter(items: list[dict], query: str, fields: tuple[str, ...]) -> list[dict]:
    """Filter by exact substring first, falling back to multi-word overlap ranking."""
    q = query.strip().lower()
    if not q:
        return items
    exact = [
        item
        for item in items
        if any(q in _as_text(item.get(f)).lower() for f in fields)
    ]
    if exact:
        return exact
    words = [w for w in re.findall(r"[a-z0-9-]+", q) if len(w) > 2]
    if not words:
        return []
    scored: list[tuple[int, dict]] = []
    for item in items:
        haystack = " ".join(_as_text(item.get(f)).lower() for f in fields)
        score = sum(1 for w in words if w in haystack)
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in scored]


def score_direction(job: str, direction: dict) -> int:
    text = job.lower()
    words = set(re.findall(r"[a-z0-9-]+", text))
    score = 0
    for kw in DIRECTION_KEYWORDS.get(direction["id"], ()):
        if kw in words or kw in text:
            score += 3
    for token in re.findall(r"[a-z0-9-]+", _as_text(direction.get("jobs")).lower()):
        if len(token) > 3 and token in words:
            score += 2
    return score


def tool_pick_direction(args: dict, data: dict) -> str:
    job = str(args.get("job", "")).strip()
    if not job:
        raise ValueError("'job' (one sentence describing what the user comes to do) is required.")

    explicit_dir = str(args.get("direction", "")).strip()
    directions = data["directions"]
    if explicit_dir:
        chosen = next((d for d in directions if d["id"] == explicit_dir), None)
        if not chosen:
            valid = ", ".join(d["id"] for d in directions)
            raise ValueError(f"Unknown direction '{explicit_dir}'. Choose one of: {valid}")
    else:
        ranked = sorted(directions, key=lambda d: score_direction(job, d), reverse=True)
        chosen = ranked[0] if score_direction(job, ranked[0]) > 0 else next(
            d for d in directions if d["id"] == "precise-technical"
        )

    dir_refs = [r for r in data["references"] if r["direction"] == chosen["id"]]
    job_words = set(re.findall(r"[a-z0-9-]+", job.lower()))
    dir_refs.sort(
        key=lambda r: sum(
            2
            for w in job_words
            if len(w) > 3
            and (w in _as_text(r.get("job")).lower() or w in _as_text(r.get("tags")).lower())
        ),
        reverse=True,
    )

    token_pack = data["tokens"].get(chosen["id"], {})
    dir_patterns = [p for p in data.get("patterns", []) if chosen["id"] in p.get("directions", [])]
    other_patterns = [p for p in data.get("patterns", []) if chosen["id"] not in p.get("directions", [])]

    def pat_score(pat: dict, boost: int) -> int:
        hay = " ".join([pat.get("title", ""), pat.get("job", ""), _as_text(pat.get("tags"))]).lower()
        return boost + sum(3 for w in job_words if len(w) > 3 and w in hay)

    ranked_patterns = sorted(
        [(pat_score(p, 2), p) for p in dir_patterns] + [(pat_score(p, 0), p) for p in other_patterns],
        key=lambda pair: pair[0],
        reverse=True,
    )
    top_patterns = [p for _, p in ranked_patterns[:2]]
    top_ref = dir_refs[0]["id"] if dir_refs else "none"
    top_pat = top_patterns[0]["id"] if top_patterns else "none"

    result = {
        "job": job,
        "recommended_direction": chosen["id"],
        "summary": chosen.get("summary"),
        "temperature": chosen.get("temperature"),
        "density": chosen.get("density"),
        "type": chosen.get("type"),
        "material": chosen.get("material"),
        "first_screen": chosen.get("first_screen"),
        "refuses": chosen.get("refuses", []),
        "matching_references": [
            {
                "id": r["id"],
                "title": r["title"],
                "job": r["job"],
                "steal": r["steal"][:3],
                "avoid": r["avoid"][:2],
            }
            for r in dir_refs[:3]
        ],
        "matching_patterns": [
            {
                "id": p["id"],
                "title": p["title"],
                "type": p["type"],
                "job": p["job"],
                "layout": p["layout"][:2],
                "litmus": p["litmus"][:1],
            }
            for p in top_patterns
        ],
        "decision_ledger_template": {
            "screen_job": job,
            "direction": chosen["id"],
            "reference": top_ref,
            "pattern": top_pat,
            "one_rule_at_risk": "Name 1 rule or anti-pattern most likely to break if rushed (e.g. type.numbers or chrome.one-primary).",
            "visual_target_gate": {
                "rendered_at_target_widths": "1280px and 375px",
                "first_screen_answer": chosen.get("first_screen"),
                "anti_averaging_check": "Preserves sharp polarity (temperature, weight discipline, no dark+warm-paper blend).",
            },
        },
        "tokens": token_pack,
    }
    return json.dumps(result, indent=2)


def tool_get_reference(args: dict, data: dict) -> str:
    ref_id = str(args.get("id", "")).strip().lower()
    direction = str(args.get("direction", "")).strip().lower()
    query = str(args.get("query", "")).strip().lower()
    refs = data["references"]

    if ref_id:
        match = next((r for r in refs if r["id"] == ref_id), None)
        if not match:
            raise ValueError(f"Reference '{ref_id}' not found. Available: {', '.join(r['id'] for r in refs)}")
        raw_md = (ROOT / "taste" / "references" / f"{ref_id}.md").read_text(encoding="utf-8")
        return json.dumps({"reference": match, "markdown": raw_md}, indent=2)

    filtered = refs
    if direction:
        filtered = [r for r in filtered if r["direction"] == direction]
    if query:
        filtered = _query_filter(filtered, query, ("id", "title", "job", "summary", "tags"))
    return json.dumps({"count": len(filtered), "references": filtered}, indent=2)


def tool_get_pattern(args: dict, data: dict) -> str:
    pat_id = str(args.get("id", "")).strip().lower()
    pat_type = str(args.get("type", "")).strip().lower()
    direction = str(args.get("direction", "")).strip().lower()
    query = str(args.get("query", "")).strip().lower()
    patterns = data.get("patterns", [])

    if pat_id:
        match = next((p for p in patterns if p["id"] == pat_id), None)
        if not match:
            raise ValueError(f"Pattern '{pat_id}' not found. Available: {', '.join(p['id'] for p in patterns)}")
        raw_md = (ROOT / "taste" / "patterns" / f"{pat_id}.md").read_text(encoding="utf-8")
        return json.dumps({"pattern": match, "markdown": raw_md}, indent=2)

    filtered = patterns
    if pat_type:
        filtered = [p for p in filtered if p.get("type", "").lower() == pat_type]
    if direction:
        filtered = [p for p in filtered if direction in p.get("directions", [])]
    if query:
        filtered = _query_filter(filtered, query, ("id", "title", "job", "summary", "tags"))
    return json.dumps({"count": len(filtered), "patterns": filtered}, indent=2)


def tool_get_tokens(args: dict, data: dict) -> str:
    direction = str(args.get("direction", "")).strip().lower()
    fmt = str(args.get("format", "css")).strip().lower()
    verbosity = str(args.get("verbosity", "extended")).strip().lower()
    if verbosity not in ("compact", "extended"):
        raise ValueError("Unknown verbosity; choose 'compact' or 'extended'.")
    pack = data["tokens"].get(direction)
    if not pack:
        valid = ", ".join(data["tokens"].keys())
        raise ValueError(f"Unknown direction '{direction}'. Choose one of: {valid}")

    colors = pack.get("colors", {})
    if fmt == "design_md":
        return catalog.render_design_md(direction, pack, verbosity=verbosity)
    if fmt == "dtcg":
        return json.dumps(catalog.render_dtcg_tokens(direction, pack), indent=2)
    if fmt == "json":
        return json.dumps(pack, indent=2)
    if fmt == "tailwind":
        lines = [f"/* Premium Taste — {pack['name']} ({direction}) */", "@theme {"]
        for k, v in colors.items():
            lines.append(f"  --color-pt-{k}: {v};")
        for k, v in (pack.get("surfaces") or {}).items():
            lines.append(f"  --color-pt-{k}: {v};")
        lines.append("}")
        return "\n".join(lines)

    lines = [f"/* Premium Taste — {pack['name']} ({direction}) */", ":root {"]
    for k, v in colors.items():
        lines.append(f"  --pt-{k}: {v};")
    for k, v in (pack.get("surfaces") or {}).items():
        lines.append(f"  --pt-{k}: {v};")
    lines.append("}")
    return "\n".join(lines)


def tool_audit_ui(args: dict, _data: dict) -> str:
    code = args.get("code")
    file_path = args.get("file_path")
    allow_fonts = {str(f).strip().lower() for f in (args.get("allow_fonts") or []) if str(f).strip()}

    if code is not None and str(code).strip():
        label = str(file_path or "snippet.html")
        findings = audit.audit_text(str(code), label, allow_fonts=allow_fonts)
        count = 1
    elif file_path:
        target = Path(str(file_path))
        if not target.is_absolute():
            target = (Path.cwd() / target).resolve()
        if not target.exists():
            raise ValueError(f"File not found: {target}")
        if target.is_dir():
            files = audit.collect_targets([target])
            findings = []
            for f in files:
                findings.extend(audit.audit_text(f.read_text(encoding="utf-8", errors="replace"), str(f), allow_fonts=allow_fonts))
            count = len(files)
        else:
            findings = audit.audit_text(target.read_text(encoding="utf-8", errors="replace"), str(target), allow_fonts=allow_fonts)
            count = 1
    else:
        raise ValueError("Provide either 'code' or 'file_path' to audit_ui.")

    payload = {
        "files_checked": count,
        "passed": not any(f.severity == "error" for f in findings),
        "scores": audit.score_dimensions(findings),
        "findings": [f.__dict__ for f in findings],
        "report": audit.format_text(findings, count),
    }
    return json.dumps(payload, indent=2)


def tool_verify_url(args: dict, _data: dict) -> str:
    url = str(args.get("url", "")).strip()
    if not url:
        raise ValueError("'url' is required (http://, https://, or file://).")
    allow_fonts = {str(f).strip().lower() for f in (args.get("allow_fonts") or []) if str(f).strip()}
    no_browser = bool(args.get("no_browser", False))
    desktop_w = int(args.get("desktop_width", 1280))
    mobile_w = int(args.get("mobile_width", 375))
    screenshot_dir = args.get("screenshot_dir")

    result = critique_url.run_url_critique(
        url,
        desktop_width=desktop_w,
        mobile_width=mobile_w,
        allow_fonts=allow_fonts,
        no_browser=no_browser,
        screenshot_dir=str(screenshot_dir) if screenshot_dir else None,
    )
    result.pop("_finding_objects", None)
    return json.dumps(result, indent=2)


TOOLS = [
    {
        "name": "pick_direction",
        "description": "Choose the single best Premium Taste direction, fitting references, matching screen/flow patterns, decision ledger template, and token palette for a screen job.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "job": {"type": "string", "description": "One sentence naming what the user comes to this screen to do."},
                "direction": {
                    "type": "string",
                    "enum": ["quiet-luxury", "cinematic-dark", "precise-technical", "editorial-print"],
                    "description": "Optional explicit direction override.",
                },
            },
            "required": ["job"],
        },
    },
    {
        "name": "get_reference",
        "description": "Inspect one or more real reference products with 'What to steal' and 'What not to copy'.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Reference ID (e.g. stripe-docs, aesop, are-na, mubi)."},
                "direction": {"type": "string", "enum": ["quiet-luxury", "cinematic-dark", "precise-technical", "editorial-print"]},
                "query": {"type": "string", "description": "Search keywords across job, summary, title, and tags."},
            },
        },
    },
    {
        "name": "get_pattern",
        "description": "Fetch reusable screen or flow architecture contracts (layout hierarchy, required states, what to include/refuse, litmus check).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Pattern ID (e.g. pricing-table, empty-state, onboarding-checklist, billing-cancellation)."},
                "type": {"type": "string", "enum": ["screen", "flow"]},
                "direction": {"type": "string", "enum": ["quiet-luxury", "cinematic-dark", "precise-technical", "editorial-print"]},
                "query": {"type": "string", "description": "Search keywords across pattern title, job, summary, and tags."},
            },
        },
    },
    {
        "name": "get_tokens",
        "description": "Get starter visual tokens for a direction as CSS variables, Tailwind v4 @theme, JSON, W3C DTCG JSON, or Compact/Extended DESIGN.md.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "direction": {"type": "string", "enum": ["quiet-luxury", "cinematic-dark", "precise-technical", "editorial-print"]},
                "format": {"type": "string", "enum": ["css", "tailwind", "json", "dtcg", "design_md"], "default": "css"},
                "verbosity": {"type": "string", "enum": ["compact", "extended"], "default": "extended", "description": "Applies to design_md: concise 30-line brief or full 14-section spec."},
            },
            "required": ["direction"],
        },
    },
    {
        "name": "audit_ui",
        "description": "Run the deterministic Premium Taste UI auditor against HTML/CSS/JSX code or a project file path.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Raw HTML/CSS/JSX/TSX code to check."},
                "file_path": {"type": "string", "description": "File or directory path to audit (optional if code is passed)."},
                "allow_fonts": {"type": "array", "items": {"type": "string"}, "description": "Explicitly exempted typeface names."},
            },
        },
    },
    {
        "name": "verify_url",
        "description": "Run live runtime DOM/CSS checks (computed contrast, fonts, weights, horizontal overflow, tabular-nums tables, unsized images, optional screenshots) on a rendered URL.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target HTTP(S) or file:// URL to critique."},
                "no_browser": {"type": "boolean", "default": False, "description": "Force HTTP static fallback instead of headless Chromium."},
                "desktop_width": {"type": "integer", "default": 1280},
                "mobile_width": {"type": "integer", "default": 375},
                "allow_fonts": {"type": "array", "items": {"type": "string"}},
                "screenshot_dir": {"type": "string", "description": "Optional directory path to save desktop.png and mobile.png."},
            },
            "required": ["url"],
        },
    },
]

TOOL_HANDLERS = {
    "pick_direction": tool_pick_direction,
    "get_reference": tool_get_reference,
    "get_pattern": tool_get_pattern,
    "get_tokens": tool_get_tokens,
    "audit_ui": tool_audit_ui,
    "verify_url": tool_verify_url,
}


def read_message(stdin_buf) -> tuple[dict | None, str]:
    """Read one JSON-RPC message using either Content-Length or newline framing."""
    while True:
        line = stdin_buf.readline()
        if not line:
            return None, "line"
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower().startswith(b"content-length:"):
            length = int(stripped.split(b":", 1)[1].strip())
            while True:
                hdr = stdin_buf.readline()
                if not hdr or hdr in (b"\r\n", b"\n"):
                    break
            body = stdin_buf.read(length)
            if not body:
                return None, "lsp"
            return json.loads(body.decode("utf-8")), "lsp"
        return json.loads(stripped.decode("utf-8")), "line"


def write_message(stdout_buf, payload: dict, framing: str) -> None:
    encoded = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    if framing == "lsp":
        header = f"Content-Length: {len(encoded)}\r\n\r\n".encode("ascii")
        stdout_buf.write(header + encoded)
    else:
        stdout_buf.write(encoded + b"\n")
    stdout_buf.flush()


def handle_request(msg: dict, data: dict) -> dict | None:
    method = msg.get("method", "")
    req_id = msg.get("id")
    params = msg.get("params") or {}

    if method.startswith("notifications/") or req_id is None:
        return None

    if method == "initialize":
        client_proto = params.get("protocolVersion") or "2024-11-05"
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": client_proto,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "premium-taste", "version": "1.0.0"},
            },
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        name = params.get("name", "")
        handler = TOOL_HANDLERS.get(name)
        if not handler:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Unknown tool: {name}"},
            }
        try:
            text = handler(params.get("arguments") or {}, data)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": text}], "isError": False},
            }
        except Exception as exc:  # noqa: BLE001
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": f"Error: {exc}"}], "isError": True},
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> int:
    data = load_catalog()
    stdin_buf = sys.stdin.buffer
    stdout_buf = sys.stdout.buffer
    while True:
        try:
            msg, framing = read_message(stdin_buf)
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write(f"premium-taste MCP parse error: {exc}\n")
            return 1
        if msg is None:
            return 0
        resp = handle_request(msg, data)
        if resp is not None:
            write_message(stdout_buf, resp, framing)


if __name__ == "__main__":
    raise SystemExit(main())
