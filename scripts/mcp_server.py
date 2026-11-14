#!/usr/bin/env python3
"""Minimal zero-dependency MCP server for Premium Taste over stdio (JSON-RPC 2.0).

Supports both newline-delimited JSON messages (MCP 2024-11-05+) and HTTP-style
Content-Length framing, replying in whichever framing mode the caller sends.

Tools exposed:
  - pick_direction: Choose 1 direction + best-fit reference + tokens for a screen job
  - get_reference: Fetch full 'what to steal' and 'what not to copy' for a reference
  - get_tokens: Export starter palette tokens as CSS vars, Tailwind v4 @theme, JSON, or DESIGN.md
  - audit_ui: Run the deterministic Premium Taste static auditor on code or a file path
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
    tokens = catalog.parse_tokens()
    return {"directions": directions, "references": references, "tokens": tokens}


def _as_text(val: object) -> str:
    if isinstance(val, list):
        return " ".join(str(x) for x in val)
    return str(val or "")


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
        filtered = [
            r
            for r in filtered
            if query in r["title"].lower()
            or query in r["job"].lower()
            or query in r["summary"].lower()
            or any(query in t.lower() for t in r["tags"])
        ]
    return json.dumps({"count": len(filtered), "references": filtered}, indent=2)


def tool_get_tokens(args: dict, data: dict) -> str:
    direction = str(args.get("direction", "")).strip().lower()
    fmt = str(args.get("format", "css")).strip().lower()
    pack = data["tokens"].get(direction)
    if not pack:
        valid = ", ".join(data["tokens"].keys())
        raise ValueError(f"Unknown direction '{direction}'. Choose one of: {valid}")

    colors = pack.get("colors", {})
    if fmt == "design_md":
        return (ROOT / pack["file"]).read_text(encoding="utf-8")
    if fmt == "json":
        return json.dumps(pack, indent=2)
    if fmt == "tailwind":
        lines = [f"/* Premium Taste — {pack['name']} ({direction}) */", "@theme {"]
        for k, v in colors.items():
            lines.append(f"  --color-pt-{k}: {v};")
        lines.append("}")
        return "\n".join(lines)

    lines = [f"/* Premium Taste — {pack['name']} ({direction}) */", ":root {"]
    for k, v in colors.items():
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


TOOLS = [
    {
        "name": "pick_direction",
        "description": "Choose the single best Premium Taste direction, fitting reference, first-screen rule, and token palette for a screen job.",
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
                "query": {"type": "string", "description": "Search keyword across job, summary, and tags."},
            },
        },
    },
    {
        "name": "get_tokens",
        "description": "Get starter visual tokens for a direction as CSS variables, Tailwind v4 @theme, JSON, or DESIGN.md.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "direction": {"type": "string", "enum": ["quiet-luxury", "cinematic-dark", "precise-technical", "editorial-print"]},
                "format": {"type": "string", "enum": ["css", "tailwind", "json", "design_md"], "default": "css"},
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
]

TOOL_HANDLERS = {
    "pick_direction": tool_pick_direction,
    "get_reference": tool_get_reference,
    "get_tokens": tool_get_tokens,
    "audit_ui": tool_audit_ui,
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
