---
name: premium-taste
description: >
  Make UI look and read like a deliberate product instead of generic AI output.
  Use before creating, redesigning, or reviewing any screen, landing page,
  dashboard, pricing table, form, or empty/error flow. Guides direction choice,
  structural reference selection, screen/flow pattern contracts, W3C/DESIGN.md
  tokens, Decision Ledger verification, and deterministic static/browser UI audits.
---

# Premium Taste

Premium Taste is a taste benchmark and deterministic verification system for coding agents. It prevents calm-editorial homogenization (`Inter`, cream gradient cards, sparkle icons, hairline weights, three identical cards) and forces structural product fit.

## Required Execution Loop

Read [AGENTS.md](../../AGENTS.md) and follow this sequence strictly:

1. **Name the job** in one sentence with a concrete verb (`compare pricing plans`, `read API reference`, `triage deployment errors`).
2. **Record the Design Decision Ledger (4 lines + 1 risk) before writing UI**:
   - `Direction`: Pick **1** from `taste/directions.yaml` (`quiet-luxury`, `cinematic-dark`, `precise-technical`, `editorial-print`). Refuse `anti-calming` / `anti-averaging` mixes (never blend Dark Room with Warm Paper).
   - `Reference`: Load **1** matching brand in `taste/references/index.yaml`. Steal its spatial layout and density, not its fonts or logo colors.
   - `Pattern`: If the screen matches a recurring layout or journey in `taste/patterns/index.yaml`, load **1** pattern (e.g., `pricing-table`, `empty-state`, `data-table-filters`, `onboarding-checklist`, `billing-cancellation`).
   - `Rule at risk`: Name **1** principle or anti-pattern most likely to fail if rushed (e.g., `type.numbers`, `chrome.one-primary`, `type.no-hairline-body`).
3. **Load tokens only if needed**: If the project lacks its own brand guide, read the matching `tokens/<direction>.DESIGN.md` pack (Respect Open Substitutes and the Scale/Surface `0..3` discipline—never use font weights `<300` at body/nav sizes `<=18px`).
4. **Generate cohesive screens**: Real media or honest empty states—never invent colorful fake preview thumbnails (`uniqueness.media-preservation`). Semantic HTML landmarks and real `<button>`/`<a>` elements (`a11y.semantics`). Zero invented metrics or buzzwords.
5. **Audit & critique against the Visual Target Gate**:
   - Run static lint: `python3 scripts/audit.py <changed-files>` (zero findings target).
   - Inspect live desktop (`1280px`) and mobile (`375px`) via `python3 scripts/critique_url.py <url>` when a local server is running.
   - Run the critique checklist in [skills/critique-ui/SKILL.md](../critique-ui/SKILL.md) and fix structure (hierarchy, measure, count) before color.

## Quick Reference Map

- **Principles (68 rules) & Anti-patterns (30 tells)**: `taste/principles.md`, `taste/principles.yaml`, `taste/anti-patterns.yaml`
- **4 Aesthetic Directions**: `taste/directions.yaml`
- **18 Brand References**: `taste/references/index.yaml`
- **12 Screen & Flow Patterns**: `taste/patterns/index.yaml`
- **4 Extended DESIGN.md Token Packs**: `tokens/*.DESIGN.md`
- **MCP Server (6 tools: `pick_direction`, `get_reference`, `get_pattern`, `get_tokens`, `audit_ui`, `verify_url`)**: `python3 scripts/mcp_server.py`
