#!/usr/bin/env python3
"""Static UI taste auditor for Premium Taste.

Checks HTML, CSS, JSX, TSX, Vue, and Svelte files against concrete rules in
taste/principles.yaml and taste/anti-patterns.yaml. Zero dependencies beyond
the Python standard library.

Examples:
    python3 scripts/audit.py examples/rowan-before.html
    python3 scripts/audit.py examples/rowan-after.html
    python3 scripts/audit.py src/ --format json
"""

from __future__ import annotations

import argparse
import bisect
import fnmatch
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

SUPPORTED_EXTS = {".html", ".htm", ".css", ".jsx", ".tsx", ".vue", ".svelte", ".astro"}

COSTUME_FONTS = (
    "Inter",
    "Geist",
    "Space Grotesk",
    "Satoshi",
    "Cabinet Grotesk",
    "Clash Display",
    "Plus Jakarta Sans",
    "DM Sans",
    "Instrument Serif",
    "Instrument Sans",
    "Playfair Display",
    "Cormorant Garamond",
)

GENERIC_FONT_TOKENS = {
    "system-ui",
    "-apple-system",
    "blinkmacsystemfont",
    "segoe ui",
    "roboto",
    "helvetica",
    "helvetica neue",
    "arial",
    "sans-serif",
    "serif",
    "monospace",
    "ui-sans-serif",
    "ui-serif",
    "ui-monospace",
    "georgia",
    "palatino",
    "iowan old style",
    "menlo",
    "consolas",
    "sf mono",
    "inherit",
    "initial",
    "unset",
}

ABSTRACT_CLICHES = (
    r"\belevate your\b",
    r"\bunlock\b",
    r"\bseamless(?:ly)?\b",
    r"\bnext[- ]gen(?:eration)?\b",
    r"\bempower(?:ing)?\b",
    r"\bsupercharge\b",
    r"\brevolutionize\b",
    r"\bdelightful experience\b",
    r"\byour workflow\b",
)

COSTUME_FONT_RES = tuple(
    (
        face,
        re.compile(rf"(?<![A-Za-z0-9-]){re.escape(face)}(?![A-Za-z0-9-])", re.I),
    )
    for face in COSTUME_FONTS
)

RULE_RE = re.compile(r"([^{}]+)\{([^}]+)\}", re.S)
HOVER_RE = re.compile(r"([^{}]+:hover[^{]*)\{([^}]+)\}", re.S | re.I)
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}\n]+)", re.I)
COLOR_TOKEN_RE = re.compile(
    r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)|var\(\s*--[A-Za-z0-9_-]+",
    re.I,
)
TAG_RE = re.compile(r"""<(?:"[^"]*"|'[^']*'|[^>"'])*>""", re.S)
COPY_BLOCK_RE = re.compile(
    r"<(script|style|pre|code)\b[^>]*>.*?</\1>",
    re.S | re.I,
)
ACTION_CLASS_RE = re.compile(r"(?:^|[\s_])(?:cta|actions|hero-actions|buttons)(?:$|[\s_])", re.I)

FAKE_PROOF_RE = re.compile(
    r"(?:trusted by\s+\d[\d,+]*|10,000\+\s+\w+|logos?\s*cloud)",
    re.I,
)

SPARKLE_RE = re.compile(r"(?:[✦✨🪄]|<Sparkles\b|sparkle-icon)", re.I)

IGNORE_RE = re.compile(r"taste-ignore:\s*([a-z0-9.,\s-]+)")


@dataclass
class Finding:
    file: str
    line: int
    rule: str
    dimension: str
    severity: str  # "error" | "warn"
    message: str
    fix: str


def line_for_offset(text: str, offset: int, newlines: list[int] | None = None) -> int:
    if offset <= 0:
        return 1
    if newlines is None:
        return text.count("\n", 0, offset) + 1
    return bisect.bisect_left(newlines, offset) + 1


def newline_index(text: str) -> list[int]:
    return [index for index, char in enumerate(text) if char == "\n"]


def ignored_rules_on_line(lines: list[str], line_no: int) -> set[str]:
    ignored: set[str] = set()
    for idx in (line_no - 1, line_no - 2):
        if 0 <= idx < len(lines):
            m = IGNORE_RE.search(lines[idx])
            if m:
                for token in m.group(1).split(","):
                    cleaned = token.strip().rstrip("*/-> ")
                    if cleaned:
                        ignored.add(cleaned)
    return ignored


def hex_to_rgb(hex_color: str) -> tuple[int, int, int] | None:
    h = hex_color.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    elif len(h) == 4:
        h = "".join(c * 2 for c in h[:3])
    elif len(h) == 8:
        h = h[:6]
    if len(h) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        return None
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _channel(token: str) -> int:
    token = token.strip()
    if token.endswith("%"):
        return max(0, min(255, round(float(token[:-1]) * 2.55)))
    return max(0, min(255, round(float(token))))


def hsl_to_rgb(hue: float, sat: float, light: float) -> tuple[int, int, int]:
    chroma = (1 - abs(2 * light - 1)) * sat
    sector = (hue % 360) / 60
    x = chroma * (1 - abs(sector % 2 - 1))
    if sector < 1:
        red, green, blue = chroma, x, 0.0
    elif sector < 2:
        red, green, blue = x, chroma, 0.0
    elif sector < 3:
        red, green, blue = 0.0, chroma, x
    elif sector < 4:
        red, green, blue = 0.0, x, chroma
    elif sector < 5:
        red, green, blue = x, 0.0, chroma
    else:
        red, green, blue = chroma, 0.0, x
    match = light - chroma / 2
    return (
        round((red + match) * 255),
        round((green + match) * 255),
        round((blue + match) * 255),
    )


def parse_color(token: str, root_vars: dict[str, str] | None = None, depth: int = 0) -> tuple[int, int, int] | None:
    token = token.strip().rstrip(";")
    var_match = re.match(r"var\(\s*(--[A-Za-z0-9_-]+)", token, re.I)
    if var_match:
        if depth >= 1 or not root_vars:
            return None
        raw = root_vars.get(var_match.group(1))
        if not raw:
            return None
        return parse_color(raw, root_vars, depth + 1)
    if token.startswith("#"):
        return hex_to_rgb(token)
    rgb_match = re.match(
        r"rgba?\(\s*([0-9.]+%?)\s*[, ]\s*([0-9.]+%?)\s*[, ]\s*([0-9.]+%?)",
        token,
        re.I,
    )
    if rgb_match:
        return (
            _channel(rgb_match.group(1)),
            _channel(rgb_match.group(2)),
            _channel(rgb_match.group(3)),
        )
    hsl_match = re.match(
        r"hsla?\(\s*([0-9.]+)\s*[, ]\s*([0-9.]+)%\s*[, ]\s*([0-9.]+)%",
        token,
        re.I,
    )
    if hsl_match:
        return hsl_to_rgb(
            float(hsl_match.group(1)),
            float(hsl_match.group(2)) / 100,
            float(hsl_match.group(3)) / 100,
        )
    return None


def contrast_rgb(rgb_a: tuple[int, int, int], rgb_b: tuple[int, int, int]) -> float:
    def rel_lum(rgb: tuple[int, int, int]) -> float:
        def adj(v: int) -> float:
            c = v / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        red, green, blue = rgb
        return 0.2126 * adj(red) + 0.7152 * adj(green) + 0.0722 * adj(blue)

    la, lb = rel_lum(rgb_a), rel_lum(rgb_b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def contrast_ratio(hex_a: str, hex_b: str) -> float | None:
    rgb_a = parse_color(hex_a)
    rgb_b = parse_color(hex_b)
    if not rgb_a or not rgb_b:
        return None
    return contrast_rgb(rgb_a, rgb_b)


def mask_keep_newlines(value: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in value)


def strip_non_copy_blocks(html: str) -> str:
    return COPY_BLOCK_RE.sub(lambda match: mask_keep_newlines(match.group(0)), html)


def visible_copy(html: str) -> str:
    masked = strip_non_copy_blocks(html)
    return TAG_RE.sub(lambda match: mask_keep_newlines(match.group(0)), masked)


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", lambda match: mask_keep_newlines(match.group(0)), css, flags=re.S)


def _scan_tag(html: str, start: int) -> tuple[str, str, int] | None:
    if start >= len(html) or html[start] != "<":
        return None
    if html.startswith(("</", "<!", "<?"), start):
        return None
    cursor = start + 1
    if cursor >= len(html) or not (html[cursor].isalpha() or html[cursor] in "_"):
        return None
    name_end = cursor + 1
    while name_end < len(html) and (html[name_end].isalnum() or html[name_end] in "-:"):
        name_end += 1
    tag = html[cursor:name_end].lower()
    quote = ""
    brace = 0
    cursor = name_end
    while cursor < len(html):
        char = html[cursor]
        if quote:
            if char == quote:
                quote = ""
            cursor += 1
            continue
        if char in {"'", '"'}:
            quote = char
            cursor += 1
            continue
        if char == "{":
            brace += 1
        elif char == "}" and brace:
            brace -= 1
        elif char == ">" and brace == 0:
            return tag, html[name_end:cursor], cursor
        cursor += 1
    return None


def iter_open_tags(html: str):
    cursor = 0
    while cursor < len(html):
        start = html.find("<", cursor)
        if start == -1:
            return
        parsed = _scan_tag(html, start)
        if parsed is None:
            cursor = start + 1
            continue
        tag, attrs, end = parsed
        yield tag, attrs, start, end
        cursor = end + 1


def attr_value(attrs: str, names: tuple[str, ...]) -> str | None:
    for name in names:
        match = re.search(rf"(?:^|[\s/>]){re.escape(name)}\s*=\s*(['\"])(.*?)\1", attrs, re.I | re.S)
        if match:
            return match.group(2)
        bare = re.search(rf"(?:^|[\s]){re.escape(name)}\s*=\s*([^\s\"'`=<>]+)", attrs, re.I)
        if bare:
            return bare.group(1)
    return None


def element_span(html: str, open_start: int, open_end: int, tag: str) -> tuple[int, int]:
    """Return the inner range of a balanced element, respecting quotes and nesting."""
    depth = 1
    cursor = open_end + 1
    closer = f"</{tag}"
    while cursor < len(html) and depth:
        next_open = html.find("<", cursor)
        if next_open == -1:
            break
        if html.startswith(closer, next_open) and (
            next_open + len(closer) >= len(html) or not html[next_open + len(closer)].isalnum()
        ):
            depth -= 1
            if depth == 0:
                return open_end + 1, next_open
            cursor = next_open + len(closer)
            continue
        parsed = _scan_tag(html, next_open)
        if parsed and parsed[0] == tag:
            depth += 1
            cursor = parsed[2] + 1
            continue
        cursor = next_open + 1
    return open_end + 1, len(html)


def root_custom_properties(css: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for match in RULE_RE.finditer(css):
        selector = match.group(1)
        if not re.search(r"(?:^|[\s,])\:root\b", selector):
            continue
        for prop in re.finditer(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;]+)", match.group(2)):
            found[prop.group(1)] = prop.group(2).strip()
    return found


def first_color_token(body: str, prop: str) -> str | None:
    match = re.search(rf"(?:^|[;{{])\s*{prop}\s*:\s*([^;}}]+)", body, re.I)
    if not match:
        return None
    token = COLOR_TOKEN_RE.search(match.group(1))
    return token.group(0) if token else None


def extract_css_segments(text: str, ext: str) -> list[tuple[str, int]]:
    if ext == ".css":
        return [(text, 0)]
    segments: list[tuple[str, int]] = []
    for m in re.finditer(r"<style\b[^>]*>(.*?)</style>", text, flags=re.S | re.I):
        segments.append((m.group(1), m.start(1)))
    return segments


def add_finding(
    findings: list[Finding],
    lines: list[str],
    file_label: str,
    line: int,
    rule: str,
    dimension: str,
    severity: str,
    message: str,
    fix: str,
) -> None:
    if rule in ignored_rules_on_line(lines, line):
        return
    findings.append(
        Finding(
            file=file_label,
            line=line,
            rule=rule,
            dimension=dimension,
            severity=severity,
            message=message,
            fix=fix,
        )
    )


def audit_text(text: str, file_label: str, allow_fonts: set[str] | None = None) -> list[Finding]:
    allow = {f.lower() for f in (allow_fonts or set())}
    ext = Path(file_label).suffix.lower() or ".html"
    lines = text.splitlines()
    findings: list[Finding] = []
    newlines = newline_index(text)

    def line_at(offset: int) -> int:
        return line_for_offset(text, offset, newlines)

    css_segments = extract_css_segments(text, ext)

    # 1. type.avoid-tells (font imports, font-family declarations, Tailwind font classes)
    font_contexts: list[tuple[int, str]] = []
    for m in re.finditer(r"fonts\.googleapis\.com/css[^\s\"'>]+", text, re.I):
        font_contexts.append((line_at( m.start()), m.group(0).replace("+", " ")))
    for m in re.finditer(r"font-family\s*:\s*([^;}\n]+)", text, re.I):
        font_contexts.append((line_at( m.start()), m.group(1)))
    for m in re.finditer(r"\bfont-(inter|geist|space-grotesk|dm-sans|plus-jakarta|playfair)\b", text, re.I):
        font_contexts.append((line_at( m.start()), m.group(1).replace("-", " ")))

    seen_tells: set[tuple[str, int]] = set()
    for ln, snippet in font_contexts:
        for face in COSTUME_FONTS:
            if face.lower() in allow:
                continue
            if next(pattern for name, pattern in COSTUME_FONT_RES if name == face).search(snippet):
                key = (face.lower(), ln)
                if key not in seen_tells:
                    seen_tells.add(key)
                    add_finding(
                        findings,
                        lines,
                        file_label,
                        ln,
                        "type.avoid-tells",
                        "uniqueness",
                        "error",
                        f"Costume typeface '{face}' detected.",
                        "Use a system stack or a quieter open face (IBM Plex, Public Sans, Newsreader, Source Serif 4) after fixing the layout.",
                    )

    # 2. type.two-families across CSS font-family declarations
    declared_families: dict[str, tuple[str, int]] = {}
    for seg, base_off in css_segments:
        for m in FONT_FAMILY_RE.finditer(seg):
            first_raw = m.group(1).split(",")[0].strip().strip("\"'")
            if not first_raw or first_raw.startswith("var("):
                continue
            key = first_raw.lower()
            if key in GENERIC_FONT_TOKENS:
                continue
            declared_families.setdefault(key, (first_raw, line_at(base_off + m.start())))
    if len(declared_families) > 2:
        names = [item[0] for item in declared_families.values()]
        first_line = min(item[1] for item in declared_families.values())
        add_finding(
            findings,
            lines,
            file_label,
            first_line,
            "type.two-families",
            "restraint",
            "error",
            f"Found {len(declared_families)} primary font families ({', '.join(names)}). Maximum is 2.",
            "Collapse extra roles into weights or sizes of the two primary families.",
        )

    # 3. color.aurora (gradient clipped text, purple-indigo meshes, glow orbs)
    for seg, base_off in css_segments:
        for m in re.finditer(r"background-clip\s*:\s*text", seg, re.I):
            ln = line_at( base_off + m.start())
            add_finding(
                findings,
                lines,
                file_label,
                ln,
                "color.aurora",
                "restraint",
                "error",
                "Gradient-clipped text headline detected (background-clip: text).",
                "Set the headline in solid ink on a flat surface.",
            )
    for m in re.finditer(r"\bbg-clip-text\b[^\n]*\bbg-gradient-", text):
        ln = line_at( m.start())
        add_finding(
            findings,
            lines,
            file_label,
            ln,
            "color.aurora",
            "restraint",
            "error",
            "Tailwind gradient-clipped text detected (bg-clip-text + bg-gradient-*).",
            "Remove the gradient text and set solid ink.",
        )

    # 4. color.indigo-default
    indigo_hits = list(
        re.finditer(
            r"(?:bg-indigo-[4567]00|text-indigo-[56]00|from-indigo-[456]00|bg-violet-[56]00|#4f46e5|#6366f1|#7c3aed)",
            text,
            re.I,
        )
    )
    if indigo_hits:
        ln = line_at( indigo_hits[0].start())
        add_finding(
            findings,
            lines,
            file_label,
            ln,
            "color.indigo-default",
            "restraint",
            "warn",
            f"Default SaaS indigo/violet accent detected ({indigo_hits[0].group(0)}).",
            "Choose temperature and structure from the screen's direction before picking an accent.",
        )

    # 5. material.glass-on-flat
    for m in re.finditer(r"(?:backdrop-filter\s*:\s*blur|backdrop-blur-)", text, re.I):
        ln = line_at( m.start())
        add_finding(
            findings,
            lines,
            file_label,
            ln,
            "material.glass-on-flat",
            "restraint",
            "warn",
            "Backdrop blur panel detected; ensure it sits over live/photographic content, not a flat surface.",
            "Use a solid surface or raised paper tone instead of decorative blur.",
        )

    # 6. motion.hover & material.gray-card-shadow & motion.reduced & motion.timing
    has_motion = False
    has_reduced_motion = "@media (prefers-reduced-motion" in text or "motion-reduce:" in text
    root_vars: dict[str, str] = {}
    for seg, _base_off in css_segments:
        root_vars.update(root_custom_properties(strip_comments(seg)))
    for seg, base_off in css_segments:
        clean_seg = strip_comments(seg)
        if "@keyframes" in clean_seg or "transition:" in clean_seg or "scroll-behavior:" in clean_seg:
            has_motion = True
        for tm in re.finditer(r"transition\s*:\s*all\b", clean_seg, re.I):
            ln = line_for_offset(text, base_off + tm.start())
            add_finding(
                findings,
                lines,
                file_label,
                ln,
                "motion.timing",
                "restraint",
                "warn",
                "transition: all animates layout properties unnecessarily.",
                "Specify exact transitions (color, border-color, opacity) keeping durations 120–180ms.",
            )
        for m in re.finditer(r"([^{}]+:hover[^{]*)\{([^}]+)\}", clean_seg, re.S | re.I):
            body = m.group(2)
            if re.search(r"transform\s*:\s*(?:translate|scale)", body, re.I) and re.search(r"box-shadow", body, re.I):
                ln = line_at( base_off + m.start())
                add_finding(
                    findings,
                    lines,
                    file_label,
                    ln,
                    "motion.hover",
                    "restraint",
                    "error",
                    "Hover rule combines transform lift/scale with box-shadow.",
                    "Hover should change ink, underline, or hairline only—do not lift cards.",
                )
        for m in re.finditer(r"([^{}]+)\{([^}]+)\}", clean_seg, re.S):
            sel, body = m.group(1), m.group(2)
            if re.search(r"box-shadow\s*:\s*(?!none|inset)[^;]+", body, re.I) and re.search(
                r"border-radius\s*:\s*(?:1[6-9]|[2-9]\d)px", body, re.I
            ):
                ln = line_at( base_off + m.start())
                add_finding(
                    findings,
                    lines,
                    file_label,
                    ln,
                    "material.gray-card-shadow",
                    "restraint",
                    "error",
                    f"In-flow card selector ({sel.strip()}) uses large border-radius with box-shadow.",
                    "Use flat paper, margins, and 1px hairlines; reserve shadow for overlays only.",
                )
            fw_m = re.search(r"font-weight\s*:\s*(100|200)\b", body, re.I)
            if fw_m:
                fs_m = re.search(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", body, re.I)
                is_reading_sel = bool(re.search(r"(?:^|[\s,])(body|p|li|dd|article|main|nav|label|button|a)\b", sel, re.I))
                if is_reading_sel or (fs_m and float(fs_m.group(1)) <= 18):
                    ln = line_at(base_off + m.start())
                    add_finding(
                        findings,
                        lines,
                        file_label,
                        ln,
                        "type.no-hairline-body",
                        "accessibility",
                        "error",
                        f"Hairline font-weight {fw_m.group(1)} applied on '{sel.strip()}' (fails practical legibility below 18px).",
                        "Use weight 400 (or 500 for short UI labels) for readable text and navigation.",
                    )
            if re.search(r"text-transform\s*:\s*uppercase", body, re.I):
                ls_m = re.search(r"letter-spacing\s*:\s*([^;}]+)", body, re.I)
                has_pos_ls = False
                if ls_m:
                    ls_raw = ls_m.group(1).strip()
                    ls_num = re.match(r"([+-]?(?:\d+\.?\d*|\.\d+))\s*(?:px|em|rem)?\b", ls_raw, re.I)
                    if (ls_num and float(ls_num.group(1)) > 0) or ls_raw.startswith("var("):
                        has_pos_ls = True
                if not has_pos_ls:
                    ln = line_at(base_off + m.start())
                    add_finding(
                        findings,
                        lines,
                        file_label,
                        ln,
                        "type.caps-tracking",
                        "restraint",
                        "warn",
                        f"Uppercase transform in '{sel.strip()}' lacks positive letter-spacing.",
                        "Add letter-spacing: 0.05em to 0.08em on a short kicker, or set in sentence case.",
                    )
            fg_token = first_color_token(body, r"(?<![a-z-])color")
            bg_token = first_color_token(body, r"background(?:-color)?")
            if fg_token and bg_token:
                fg_rgb = parse_color(fg_token, root_vars)
                bg_rgb = parse_color(bg_token, root_vars)
                if fg_rgb and bg_rgb:
                    ratio = contrast_rgb(fg_rgb, bg_rgb)
                    if ratio < 4.5:
                        fg_at = body.find(fg_token)
                        bg_at = body.find(bg_token)
                        prop_at = min(index for index in (fg_at, bg_at) if index >= 0)
                        ln = line_at(base_off + m.start(2) + prop_at)
                        add_finding(
                            findings,
                            lines,
                            file_label,
                            ln,
                            "color.contrast",
                            "accessibility",
                            "error",
                            f"Contrast {ratio:.2f}:1 between {fg_token} and {bg_token} in '{sel.strip()}' is under 4.5:1.",
                            "Darken muted ink or raise foreground/background contrast to at least 4.5:1.",
                        )

    for m in re.finditer(r"\btransition-all\b", text):
        ln = line_for_offset(text, m.start())
        add_finding(
            findings,
            lines,
            file_label,
            ln,
            "motion.timing",
            "restraint",
            "warn",
            "Tailwind transition-all utility detected.",
            "Replace with transition-colors or specific property transitions (120–180ms).",
        )

    for m in re.finditer(r"hover:(?:-?translate-y-|scale-)", text):
        ln = line_at( m.start())
        add_finding(
            findings,
            lines,
            file_label,
            ln,
            "motion.hover",
            "restraint",
            "error",
            f"Tailwind hover lift/scale utility '{m.group(0)}' detected.",
            "Replace card lift with a border or ink color change.",
        )

    if has_motion and not has_reduced_motion:
        add_finding(
            findings,
            lines,
            file_label,
            1,
            "motion.reduced",
            "accessibility",
            "warn",
            "Transitions or animations found without a prefers-reduced-motion fallback.",
            "Add @media (prefers-reduced-motion: reduce) to remove transforms and long transitions.",
        )

    # 7. a11y.focus-removed
    has_outline_none = list(
        re.finditer(r"(?:outline\s*:\s*(?:none|0)\b|focus:outline-none)", text, re.I)
    )
    if has_outline_none and ":focus-visible" not in text and "focus-visible:" not in text:
        ln = line_at( has_outline_none[0].start())
        add_finding(
            findings,
            lines,
            file_label,
            ln,
            "a11y.focus-removed",
            "accessibility",
            "error",
            "Focus outline removed without a :focus-visible replacement.",
            "Add a 2px offset :focus-visible outline in ink or accent.",
        )

    # 8. a11y.size (small body font-size in CSS)
    for seg, base_off in css_segments:
        for m in re.finditer(
            r"(?:^|[}\n]\s*)(body|p|li|dd|article|main)\s*\{[^}]*font-size\s*:\s*(\d+(?:\.\d+)?)px",
            seg,
            re.I | re.M,
        ):
            px = float(m.group(2))
            if px < 14:
                ln = line_at( base_off + m.start())
                add_finding(
                    findings,
                    lines,
                    file_label,
                    ln,
                    "a11y.size",
                    "accessibility",
                    "error",
                    f"Reading selector '{m.group(1)}' sets font-size to {px:g}px (below 14px minimum).",
                    "Raise body reading text to at least 14px (16–18px for prose).",
                )

    # 9. HTML/JSX structural, copy & accessibility checks
    if ext in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro"}:
        label_fors: set[str] = set()
        open_tags = list(iter_open_tags(text))
        for tag, attrs, start, _end in open_tags:
            if tag != "label":
                continue
            target = attr_value(attrs, ("for", "htmlFor"))
            if target:
                label_fors.add(target)
        for tag, attrs, start, _end in open_tags:
            if tag not in {"input", "textarea"}:
                continue
            control_type = (attr_value(attrs, ("type",)) or "").lower()
            if control_type in {"hidden", "submit", "button", "reset"}:
                continue
            if attr_value(attrs, ("placeholder",)) is None:
                continue
            has_aria = attr_value(attrs, ("aria-label", "aria-labelledby")) is not None
            control_id = attr_value(attrs, ("id",))
            has_for = bool(control_id and control_id in label_fors)
            prefix = text[max(0, start - 250) : start]
            inside_label = prefix.lower().rfind("<label") > prefix.lower().rfind("</label")
            if not (has_aria or has_for or inside_label):
                add_finding(
                    findings,
                    lines,
                    file_label,
                    line_at(start),
                    "a11y.placeholder-label",
                    "accessibility",
                    "error",
                    "Form control relies on placeholder without a visible <label> or aria-label.",
                    "Add a visible <label for=...> above or beside the field.",
                )

        for tag, attrs, start, end in open_tags:
            if tag != "div":
                continue
            class_name = attr_value(attrs, ("class", "className")) or ""
            if not ACTION_CLASS_RE.search(class_name):
                continue
            inner_start, inner_end = element_span(text, start, end, "div")
            inner = text[inner_start:inner_end]
            filled = []
            for inner_tag, inner_attrs, _inner_start, _inner_end in iter_open_tags(inner):
                if inner_tag not in {"button", "a"}:
                    continue
                cls = attr_value(inner_attrs, ("class", "className")) or ""
                if ("btn" in cls or "button" in cls or "bg-" in cls) and not re.search(
                    r"\b(?:ghost|secondary|outline|quiet|text|link)\b",
                    cls,
                    re.I,
                ):
                    filled.append(cls)
            if len(filled) > 1:
                add_finding(
                    findings,
                    lines,
                    file_label,
                    line_at(start),
                    "chrome.two-primaries",
                    "hierarchy",
                    "error",
                    f"Action group has {len(filled)} primary-styled buttons side by side.",
                    "Keep one filled primary action; demote secondary actions to underlined text or quiet buttons.",
                )

        visible_text = visible_copy(text)
        for pat in ABSTRACT_CLICHES:
            match = re.search(pat, visible_text, re.I)
            if not match:
                continue
            add_finding(
                findings,
                lines,
                file_label,
                line_at(match.start()),
                "content.abstract-verbs",
                "uniqueness",
                "error",
                f"Generic marketing phrasing '{match.group(0).strip()}' could fit any product.",
                "Replace with concrete nouns, materials, prices, or actions specific to this product.",
            )

        fake_m = FAKE_PROOF_RE.search(visible_text)
        if fake_m:
            add_finding(
                findings,
                lines,
                file_label,
                line_at(fake_m.start()),
                "content.fake-proof",
                "uniqueness",
                "error",
                f"Unsourced social proof pattern '{fake_m.group(0)}' detected.",
                "Remove invented counts or logo clouds; use one verifiable fact or nothing.",
            )

        spark_m = SPARKLE_RE.search(strip_non_copy_blocks(text))
        if spark_m:
            add_finding(
                findings,
                lines,
                file_label,
                line_at(spark_m.start()),
                "chrome.sparkle",
                "uniqueness",
                "error",
                f"Sparkle motif '{spark_m.group(0)}' used as UI decoration.",
                "Remove sparkle/wand icons; depict the product's real object or state.",
            )

        # a11y.semantics (clickable div/span without role, zoom-blocking viewport meta)
        copy_html = strip_non_copy_blocks(text)
        for m in re.finditer(r"<(div|span)\b([^>]*\bon(?:click|Click)\s*=[^>]*)>", copy_html, re.S):
            attrs = m.group(2)
            if not re.search(r'\brole=["\']?(?:button|link|menuitem|tab)', attrs, re.I):
                pos = text.find(m.group(0))
                ln = line_for_offset(text, pos if pos != -1 else 0)
                add_finding(
                    findings,
                    lines,
                    file_label,
                    ln,
                    "a11y.semantics",
                    "accessibility",
                    "error",
                    f"Clickable <{m.group(1)}> lacks native button/link semantics.",
                    "Replace with <button type=\"button\"> or <a href=\"...\"> for keyboard and screen-reader support.",
                )

        vp_m = re.search(r'<meta\b[^>]*name=["\']viewport["\'][^>]*content=["\']([^"\']+)["\']', text, re.I)
        if vp_m and re.search(r"(?:user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0+)?\b)", vp_m.group(1), re.I):
            ln = line_for_offset(text, vp_m.start())
            add_finding(
                findings,
                lines,
                file_label,
                ln,
                "a11y.semantics",
                "accessibility",
                "error",
                "Viewport meta disables pinch zoom (user-scalable=no or maximum-scale=1).",
                "Allow zooming with content=\"width=device-width, initial-scale=1.0\".",
            )

        # type.tabular-numbers on standalone tables (skip when styles live in external CSS checked elsewhere)
        tbl_m = re.search(r"<table\b", copy_html, re.I)
        uses_external_css = bool(
            re.search(r'<link\b[^>]+rel=["\']stylesheet["\']', text, re.I)
            or re.search(r'import\s+["\'][^"\']+\.css', text)
        )
        if tbl_m and not uses_external_css and "tabular-nums" not in text:
            pos = text.find(tbl_m.group(0))
            ln = line_for_offset(text, pos if pos != -1 else 0)
            add_finding(
                findings,
                lines,
                file_label,
                ln,
                "type.numbers",
                "hierarchy",
                "warn",
                "Data table present without font-variant-numeric: tabular-nums or Tailwind tabular-nums.",
                "Set font-variant-numeric: tabular-nums on numeric/table columns so figures stay aligned.",
            )

        # type.caps-tracking on Tailwind uppercase class tokens
        for cm in re.finditer(r'class(?:Name)?=["\']([^"\']*\buppercase\b[^"\']*)["\']', copy_html):
            if not re.search(r"\btracking-(?:wide|wider|widest)\b", cm.group(1)):
                pos = text.find(cm.group(0))
                ln = line_for_offset(text, pos if pos != -1 else 0)
                add_finding(
                    findings,
                    lines,
                    file_label,
                    ln,
                    "type.caps-tracking",
                    "restraint",
                    "warn",
                    "Tailwind 'uppercase' utility used without positive tracking-* spacing.",
                    "Pair uppercase with tracking-wider on one short kicker or remove uppercase.",
                )

    return findings


def score_dimensions(findings: list[Finding]) -> dict[str, int]:
    dims = {
        "hierarchy": 5,
        "spacing": 5,
        "uniqueness": 5,
        "restraint": 5,
        "accessibility": 5,
        "product_fit": 5,
    }
    for f in findings:
        d = f.dimension if f.dimension in dims else "restraint"
        penalty = 2 if f.severity == "error" else 1
        dims[d] = max(1, dims[d] - penalty)
    return dims


def path_excluded(path: Path, patterns: list[str]) -> bool:
    rendered = path.as_posix()
    for pattern in patterns:
        if (
            fnmatch.fnmatch(rendered, pattern)
            or fnmatch.fnmatch(path.name, pattern)
            or fnmatch.fnmatch(str(path), pattern)
        ):
            return True
    return False


def collect_targets(paths: list[Path], exclude: list[str] | None = None) -> list[Path]:
    patterns = exclude or []
    files: list[Path] = []
    for p in paths:
        if p.is_file():
            if not path_excluded(p, patterns):
                files.append(p)
        elif p.is_dir():
            for child in sorted(p.rglob("*")):
                if child.is_file() and child.suffix.lower() in SUPPORTED_EXTS:
                    if any(part in {"node_modules", ".git", ".next", "dist", "build"} for part in child.parts):
                        continue
                    if path_excluded(child, patterns):
                        continue
                    files.append(child)
    return files


def format_text(findings: list[Finding], file_count: int) -> str:
    scores = score_dimensions(findings)
    lines = [
        f"Premium Taste Audit ({file_count} file(s), {len(findings)} finding(s))",
        "",
        "Static Scores (automated check):",
        f"  - Hierarchy:     {scores['hierarchy']}/5",
        f"  - Spacing:       {scores['spacing']}/5 (verify visual measure & section jumps manually)",
        f"  - Uniqueness:    {scores['uniqueness']}/5",
        f"  - Restraint:     {scores['restraint']}/5",
        f"  - Accessibility: {scores['accessibility']}/5",
        f"  - Product fit:   {scores['product_fit']}/5 (verify direction-serves-job manually)",
    ]
    if not findings:
        lines.extend(["", "PASS: No automated rule violations found."])
        return "\n".join(lines)

    lines.extend(["", "Findings:"])
    for idx, f in enumerate(findings, 1):
        lines.append(f"  {idx}. [{f.severity.upper()}] {f.file}:{f.line} — {f.rule}")
        lines.append(f"     Now: {f.message}")
        lines.append(f"     Fix: {f.fix}")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit HTML/CSS/JSX/TSX files against Premium Taste rules."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="File(s) or directory(ies) to audit.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--allow-font",
        action="append",
        default=[],
        help="Font name already owned by the product's brand guide (repeatable).",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Glob of files to skip (repeatable). Matched against the path and the file name.",
    )
    parser.add_argument(
        "--ignore-rule",
        action="append",
        default=[],
        help="Rule id to drop from the report (repeatable).",
    )
    parser.add_argument(
        "--fail-on",
        choices=("error", "warn"),
        default="warn",
        help="Minimum severity that produces a non-zero exit (default: warn).",
    )
    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="Always exit 0 even when violations are found.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    targets = collect_targets(args.paths, args.exclude)
    if not targets:
        print("No supported UI files found in given path(s).", file=sys.stderr)
        return 2

    ignored = {rule.strip() for rule in args.ignore_rule if rule.strip()}
    all_findings: list[Finding] = []
    allow = set(args.allow_font)
    for path in targets:
        text = path.read_text(encoding="utf-8", errors="replace")
        for finding in audit_text(text, str(path), allow_fonts=allow):
            if finding.rule not in ignored:
                all_findings.append(finding)

    passed = len(all_findings) == 0
    if args.format == "json":
        payload = {
            "files": [str(t) for t in targets],
            "scores": score_dimensions(all_findings),
            "passed": passed,
            "findings": [asdict(f) for f in all_findings],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(format_text(all_findings, len(targets)))

    if args.warn_only or passed:
        return 0
    if args.fail_on == "error":
        return 1 if any(finding.severity == "error" for finding in all_findings) else 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
