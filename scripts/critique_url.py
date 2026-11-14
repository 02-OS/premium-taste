#!/usr/bin/env python3
"""Critique a live URL or localhost page against Premium Taste rules using Chromium CDP or HTTP fallback."""

from __future__ import annotations

import argparse
import base64
import glob
import hashlib
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit  # noqa: E402


EVAL_DOM_JS = r"""
(() => {
  const parseRgba = (str) => {
    if (!str) return null;
    const m = str.match(/rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?\s*\)/i);
    if (!m) return null;
    return [Number(m[1]), Number(m[2]), Number(m[3]), m[4] === undefined ? 1 : Number(m[4])];
  };

  const blend = (fg, bg) => {
    const a = fg[3];
    if (a >= 0.999) return [fg[0], fg[1], fg[2], 1];
    return [
      fg[0] * a + bg[0] * (1 - a),
      fg[1] * a + bg[1] * (1 - a),
      fg[2] * a + bg[2] * (1 - a),
      1,
    ];
  };

  const lum = ([r, g, b]) => {
    const c = [r, g, b].map((v) => {
      const s = v / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  };

  const ratio = (c1, c2) => {
    const l1 = lum(c1);
    const l2 = lum(c2);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  };

  const getEffectiveBg = (el) => {
    const chain = [];
    let cur = el;
    while (cur && cur.nodeType === 1) {
      chain.push(cur);
      cur = cur.parentElement;
    }
    let bg = [255, 255, 255, 1];
    for (let i = chain.length - 1; i >= 0; i--) {
      const c = parseRgba(getComputedStyle(chain[i]).backgroundColor);
      if (c && c[3] > 0) bg = blend(c, bg);
    }
    return bg;
  };

  const isVisible = (el) => {
    if (!el || el.nodeType !== 1) return false;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return false;
    if (el.closest('[hidden], [aria-hidden="true"]')) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };

  const isSkippedNegative = (el) => Boolean(el.closest('[data-taste-specimen="negative"]'));

  const fonts = new Set();
  const radii = new Set();
  const contrastFailures = [];
  const inFlowShadows = [];
  const smallTargets = [];
  const unlabeledControls = [];
  const firstFoldButtons = [];
  const hairlineBodyText = [];
  const nonTabularTables = [];
  const unsizedImages = [];
  let h1Count = 0;
  let bodyFontSize = null;
  let skippedNegativeCount = 0;

  if (document.body) {
    bodyFontSize = parseFloat(getComputedStyle(document.body).fontSize) || 16;
  }

  for (const el of document.querySelectorAll('*')) {
    if (!isVisible(el)) continue;
    if (isSkippedNegative(el)) {
      skippedNegativeCount++;
      continue;
    }

    const tag = el.tagName.toLowerCase();
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();

    if (tag === 'h1') h1Count++;

    for (const side of ['borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomRightRadius', 'borderBottomLeftRadius']) {
      const val = cs[side];
      if (val && val !== '0px' && !val.includes('999')) {
        radii.add(val);
      }
    }

    if (cs.boxShadow && cs.boxShadow !== 'none' && (cs.position === 'static' || cs.position === 'relative')) {
      // Allow subtle inset or 1px focus/border ring shadows without blur; flag blurred elevation shadows
      const hasBlur = /px\s+[\d.-]+px\s+[1-9]\d*px/.test(cs.boxShadow);
      if (hasBlur && inFlowShadows.length < 10) {
        inFlowShadows.push(tag + (el.className ? '.' + String(el.className).trim().split(/\s+/).slice(0, 2).join('.') : ''));
      }
    }

    // Direct text contrast & font family check
    let hasDirectText = false;
    for (const n of el.childNodes) {
      if (n.nodeType === 3 && n.textContent.trim().length > 0) {
        hasDirectText = true;
        break;
      }
    }
    if (hasDirectText) {
      const primaryFont = (cs.fontFamily || '').split(',')[0].trim().replace(/^["']|["']$/g, '');
      if (primaryFont) fonts.add(primaryFont);
      const fg = parseRgba(cs.color);
      if (fg) {
        const bg = getEffectiveBg(el);
        const effFg = blend(fg, bg);
        const r = ratio(effFg, bg);
        const fs = parseFloat(cs.fontSize) || 16;
        const fw = parseInt(cs.fontWeight, 10) || 400;
        if (fw < 300 && fs <= 18 && hairlineBodyText.length < 10) {
          hairlineBodyText.push({
            element: tag + (el.className ? '.' + String(el.className).trim().split(/\s+/)[0] : ''),
            text: el.textContent.trim().slice(0, 40),
            size: Number(fs.toFixed(1)),
            weight: fw,
          });
        }
        const threshold = (fs >= 24 || (fs >= 18.66 && fw >= 700)) ? 3.0 : 4.5;
        if (r < threshold && contrastFailures.length < 15) {
          contrastFailures.push({
            element: tag + (el.className ? '.' + String(el.className).trim().split(/\s+/)[0] : ''),
            text: el.textContent.trim().slice(0, 40),
            ratio: Number(r.toFixed(2)),
            threshold,
          });
        }
      }
    }

    // Interactive checks (WCAG 2.5.8 exempts inline text links inside prose sentences)
    const isInteractive = ['a', 'button', 'input', 'select', 'textarea'].includes(tag) || el.getAttribute('role') === 'button';
    const isInlineProseLink = tag === 'a' && cs.display === 'inline' && Boolean(el.closest('p, li, dd, td, span, figcaption'));
    if (isInteractive && !isInlineProseLink) {
      if (rect.width < 24 || rect.height < 24) {
        if (smallTargets.length < 10) {
          smallTargets.push({
            element: tag,
            text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 30),
            size: `${Math.round(rect.width)}x${Math.round(rect.height)}`,
          });
        }
      }
      const isOnScreen = rect.right > 0 && rect.left < window.innerWidth && rect.bottom > 0;
      if (['button', 'a'].includes(tag) && isOnScreen && rect.top < 700) {
        const bg = parseRgba(cs.backgroundColor);
        const pageBg = getEffectiveBg(document.body || document.documentElement);
        if (bg && bg[3] > 0.25 && ratio(blend(bg, pageBg), pageBg) > 2.0 && cs.display !== 'inline') {
          firstFoldButtons.push((el.textContent || el.getAttribute('aria-label') || tag).trim().slice(0, 32));
        }
      }
    }

    if (tag === 'table') {
      const numericCells = Array.from(el.querySelectorAll('td')).filter((td) => /\d/.test(td.textContent || ''));
      if (numericCells.length > 0) {
        const tableFvn = (cs.fontVariantNumeric || '').toLowerCase();
        const hasTabular = tableFvn.includes('tabular-nums') || numericCells.some((td) => (getComputedStyle(td).fontVariantNumeric || '').toLowerCase().includes('tabular-nums'));
        if (!hasTabular && nonTabularTables.length < 10) {
          nonTabularTables.push({
            element: 'table' + (el.className ? '.' + String(el.className).trim().split(/\s+/)[0] : ''),
            sample: numericCells[0].textContent.trim().slice(0, 24),
          });
        }
      }
    }

    if (tag === 'img') {
      const hasAttrDims = el.hasAttribute('width') && el.hasAttribute('height');
      const hasAspect = cs.aspectRatio && cs.aspectRatio !== 'auto';
      if (!hasAttrDims && !hasAspect && unsizedImages.length < 10) {
        unsizedImages.push({
          element: 'img',
          src: (el.getAttribute('src') || '').slice(0, 60),
        });
      }
    }

    if (['input', 'textarea', 'select'].includes(tag)) {
      const t = (el.getAttribute('type') || '').toLowerCase();
      if (!['hidden', 'submit', 'button', 'reset'].includes(t)) {
        const id = el.getAttribute('id');
        const hasLabelEl = id ? Boolean(document.querySelector(`label[for="${CSS.escape(id)}"]`)) : Boolean(el.closest('label'));
        const hasAria = Boolean(el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') || el.getAttribute('title'));
        if (!hasLabelEl && !hasAria) {
          unlabeledControls.push({ element: tag, name: el.getAttribute('name') || el.getAttribute('placeholder') || '(unnamed)' });
        }
      }
    }
  }

  return {
    title: document.title,
    innerWidth: window.innerWidth,
    scrollWidth: document.documentElement.scrollWidth,
    overflowX: document.documentElement.scrollWidth > window.innerWidth + 1,
    h1Count,
    bodyFontSize,
    fonts: Array.from(fonts),
    radii: Array.from(radii),
    inFlowShadows,
    contrastFailures,
    smallTargets,
    unlabeledControls,
    firstFoldButtons,
    hairlineBodyText,
    nonTabularTables,
    unsizedImages,
    skippedNegativeCount,
  };
})()
"""


def find_chromium_binary(explicit: str | None) -> str | None:
    if explicit:
        return explicit if Path(explicit).exists() else shutil.which(explicit)
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome-headless-shell", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    patterns = [
        str(Path.home() / ".cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-*/chrome-headless-shell"),
        str(Path.home() / ".cache/ms-playwright/chromium-*/chrome-*/chrome"),
        "/root/.cache/ms-playwright/chromium*/**/chrome*",
    ]
    for pat in patterns:
        matches = sorted(glob.glob(pat, recursive=True), reverse=True)
        for m in matches:
            p = Path(m)
            if p.is_file() and os.access(p, os.X_OK):
                return str(p)
    return None


class CdpClient:
    """Minimal stdlib RFC 6455 WebSocket client for Chrome DevTools Protocol."""

    def __init__(self, ws_url: str, timeout: float = 15.0) -> None:
        parsed = urllib.parse.urlparse(ws_url)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or (443 if parsed.scheme == "wss" else 80)
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query

        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        self._buf = bytearray()
        self._next_id = 1

        key = base64.b64encode(os.urandom(16)).decode("ascii")
        req = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode("ascii"))

        while b"\r\n\r\n" not in self._buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("WebSocket handshake closed unexpectedly")
            self._buf.extend(chunk)

        sep = self._buf.index(b"\r\n\r\n") + 4
        header = bytes(self._buf[:sep]).decode("latin1")
        del self._buf[:sep]
        if " 101 " not in header:
            raise ConnectionError(f"WebSocket upgrade failed: {header.splitlines()[0]}")

    def close(self) -> None:
        try:
            self._send_frame(0x8, b"")
        except OSError:
            pass
        self.sock.close()

    def _read_exact(self, n: int) -> bytes:
        while len(self._buf) < n:
            chunk = self.sock.recv(max(4096, n - len(self._buf)))
            if not chunk:
                raise EOFError("WebSocket connection closed")
            self._buf.extend(chunk)
        out = bytes(self._buf[:n])
        del self._buf[:n]
        return out

    def _send_frame(self, opcode: int, payload: bytes) -> None:
        mask_key = os.urandom(4)
        length = len(payload)
        header = bytearray([0x80 | opcode])
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        header.extend(mask_key)
        masked = bytes(b ^ mask_key[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(header) + masked)

    def _recv_message(self) -> str:
        fragments: list[bytes] = []
        while True:
            b1, b2 = self._read_exact(2)
            fin = (b1 & 0x80) != 0
            opcode = b1 & 0x0F
            masked = (b2 & 0x80) != 0
            length = b2 & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._read_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._read_exact(8))[0]
            mask = self._read_exact(4) if masked else b""
            payload = self._read_exact(length)
            if masked:
                payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))

            if opcode == 0x8:
                raise EOFError("WebSocket close frame received")
            if opcode == 0x9:
                self._send_frame(0xA, payload)
                continue
            if opcode == 0xA:
                continue
            fragments.append(payload)
            if fin:
                return b"".join(fragments).decode("utf-8", errors="replace")

    def call(self, method: str, params: dict | None = None, wait_event: str | None = None) -> dict:
        req_id = self._next_id
        self._next_id += 1
        msg = json.dumps({"id": req_id, "method": method, "params": params or {}})
        self._send_frame(0x1, msg.encode("utf-8"))
        result: dict | None = None
        seen_event = wait_event is None
        while result is None or not seen_event:
            raw = self._recv_message()
            data = json.loads(raw)
            if data.get("id") == req_id:
                if "error" in data:
                    raise RuntimeError(f"CDP error on {method}: {data['error']}")
                result = data.get("result", {})
            elif wait_event and data.get("method") == wait_event:
                seen_event = True
        return result


def wait_for_cdp_port(proc: subprocess.Popen[str], timeout: float = 10.0) -> int:
    deadline = time.monotonic() + timeout
    assert proc.stderr is not None
    while time.monotonic() < deadline:
        line = proc.stderr.readline()
        if not line:
            if proc.poll() is not None:
                raise RuntimeError(f"Chromium exited early with code {proc.returncode}")
            time.sleep(0.05)
            continue
        m = re.search(r"ws://127\.0\.0\.1:(\d+)/", line)
        if m:
            return int(m.group(1))
    raise TimeoutError("Timed out waiting for Chromium DevTools WebSocket port")


def inspect_with_chromium(
    url: str,
    chrome_bin: str,
    desktop_w: int,
    mobile_w: int,
    screenshot_dir: Path | None = None,
) -> dict:
    with tempfile.TemporaryDirectory(prefix="pt-critique-") as profile_dir:
        cmd = [
            chrome_bin,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--remote-debugging-port=0",
            f"--user-data-dir={profile_dir}",
            "about:blank",
        ]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        client: CdpClient | None = None
        try:
            port = wait_for_cdp_port(proc)
            targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=5).read())
            page_target = next((t for t in targets if t.get("type") == "page"), None)
            if not page_target:
                req = urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT")
                page_target = json.loads(urllib.request.urlopen(req, timeout=5).read())

            client = CdpClient(page_target["webSocketDebuggerUrl"], timeout=15.0)
            client.call("Page.enable")
            client.call("Runtime.enable")
            client.call(
                "Emulation.setDeviceMetricsOverride",
                {"width": desktop_w, "height": 800, "deviceScaleFactor": 1, "mobile": False},
            )
            client.call("Page.navigate", {"url": url}, wait_event="Page.loadEventFired")

            # Wait briefly for webfonts and layout settle
            client.call(
                "Runtime.evaluate",
                {
                    "expression": "Promise.race([document.fonts ? document.fonts.ready : Promise.resolve(), new Promise(r => setTimeout(r, 1500))])",
                    "awaitPromise": True,
                },
            )
            desktop_res = client.call(
                "Runtime.evaluate",
                {"expression": EVAL_DOM_JS, "returnByValue": True},
            )
            desktop = desktop_res["result"]["value"]
            desktop["targetWidth"] = desktop_w
            screenshots: dict[str, str] = {}
            if screenshot_dir is not None:
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                shot = client.call("Page.captureScreenshot", {"format": "png"})
                if shot.get("data"):
                    d_path = screenshot_dir / "desktop.png"
                    d_path.write_bytes(base64.b64decode(shot["data"]))
                    screenshots["desktop"] = str(d_path)

            client.call(
                "Emulation.setDeviceMetricsOverride",
                {"width": mobile_w, "height": 812, "deviceScaleFactor": 2, "mobile": True},
            )
            client.call(
                "Runtime.evaluate",
                {"expression": "new Promise(r => setTimeout(r, 80))", "awaitPromise": True},
            )
            mobile_res = client.call(
                "Runtime.evaluate",
                {"expression": EVAL_DOM_JS, "returnByValue": True},
            )
            mobile = mobile_res["result"]["value"]
            mobile["targetWidth"] = mobile_w
            if screenshot_dir is not None:
                shot = client.call("Page.captureScreenshot", {"format": "png"})
                if shot.get("data"):
                    m_path = screenshot_dir / "mobile.png"
                    m_path.write_bytes(base64.b64decode(shot["data"]))
                    screenshots["mobile"] = str(m_path)
            payload = {"mode": "chromium-cdp", "chrome": chrome_bin, "desktop": desktop, "mobile": mobile}
            if screenshots:
                payload["screenshots"] = screenshots
            return payload
        finally:
            if client is not None:
                client.close()
            proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()


def inspect_http_fallback(url: str, allow_fonts: set[str]) -> tuple[dict, list[audit.Finding]]:
    with urllib.request.urlopen(url, timeout=10) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    findings = audit.audit_text(html, url, allow_fonts=allow_fonts)
    for href in re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']([^"\']+)["\']', html, re.I):
        css_url = urllib.parse.urljoin(url, href)
        if urllib.parse.urlparse(css_url).netloc == urllib.parse.urlparse(url).netloc:
            try:
                with urllib.request.urlopen(css_url, timeout=10) as css_resp:
                    css = css_resp.read().decode("utf-8", errors="replace")
                findings.extend(audit.audit_text(css, css_url, allow_fonts=allow_fonts))
            except urllib.error.URLError:
                pass
    meta = {"mode": "http-static-fallback", "url": url}
    return meta, findings


def dom_metrics_to_findings(
    url: str,
    desktop: dict,
    mobile: dict,
    allow_fonts: set[str],
) -> list[audit.Finding]:
    findings: list[audit.Finding] = []

    if desktop.get("h1Count", 1) != 1:
        findings.append(
            audit.Finding(
                url,
                0,
                "hierarchy.single-h1",
                "hierarchy",
                "error",
                f"Rendered page has {desktop.get('h1Count', 0)} visible <h1> elements (expected 1).",
                "Render exactly one <h1> defining the main job of the screen.",
            )
        )

    cta_count = len(desktop.get("firstFoldButtons", []))
    if cta_count > 1:
        names = ", ".join(desktop["firstFoldButtons"][:4])
        findings.append(
            audit.Finding(
                url,
                0,
                "hierarchy.one-primary-action",
                "hierarchy",
                "warn",
                f"{cta_count} high-contrast filled buttons visible in the first 700px ({names}).",
                "Keep one filled primary CTA; convert supporting actions to outlined buttons or text links.",
            )
        )

    for viewport_label, data in (("desktop", desktop), ("mobile", mobile)):
        target_w = data.get("targetWidth", data.get("innerWidth", 0))
        effective_w = max(data.get("scrollWidth", 0), data.get("innerWidth", 0))
        if data.get("overflowX") or effective_w > target_w + 1:
            findings.append(
                audit.Finding(
                    url,
                    0,
                    "a11y.overflow-x",
                    "accessibility",
                    "error",
                    f"Horizontal overflow at {viewport_label} width ({effective_w}px > {target_w}px).",
                    "Constrain children with minmax(0, 1fr), max-width: 100%, or scrollable wrappers.",
                )
            )

    fonts = desktop.get("fonts", [])
    costume_lower = {f.lower() for f in audit.COSTUME_FONTS}
    for f in fonts:
        if f.lower() in costume_lower and f.lower() not in allow_fonts:
            findings.append(
                audit.Finding(
                    url,
                    0,
                    "type.avoid-tells",
                    "uniqueness",
                    "error",
                    f"Rendered page uses costume typeface '{f}'.",
                    "Switch to system-ui or IBM Plex / Public Sans / Newsreader / Source Serif 4.",
                )
            )

    generic = {g.lower() for g in audit.GENERIC_FONT_TOKENS} | {"times new roman", "times", "courier new"}
    custom_fonts = [f for f in fonts if f.lower() not in generic]
    if len(custom_fonts) > 2:
        findings.append(
            audit.Finding(
                url,
                0,
                "type.two-family-cap",
                "restraint",
                "error",
                f"{len(custom_fonts)} webfont/named families rendered ({', '.join(custom_fonts[:4])}). Max is 2.",
                "Consolidate to at most two families (plus monospace only when code/telemetry needs it).",
            )
        )

    body_px = desktop.get("bodyFontSize") or 16
    if body_px < 14:
        findings.append(
            audit.Finding(
                url,
                0,
                "type.body-floor",
                "accessibility",
                "error",
                f"Computed <body> font size is {body_px:.1f}px (minimum 14px).",
                "Raise root body text to 15–17px (0.9375–1.0625rem).",
            )
        )

    radii = desktop.get("radii", [])
    if len(radii) > 3:
        findings.append(
            audit.Finding(
                url,
                0,
                "material.radius-system",
                "restraint",
                "warn",
                f"{len(radii)} distinct border-radius values rendered ({', '.join(radii[:5])}). Cap at 3.",
                "Standardize onto one architectural radius token across controls and containers.",
            )
        )

    shadows = desktop.get("inFlowShadows", [])
    if shadows:
        findings.append(
            audit.Finding(
                url,
                0,
                "material.shadow-budget",
                "restraint",
                "warn",
                f"Blurred elevation shadow detected on in-flow element(s): {', '.join(shadows[:4])}.",
                "Use 1px hairline borders or step in surface tone; keep shadows for overlays only.",
            )
        )

    for cf in desktop.get("contrastFailures", []):
        findings.append(
            audit.Finding(
                url,
                0,
                "color.contrast-floor",
                "accessibility",
                "error",
                f"Low computed contrast {cf['ratio']}:1 (< {cf['threshold']}:1) on {cf['element']} ({cf['text']!r}).",
                "Darken text or adjust surface tone so normal text reaches >= 4.5:1 and large text >= 3.0:1.",
            )
        )

    for st in desktop.get("smallTargets", []):
        findings.append(
            audit.Finding(
                url,
                0,
                "a11y.target-size",
                "accessibility",
                "warn",
                f"Interactive <{st['element']}> '{st['text']}' is {st['size']}px (< 24x24px minimum).",
                "Expand padding or min-width/min-height so click/tap targets are at least 24x24px.",
            )
        )

    for uc in desktop.get("unlabeledControls", []):
        findings.append(
            audit.Finding(
                url,
                0,
                "a11y.placeholder-label",
                "accessibility",
                "error",
                f"Rendered <{uc['element']}> ({uc['name']}) lacks a visible <label> or aria-label.",
                "Associate an explicit <label for=...> element with every input control.",
            )
        )

    for hb in desktop.get("hairlineBodyText", []):
        findings.append(
            audit.Finding(
                url,
                0,
                "type.no-hairline-body",
                "typography",
                "error",
                f"Computed font-weight {hb['weight']} at {hb['size']}px on {hb['element']} ({hb['text']!r}) harms reading legibility.",
                "Use font-weight 400-500 for reading copy and UI labels <= 18px; reserve weights < 300 for display headlines >= 48px.",
            )
        )

    for nt in desktop.get("nonTabularTables", []):
        findings.append(
            audit.Finding(
                url,
                0,
                "type.numbers",
                "typography",
                "warn",
                f"Rendered numeric {nt['element']} (sample {nt['sample']!r}) lacks computed font-variant-numeric: tabular-nums.",
                "Apply font-variant-numeric: tabular-nums on numeric tables so columns align vertically.",
            )
        )

    for ui in desktop.get("unsizedImages", []):
        findings.append(
            audit.Finding(
                url,
                0,
                "a11y.semantics",
                "accessibility",
                "warn",
                f"Rendered <{ui['element']}> ({ui['src'] or 'inline'}) lacks width/height attributes or CSS aspect-ratio.",
                "Declare explicit width and height attributes (or CSS aspect-ratio) on rendered images to prevent layout shift.",
            )
        )

    return findings


def run_url_critique(
    url: str,
    desktop_width: int = 1280,
    mobile_width: int = 375,
    allow_fonts: set[str] | None = None,
    no_browser: bool = False,
    chrome_path: str | None = None,
    screenshot_dir: str | Path | None = None,
) -> dict:
    """Critique a live URL using headless Chromium CDP (or HTTP fallback) and return structured results."""
    norm_fonts = {f.strip().lower() for f in (allow_fonts or set()) if f and f.strip()}
    chrome_bin = None if no_browser else find_chromium_binary(chrome_path)
    shot_path = Path(screenshot_dir) if screenshot_dir else None

    if chrome_bin:
        report_meta = inspect_with_chromium(
            url, chrome_bin, desktop_width, mobile_width, screenshot_dir=shot_path
        )
        findings = dom_metrics_to_findings(
            url, report_meta["desktop"], report_meta["mobile"], norm_fonts
        )
    else:
        report_meta, findings = inspect_http_fallback(url, norm_fonts)

    scores = audit.score_dimensions(findings)
    return {
        "url": url,
        "mode": report_meta["mode"],
        "meta": report_meta,
        "scores": scores,
        "findings": [f.__dict__ for f in findings],
        "passed": not any(f.severity == "error" for f in findings),
        "screenshots": report_meta.get("screenshots", {}),
        "_finding_objects": findings,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Critique a live URL against Premium Taste rules.")
    parser.add_argument("url", help="Target HTTP(S) or file:// URL to inspect.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--chrome-path", help="Explicit path to Chrome/Chromium binary.")
    parser.add_argument("--no-browser", action="store_true", help="Force HTTP static fallback instead of headless Chromium.")
    parser.add_argument("--desktop-width", type=int, default=1280)
    parser.add_argument("--mobile-width", type=int, default=375)
    parser.add_argument("--allow-font", action="append", default=[])
    parser.add_argument("--screenshot-dir", help="Optional directory to write desktop.png and mobile.png via Chromium CDP.")
    parser.add_argument("--warn-only", action="store_true")
    args = parser.parse_args(argv)

    result = run_url_critique(
        args.url,
        desktop_width=args.desktop_width,
        mobile_width=args.mobile_width,
        allow_fonts=set(args.allow_font),
        no_browser=args.no_browser,
        chrome_path=args.chrome_path,
        screenshot_dir=args.screenshot_dir,
    )
    finding_objs = result.pop("_finding_objects")
    report_meta = result["meta"]

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Premium Taste Live Critique — {args.url} ({report_meta['mode']})")
        if report_meta["mode"] == "chromium-cdp":
            d = report_meta["desktop"]
            m = report_meta["mobile"]
            print(
                f"  Desktop {d['innerWidth']}px (scroll {d['scrollWidth']}px) · "
                f"Mobile {m['innerWidth']}px (scroll {m['scrollWidth']}px)"
            )
            print(
                f"  Fonts: {', '.join(d['fonts']) or 'default'} | "
                f"Body: {d['bodyFontSize']:.1f}px | H1s: {d['h1Count']} | "
                f"Radii: {len(d['radii'])} | First-fold filled CTAs: {len(d['firstFoldButtons'])}"
            )
            if report_meta.get("screenshots"):
                print(f"  Screenshots: {report_meta['screenshots']}")
            if d.get("skippedNegativeCount"):
                print(f"  Note: skipped {d['skippedNegativeCount']} elements inside [data-taste-specimen=\"negative\"]")
        print()
        print(audit.format_text(finding_objs, 1))

    return 0 if (args.warn_only or result["passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
