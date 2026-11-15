"""MCP framing, tools, resources, and prompts. verify_url stays on the HTTP fallback."""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import mcp_server  # noqa: E402


class McpServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = mcp_server.load_catalog()

    def test_content_length_header_need_not_be_first(self) -> None:
        body = b'{"jsonrpc":"2.0","id":1,"method":"ping"}'
        raw = (
            b"Content-Type: application/vscode-jsonrpc; charset=utf-8\r\n"
            + f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
            + body
        )
        message, framing = mcp_server.read_message(io.BytesIO(raw))
        self.assertEqual(framing, "lsp")
        self.assertEqual(message["method"], "ping")

    def test_short_body_raises(self) -> None:
        with self.assertRaises(ValueError):
            mcp_server.read_message(io.BytesIO(b"Content-Length: 20\r\n\r\n{}"))

    def test_non_dict_and_bad_json_are_rpc_errors(self) -> None:
        for payload, code in ((b"[1,2]\n", b"-32600"), (b"{not json}\n", b"-32700")):
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "mcp_server.py")],
                input=payload,
                capture_output=True,
                check=False,
                timeout=15,
            )
            self.assertIn(code, proc.stdout)

    def test_score_direction_uses_whole_tokens(self) -> None:
        precise = next(item for item in self.data["directions"] if item["id"] == "precise-technical")
        self.assertEqual(mcp_server.score_direction("Browse a clinic space catalog", precise), 0)
        self.assertGreater(mcp_server.score_direction("Read the cli log", precise), 0)

    def test_unknown_token_format_is_rejected_and_css_includes_scales(self) -> None:
        with self.assertRaises(ValueError):
            mcp_server.tool_get_tokens({"direction": "cinematic-dark", "format": "scss"}, self.data)
        css = mcp_server.tool_get_tokens({"direction": "cinematic-dark", "format": "css"}, self.data)
        self.assertIn("--pt-space-", css)
        self.assertIn("--pt-radius-", css)
        self.assertIn("--pt-font-credit-fontstyle: italic", css)

    def test_zero_files_do_not_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            payload = json.loads(mcp_server.tool_audit_ui({"file_path": tmp}, self.data))
        self.assertEqual(payload["files_checked"], 0)
        self.assertFalse(payload["passed"])

    def test_six_tools_resources_prompts_and_version(self) -> None:
        tools = mcp_server.handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, self.data)
        names = [item["name"] for item in tools["result"]["tools"]]
        self.assertEqual(
            names,
            ["pick_direction", "get_reference", "get_tokens", "get_pattern", "audit_ui", "verify_url"],
        )
        init = mcp_server.handle_request(
            {"jsonrpc": "2.0", "id": 2, "method": "initialize", "params": {}},
            self.data,
        )
        self.assertEqual(init["result"]["serverInfo"]["version"], "1.1.0")
        self.assertEqual(
            set(init["result"]["capabilities"]),
            {"tools", "resources", "prompts"},
        )
        resources = mcp_server.handle_request({"jsonrpc": "2.0", "id": 3, "method": "resources/list"}, self.data)
        uris = [item["uri"] for item in resources["result"]["resources"]]
        self.assertIn("premium-taste://taste/principles.yaml", uris)
        self.assertIn("premium-taste://skills/critique-ui/SKILL.md", uris)
        prompts = mcp_server.handle_request({"jsonrpc": "2.0", "id": 4, "method": "prompts/list"}, self.data)
        self.assertEqual(
            [item["name"] for item in prompts["result"]["prompts"]],
            ["critique-ui", "choose-direction"],
        )
        chosen = mcp_server.handle_request(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "prompts/get",
                "params": {"name": "choose-direction", "arguments": {"job": "read the essay"}},
            },
            self.data,
        )
        text = chosen["result"]["messages"][0]["content"]["text"]
        self.assertIn("editorial-print", text)
        self.assertIn("generic skeleton", text)

    def test_resource_paths_cannot_escape(self) -> None:
        response = mcp_server.handle_request(
            {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "resources/read",
                "params": {"uri": "premium-taste://../AGENTS.md"},
            },
            self.data,
        )
        self.assertEqual(response["error"]["code"], -32602)

    def test_verify_url_uses_http_fallback(self) -> None:
        with self.assertRaises(ValueError):
            mcp_server.tool_verify_url({"url": "file:///tmp/secret"}, self.data)
        with mock.patch("critique_url.urllib.request.urlopen", side_effect=urllib.error.URLError("down")):
            payload = json.loads(mcp_server.tool_verify_url({"url": "https://example.com/"}, self.data))
        self.assertFalse(payload["passed"])
        self.assertTrue(payload["error"])


if __name__ == "__main__":
    unittest.main()
