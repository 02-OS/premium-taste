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
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

CORE_DIRS = ("taste", "tokens")
CORE_FILES = (
    "AGENTS.md",
    "skills/critique-ui/SKILL.md",
    "scripts/audit.py",
    "scripts/critique_url.py",
    "scripts/mcp_server.py",
    "scripts/build_site_data.py",
)

AGENTS_POINTER = """<!-- premium-taste:start -->
## UI and Design Judgment (Premium Taste)

Before creating or restyling any interface, read `.premium-taste/AGENTS.md` and follow its load order (job -> 1 direction -> 1 reference -> generate -> `.premium-taste/skills/critique-ui/SKILL.md`). After generating UI, run `python3 .premium-taste/scripts/audit.py <changed-files>`.
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
2. Pick one direction in `.premium-taste/taste/directions.yaml`.
3. Load one matching reference from `.premium-taste/taste/references/index.yaml`.
4. Generate from the structural idea, not the reference palette.
5. Critique and revise against `.premium-taste/skills/critique-ui/SKILL.md`, citing rule ids from `.premium-taste/taste/principles.yaml`, then run `python3 .premium-taste/scripts/audit.py <files>`.
"""

CURSOR_RULE = """---
description: Apply Premium Taste design judgment before generating or editing UI screens.
globs: ["**/*.html", "**/*.css", "**/*.tsx", "**/*.jsx", "**/*.vue", "**/*.svelte", "**/*.astro"]
alwaysApply: false
---

Before building or restyling any UI screen:

1. Read `.premium-taste/AGENTS.md` and follow its load order.
2. Pick one direction in `.premium-taste/taste/directions.yaml` and one reference in `.premium-taste/taste/references/index.yaml`.
3. Refuse anti-patterns in `.premium-taste/taste/anti-patterns.yaml`.
4. Run `python3 .premium-taste/scripts/audit.py <files>` and `.premium-taste/skills/critique-ui/SKILL.md` on the result, applying structural revisions before color tweaks.
"""

AGENT_SKILL = """---
name: premium-taste
description: >
  Apply Premium Taste judgment before building or refining any UI screen. Picks
  one direction, loads one reference structure, avoids generic SaaS skeletons,
  and runs a rule-based UI critique.
---

# Premium Taste

Read `.premium-taste/AGENTS.md` first and follow its load order strictly:

1. Name the job of the screen in one sentence with a verb.
2. Pick **one** direction in `.premium-taste/taste/directions.yaml`.
3. Load **one** reference from `.premium-taste/taste/references/index.yaml` whose job is close. Steal its structure, not its palette or fonts.
4. If the project has no `DESIGN.md` or brand guide, you may load the matching `.premium-taste/tokens/*.DESIGN.md` sample identity.
5. After generating, run `python3 .premium-taste/scripts/audit.py <files>` and `.premium-taste/skills/critique-ui/SKILL.md`, fixing structure before color.
"""


def detect_agents(target: Path) -> set[str]:
    found: set[str] = set()
    if (target / ".claude").exists() or (target / "CLAUDE.md").exists():
        found.add("claude")
    if (target / ".cursor").exists() or (target / ".cursorrules").exists():
        found.add("cursor")
    if (target / ".agents").exists() or (target / "AGENTS.md").exists():
        found.add("agents")
    if (target / ".codex").exists():
        found.add("codex")
    if (target / ".gemini").exists():
        found.add("gemini")
    if not found:
        # Install universal agent skill + AGENTS.md pointer by default
        found.add("agents")
    return found


INSTALL_VERSION = "1.1.0"


class InstallError(Exception):
    pass


def archive_url(repo: str, ref: str) -> str:
    """GitHub archive URL for a branch, tag, or commit. No network."""
    base = repo[:-4] if repo.endswith(".git") else repo
    base = base.rstrip("/")
    return f"{base}/archive/{ref}.tar.gz"


def _managed_tree(root: Path) -> list[str]:
    files: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            files.append(path.relative_to(root).as_posix())
    return files


def copy_core(target: Path, dry_run: bool) -> tuple[list[str], list[str]]:
    actions: list[str] = []
    dest_root = target / ".premium-taste"
    if dest_root.is_symlink():
        raise InstallError(f"refusing to replace symlink {dest_root}")
    managed = [f".premium-taste/{rel}" for rel in CORE_FILES]
    if dry_run:
        actions.append(f"copy {dest_root}")
        return actions, managed

    staging = target / ".premium-taste.staging"
    if staging.is_symlink():
        raise InstallError(f"refusing to replace symlink {staging}")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    backup = target / ".premium-taste.backup"
    moved = False
    try:
        for rel in CORE_FILES:
            src = REPO_ROOT / rel
            dst = staging / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            actions.append(f"copy {dest_root / rel}")
        for rel_dir in CORE_DIRS:
            src_dir = REPO_ROOT / rel_dir
            dst_dir = staging / rel_dir
            shutil.copytree(src_dir, dst_dir)
            actions.append(f"copy {dest_root / rel_dir}/")
            for copied in _managed_tree(dst_dir):
                managed.append(f".premium-taste/{rel_dir}/{copied}")
        if dest_root.exists():
            if backup.is_symlink():
                raise InstallError(f"refusing to replace symlink {backup}")
            if backup.exists():
                shutil.rmtree(backup)
            os.replace(dest_root, backup)
            moved = True
        os.replace(staging, dest_root)
        if backup.exists() and not backup.is_symlink():
            shutil.rmtree(backup)
    except Exception:
        if staging.exists() and not staging.is_symlink():
            shutil.rmtree(staging)
        if moved and not dest_root.exists() and backup.exists() and not backup.is_symlink():
            os.replace(backup, dest_root)
        raise
    return actions, managed


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
        try:
            loaded = json.loads(mcp_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            loaded = {}
        if isinstance(loaded, dict):
            data = loaded
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        servers = {}
    data["mcpServers"] = servers
    servers["premium-taste"] = {
        "command": "python3",
        "args": [".premium-taste/scripts/mcp_server.py"],
    }
    if not dry_run:
        mcp_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return f"update {mcp_file} (registered premium-taste stdio MCP server)"


GEMINI_EXTENSION = """{
  "name": "premium-taste",
  "version": "1.1.0",
  "mcpServers": {
    "premium-taste": {
      "command": "python3",
      "args": [".premium-taste/scripts/mcp_server.py"]
    }
  }
}
"""


def inside_repo(target: Path) -> bool:
    try:
        target.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        return False
    return True


def uninstall(target: Path, dry_run: bool) -> list[str]:
    manifest_path = target / ".premium-taste" / ".install-manifest.json"
    if not manifest_path.is_file():
        raise InstallError(f"No install manifest at {manifest_path}")
    try:
        loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise InstallError(f"Malformed install manifest: {exc}") from exc
    files = loaded.get("files") if isinstance(loaded, dict) else None
    if not isinstance(files, list):
        raise InstallError("Install manifest files must be a list.")
    root = target.resolve()
    actions: list[str] = []
    for rel in files:
        candidate = (target / str(rel))
        if candidate.is_symlink():
            resolved = candidate.resolve()
        else:
            resolved = candidate.resolve()
        if resolved != root and root not in resolved.parents:
            actions.append(f"skip escaped path {rel}")
            continue
        if candidate.is_symlink() or candidate.is_file():
            actions.append(f"remove {candidate}")
            if not dry_run:
                candidate.unlink()
    return actions


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Premium Taste into a target repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=Path("."),
        help="Path to the target project directory (default: .).",
    )
    parser.add_argument(
        "--agent",
        choices=("auto", "claude", "cursor", "agents", "codex", "gemini", "all", "none"),
        default="auto",
        help="Which agent integration files to write (default: auto-detect).",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Remove only files recorded in .premium-taste/.install-manifest.json.",
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


def remember(actions: list[str], managed: list[str], target: Path, path: Path, content: str, dry_run: bool) -> None:
    actions.append(write_text(path, content, dry_run))
    managed.append(path.resolve().relative_to(target.resolve()).as_posix())


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    target = args.target.resolve()

    if inside_repo(target):
        print("Target cannot be the Premium Taste repo or one of its subdirectories.", file=sys.stderr)
        return 1

    try:
        if args.uninstall:
            actions = uninstall(target, args.dry_run)
            prefix = "[dry-run] " if args.dry_run else ""
            print(f"{prefix}Uninstalled Premium Taste from {target}:")
            for line in actions:
                print(f"  - {line}")
            return 0

        if not target.exists():
            if args.dry_run:
                print(f"would create directory {target}")
            else:
                target.mkdir(parents=True, exist_ok=True)

        actions, managed = copy_core(target, args.dry_run)

        if args.agent == "none":
            selected: set[str] = set()
        elif args.agent == "all":
            selected = {"claude", "cursor", "agents", "codex", "gemini"}
        elif args.agent == "auto":
            selected = detect_agents(target)
        else:
            selected = {args.agent}

        if "claude" in selected:
            remember(actions, managed, target, target / ".claude" / "skills" / "critique-ui" / "SKILL.md", CLAUDE_SKILL, args.dry_run)
        if "cursor" in selected:
            remember(actions, managed, target, target / ".cursor" / "rules" / "premium-taste.mdc", CURSOR_RULE, args.dry_run)
        if "agents" in selected or "codex" in selected:
            remember(actions, managed, target, target / ".agents" / "skills" / "premium-taste" / "SKILL.md", AGENT_SKILL, args.dry_run)
        if "codex" in selected:
            remember(actions, managed, target, target / ".codex" / "skills" / "critique-ui" / "SKILL.md", AGENT_SKILL, args.dry_run)
        if "gemini" in selected:
            remember(
                actions,
                managed,
                target,
                target / ".gemini" / "extensions" / "premium-taste" / "gemini-extension.json",
                GEMINI_EXTENSION,
                args.dry_run,
            )

        if not args.no_agents_md and args.agent != "none":
            agents_file = target / "AGENTS.md"
            created_agents = not agents_file.exists()
            note = update_agents_md(target, args.dry_run)
            if note:
                actions.append(note)
                if created_agents:
                    managed.append("AGENTS.md")

        if args.mcp:
            mcp_file = target / ".mcp.json"
            created_mcp = not mcp_file.exists()
            actions.append(update_mcp_json(target, args.dry_run))
            if created_mcp:
                managed.append(".mcp.json")

        manifest_rel = ".premium-taste/.install-manifest.json"
        managed.append(manifest_rel)
        manifest = {"version": INSTALL_VERSION, "files": sorted(set(managed))}
        actions.append(
            write_text(
                target / manifest_rel,
                json.dumps(manifest, indent=2) + "\n",
                args.dry_run,
            )
        )
    except InstallError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    prefix = "[dry-run] " if args.dry_run else ""
    print(f"{prefix}Installed Premium Taste in {target}:")
    for line in actions:
        print(f"  - {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
