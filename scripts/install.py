#!/usr/bin/env python3
"""Install the Premium Taste judgment layer into a target project directory.

Standard-library only. Copies the core judgment files into
<target>/.premium-taste/ and adds lightweight pointer files for your coding
agent without duplicating the principles into host rule files.

Examples:
    python3 scripts/install.py /path/to/your-app
    python3 scripts/install.py . --agent cursor
    python3 scripts/install.py /path/to/your-app --agent all --dry-run
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

CORE_DIRS = ("taste", "tokens")
CORE_FILES = (
    "AGENTS.md",
    "skills/critique-ui.md",
    "skills/premium-taste/SKILL.md",
    "scripts/audit.py",
    "scripts/critique_url.py",
    "scripts/mcp_server.py",
    "scripts/build_site_data.py",
)

AGENTS_POINTER = """<!-- premium-taste:start -->
## UI and Design Judgment (Premium Taste)

Before creating or restyling any interface, read `.premium-taste/AGENTS.md` and follow its load order (job -> 1 direction -> 1 reference -> optional pattern -> Decision Ledger -> generate -> `.premium-taste/skills/critique-ui.md`). After generating UI, run `python3 .premium-taste/scripts/audit.py <changed-files>`.
<!-- premium-taste:end -->
"""

CLAUDE_SKILL = """---
name: critique-ui
description: >
  Design and critique user interfaces using Premium Taste. Use before building
  a new screen, reviewing UI quality, or replacing a generic layout.
---

# Premium Taste

Read `.premium-taste/AGENTS.md` and follow its load order before generating UI:

1. Name the job of this screen in one sentence with a verb.
2. Pick **1** direction in `.premium-taste/taste/directions.yaml`.
3. Load **1** matching reference in `.premium-taste/taste/references/index.yaml` and (when recurring) **1** pattern in `.premium-taste/taste/patterns/index.yaml`.
4. Record the 4-line Decision Ledger (`Direction`, `Reference`, `Pattern`, `1 rule at risk`) and generate from the structural idea, not the reference palette.
5. Critique and revise against `.premium-taste/skills/critique-ui.md`, citing rule ids from `.premium-taste/taste/principles.yaml`, then run `python3 .premium-taste/scripts/audit.py <files>` (and `critique_url.py <url>` if a server runs).
"""

CURSOR_RULE = """---
description: Apply Premium Taste design judgment before generating or editing UI screens.
globs: ["**/*.html", "**/*.css", "**/*.tsx", "**/*.jsx", "**/*.vue", "**/*.svelte", "**/*.astro"]
alwaysApply: false
---

Before building or restyling any UI screen:

1. Read `.premium-taste/AGENTS.md` and follow its load order.
2. Pick 1 direction in `.premium-taste/taste/directions.yaml`, 1 reference in `.premium-taste/taste/references/index.yaml`, and (when recurring) 1 pattern in `.premium-taste/taste/patterns/index.yaml`.
3. Refuse anti-patterns in `.premium-taste/taste/anti-patterns.yaml`.
4. Run `python3 .premium-taste/scripts/audit.py <files>` and `.premium-taste/skills/critique-ui.md` on the result, applying structural revisions before color tweaks.
"""

AGENT_SKILL = """---
name: premium-taste
description: >
  Apply Premium Taste judgment before building or refining any UI screen. Picks
  one direction, loads one reference structure and optional screen/flow pattern,
  avoids generic SaaS skeletons, and runs deterministic static/browser UI audits.
---

# Premium Taste

Read `.premium-taste/AGENTS.md` first and follow its load order strictly:

1. Name the job of the screen in one sentence with a verb.
2. Pick **one** direction in `.premium-taste/taste/directions.yaml`.
3. Load **one** reference from `.premium-taste/taste/references/index.yaml` whose job is close, plus **one** pattern from `.premium-taste/taste/patterns/index.yaml` when building a recurring screen or multi-step flow.
4. If the project has no `DESIGN.md` or brand guide, load the matching `.premium-taste/tokens/*.DESIGN.md` sample identity.
5. After generating, run `python3 .premium-taste/scripts/audit.py <files>` (and `.premium-taste/scripts/critique_url.py <url>` for rendered layouts) and review `.premium-taste/skills/critique-ui.md`.
"""


def detect_agents(target: Path) -> set[str]:
    found: set[str] = set()
    if (target / ".claude").exists() or (target / "CLAUDE.md").exists():
        found.add("claude")
    if (target / ".cursor").exists() or (target / ".cursorrules").exists():
        found.add("cursor")
    if (target / ".agents").exists() or (target / "AGENTS.md").exists():
        found.add("agents")
    if not found:
        # Install universal agent skill + AGENTS.md pointer by default
        found.add("agents")
    return found


def copy_core(target: Path, dry_run: bool) -> list[str]:
    actions: list[str] = []
    dest_root = target / ".premium-taste"

    if dest_root.exists():
        actions.append(f"replace {dest_root}")
        if not dry_run:
            shutil.rmtree(dest_root)

    for rel in CORE_FILES:
        src = REPO_ROOT / rel
        dst = dest_root / rel
        actions.append(f"copy {dst}")
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    for rel_dir in CORE_DIRS:
        src_dir = REPO_ROOT / rel_dir
        dst_dir = dest_root / rel_dir
        actions.append(f"copy {dst_dir}/")
        if not dry_run:
            shutil.copytree(src_dir, dst_dir)

    return actions


def write_text(path: Path, content: str, dry_run: bool) -> str:
    label = f"write {path}"
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return label


def update_agents_md(target: Path, dry_run: bool) -> str | None:
    agents_file = target / "AGENTS.md"
    if agents_file.exists():
        current = agents_file.read_text(encoding="utf-8")
        if ".premium-taste/AGENTS.md" in current or "premium-taste:start" in current:
            return f"skip {agents_file} (already links .premium-taste)"
        updated = current.rstrip() + "\n\n" + AGENTS_POINTER
        if not dry_run:
            agents_file.write_text(updated, encoding="utf-8")
        return f"append pointer to {agents_file}"
    if not dry_run:
        agents_file.write_text("# AGENTS.md\n\n" + AGENTS_POINTER, encoding="utf-8")
    return f"create {agents_file}"


def update_mcp_json(target: Path, dry_run: bool) -> str:
    mcp_file = target / ".mcp.json"
    data: dict = {}
    if mcp_file.exists():
        data = json.loads(mcp_file.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            data = {}
    servers = data.setdefault("mcpServers", {})
    servers["premium-taste"] = {
        "command": "python3",
        "args": [".premium-taste/scripts/mcp_server.py"],
    }
    if not dry_run:
        mcp_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return f"update {mcp_file} (registered premium-taste stdio MCP server)"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Premium Taste into a target repository."
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Path to the target project directory.",
    )
    parser.add_argument(
        "--agent",
        choices=("auto", "claude", "cursor", "agents", "all", "none"),
        default="auto",
        help="Which agent integration files to write (default: auto-detect).",
    )
    parser.add_argument(
        "--no-agents-md",
        action="store_true",
        help="Do not create or append a pointer in target AGENTS.md.",
    )
    parser.add_argument(
        "--mcp",
        action="store_true",
        help="Register the bundled MCP server in <target>/.mcp.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without changing files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target = args.target.resolve()

    if target == REPO_ROOT:
        print("Target cannot be the Premium Taste repo itself.", file=sys.stderr)
        return 1

    if not target.exists():
        if args.dry_run:
            print(f"would create directory {target}")
        else:
            target.mkdir(parents=True, exist_ok=True)

    actions = copy_core(target, args.dry_run)

    if args.agent == "none":
        selected: set[str] = set()
    elif args.agent == "all":
        selected = {"claude", "cursor", "agents"}
    elif args.agent == "auto":
        selected = detect_agents(target)
    else:
        selected = {args.agent}

    if "claude" in selected:
        actions.append(
            write_text(
                target / ".claude" / "skills" / "critique-ui" / "SKILL.md",
                CLAUDE_SKILL,
                args.dry_run,
            )
        )
    if "cursor" in selected:
        actions.append(
            write_text(
                target / ".cursor" / "rules" / "premium-taste.mdc",
                CURSOR_RULE,
                args.dry_run,
            )
        )
    if "agents" in selected:
        actions.append(
            write_text(
                target / ".agents" / "skills" / "premium-taste" / "SKILL.md",
                AGENT_SKILL,
                args.dry_run,
            )
        )

    if not args.no_agents_md and args.agent != "none":
        note = update_agents_md(target, args.dry_run)
        if note:
            actions.append(note)

    if args.mcp:
        actions.append(update_mcp_json(target, args.dry_run))

    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}Installed Premium Taste in {target}:")
    for line in actions:
        print(f"  - {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
