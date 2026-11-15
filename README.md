# Premium Taste

An open taste layer for AI coding agents. It teaches why a screen looks finished or cheap, and it gives them a way to critique their own output.

The core is judgment. Principles, a small gallery of annotated products, and a critique loop. Not a component library, and not one visual style to apply everywhere.

Agents that follow it should make interfaces that are specific to the product in front of them. A bowl, a film, a revision list, and an essay do not share a layout. They can share a standard: one idea, a real hierarchy, restrained color, type with a job, and text someone can read.

## Use it in 30 seconds

**Option 1 — Paste one prompt (no setup):**

```text
Read AGENTS.md at https://github.com/02-OS/premium-taste and follow its load order.
Pick one direction and one reference for this screen, refuse generic SaaS skeletons,
then run skills/critique-ui/SKILL.md and fix structure before color.

Job of this screen: [one sentence with a verb]
```

**Option 2 — Install into your project (1 command, no manual clone):**

```sh
curl -fsSL https://raw.githubusercontent.com/02-OS/premium-taste/master/install.sh | bash -s -- . --agent all --mcp
```

Or run the Python installer from a local checkout:

```sh
python3 /tmp/premium-taste/scripts/install.py /path/to/your-app --agent all --mcp
```

**Option 3 — Run deterministic audits locally:**

```sh
python3 scripts/audit.py src/                         # static rules on HTML/CSS/JSX/TSX
python3 scripts/critique_url.py http://localhost:4173/ # live Chromium contrast & layout check
```

That copies the judgment files into `.premium-taste/` inside your project and writes a lightweight pointer for Claude Code (`.claude/skills/critique-ui/SKILL.md`), Cursor (`.cursor/rules/premium-taste.mdc`), Codex (`.codex/skills/critique-ui/SKILL.md`), Gemini (`.gemini/extensions/premium-taste/gemini-extension.json`), or other agents (`.agents/skills/premium-taste/SKILL.md` and `AGENTS.md`). `--agent all` includes claude, cursor, agents, codex, and gemini. Flags may come before the target path. Pass `--dry-run` to preview.

## MCP

`python3 scripts/mcp_server.py` is a stdlib JSON-RPC 2.0 server on stdio. It accepts newline JSON and Content-Length framing. Server version 1.1.0.

Tools: `pick_direction`, `get_reference`, `get_pattern`, `get_tokens`, `audit_ui`, `verify_url`.

Resources use a `premium-taste://` URI plus a path in this repo, for example `premium-taste://taste/principles.yaml`. Prompts: `critique-ui` and `choose-direction`.

## How an agent should use it

Start at [AGENTS.md](AGENTS.md). The short version:

1. Name the job of this screen in one sentence with a verb.
2. Pick one direction in [taste/directions.yaml](taste/directions.yaml).
3. Load one reference from [taste/references/index.yaml](taste/references/index.yaml). Steal a structure, not a palette.
4. Generate.
5. Run [skills/critique-ui/SKILL.md](skills/critique-ui/SKILL.md). Change the structure before the colors.

Claude Code also reads [CLAUDE.md](CLAUDE.md), which points here. Other agents (Cursor, Codex, Grok, and the rest) can be pointed at `AGENTS.md` and the skill file. Do not paste the principles into a host rule file. Link them, so a rule has one home.

If the product already has a `DESIGN.md` or a brand guide, that file wins on color and type families. Premium Taste still wins on hierarchy, spacing, restraint, accessibility, and refusing generic skeletons.

## Directions

| Id | The screen is… |
| --- | --- |
| `quiet-luxury` | an object, a place, a slow brand |
| `cinematic-dark` | a room for images, film, music, or night culture |
| `precise-technical` | a tool for repeated decisions, data, or documents |
| `editorial-print` | a long text, a story, a spread |

Cinematic dark is not a dark theme switch. Quiet luxury is not a serif and a large margin on the same old page. The direction changes what the page *is*. Recipes for the first screen are in `taste/directions.yaml`.

## What's in the repo

```
AGENTS.md                 load order and precedence
CLAUDE.md                 pointer for Claude Code
taste/principles.md       the judgment, with a rule id on every test
taste/principles.yaml     the same ids, as checks
taste/anti-patterns.yaml  named cheap and generic patterns
taste/directions.yaml     how to choose a direction
taste/references/         annotated gallery and an index
skills/critique-ui/SKILL.md  generate → critique → revise
tokens/                   four example DESIGN.md identities
examples/                 a negative specimen, two afters, prompts
site/                     interactive workbench, live auditor, token contrast studio, and catalog explorer
install.sh                zero-clone installer; flags may precede the target
scripts/audit.py          deterministic static UI rule checker (HTML, CSS, JSX, TSX, Vue, Svelte, Astro)
scripts/critique_url.py   live Chromium CDP / HTTP fallback URL critique (contrast, fonts, overflow)
scripts/mcp_server.py     stdlib JSON-RPC 2.0 MCP server (six tools, resources, prompts)
scripts/check_catalog.py   ids and files still match
scripts/install.py         install into another project and register agent rules / .mcp.json
scripts/build_site_data.py sync site/data.js from taste/ and tokens/
```

Sample tokens for each direction live in `tokens/` and use the [DESIGN.md](https://github.com/google-labs-code/design.md) format. Load the one that matches the direction you chose, and only when the product has no guide of its own. They are examples of a direction, not the system.

## Site

[site/index.html](site/index.html) is the self-contained guide and interactive prompt builder for this repo. It follows `precise-technical`, the Stripe Docs structure, and the Instrument tokens. Serve `site/` directly with any static HTTP server (for example, `python3 -m http.server 4173 --directory site`). If you edit `taste/` or `tokens/`, regenerate its data with `python3 scripts/build_site_data.py`.

## Examples

- [examples/before-after.md](examples/before-after.md) walks a critique of a generic landing and the two screens that replace that kind of thinking.
- [examples/rowan-before.html](examples/rowan-before.html) is a **negative specimen**. It is the generic skeleton, labeled as such. Do not reuse it.
- [examples/rowan-after.html](examples/rowan-after.html) is a quiet object page for a fictional ceramics studio.
- [examples/harbor-after.html](examples/harbor-after.html) is a revision list. The filter works in the browser.
- [examples/prompts.md](examples/prompts.md) has prompts you can paste in front of a task.

Rowan and Harbor are not real products and do not belong in the gallery.

## How to extend it

**Add a reference** when a real public product teaches a decision the gallery lacks.

1. Copy [taste/references/_template.md](taste/references/_template.md) to `taste/references/<id>.md`.
2. Write only what you can support. Set `confidence: medium` when you are describing long-standing character rather than a measured capture.
3. Fill "What not to copy". A reference without a refusal becomes a costume.
4. Add the row to [taste/references/index.yaml](taste/references/index.yaml) and list the id under one direction in `taste/directions.yaml`.
5. Run `python3 scripts/check_catalog.py`.

The procedure and the current gaps are in [taste/references/README.md](taste/references/README.md).

**Add a rule** when you can name a test and a fix, not when you want to say "make it cleaner."

1. Add the prose, with the id as a `### \`id.name\`` heading, to `taste/principles.md`.
2. Add the same id to `taste/principles.yaml` with `rule`, `test`, and `fix`.
3. If it is a named failure rather than a positive test, add it to `taste/anti-patterns.yaml` and to the catalog table in the principles.
4. Run the catalog check. Every id has to appear in both places.

Do not add a component, a React kit, or a new token file to make a principle easier to apply. Map the rule onto whatever the host project already uses.

## Status

v1 judgment, with a gallery of 18. The target range is 15–25. Each direction has at least three references and a sample token file in `tokens/`.

Principles are written for Latin-script UI. Hierarchy, proximity, contrast, and restraint still apply to other writing systems. Tracking and case rules do not.

## License

[MIT](LICENSE). The products named in the gallery are other people's work. This repo annotates public design decisions. It does not ship their fonts, photographs, or trademarks, and it does not grant you those.
