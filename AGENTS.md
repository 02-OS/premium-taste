# AGENTS.md — Premium Taste

You are using Premium Taste, a stack-agnostic taste layer. It teaches judgment. It does not give you a component kit, and it does not license one look.

Load the smallest set of files that can change the screen in front of you.

## Load order

1. Read this file.
2. Read `taste/index.yaml` if you need the map. Skip it when you already know the paths below.
3. Name the job of **this screen** in one sentence. A job is a user outcome: "reserve a bowl from this firing", "see which revision failed", "read the essay". "Look premium" is not a job.
4. Pick **one** direction in `taste/directions.yaml`. Use the `choose` block. If two could fit, pick the job of this screen, not the brand's mood.
5. Read that direction's entry, then **one** reference from `taste/references/` whose `job` is close to this screen. Get the filename from `taste/references/index.yaml`. Do not read the whole gallery.
6. Generate from the structural idea in the reference (what the page *is*), not from its palette.
7. Run `skills/critique-ui/SKILL.md` on the result. Revise structure before you revise color.
8. If the product has no brand guide, you may apply the sample identity for the direction you chose: `tokens/quiet-luxury.DESIGN.md`, `tokens/cinematic-dark.DESIGN.md`, `tokens/precise-technical.DESIGN.md`, or `tokens/editorial-print.DESIGN.md`. Those files are sample identities, not the system.

When you need the reasoning, read `taste/principles.md`. When you need a pass/fail check, read `taste/principles.yaml` and `taste/anti-patterns.yaml`. Cite rule ids in the critique (`hierarchy.one-primary-action`, `skeleton.saas-landing`).

## Precedence

1. The user's explicit instruction, and the product's real content.
2. The product's own `DESIGN.md` or brand guide, for **color and type families**.
3. `taste/principles.yaml`, for hierarchy, spacing, density, restraint, motion, accessibility, and refusing generic skeletons.
4. The one reference you loaded, for structure and material.

If the brand guide itself is the generic skeleton (gradient hero, three icon cards, indigo on Inter), follow the user's explicit ask and still remove every habit they did not ask for. Say what you removed.

A reference is evidence of a decision. Hex values and font names inside references are observations, sometimes from public captures. Do not paste them into an unrelated product. Steal the decision named under "What to steal".

## What a good pass looks like

- The first screen can be described without saying "modern" or "clean".
- A stranger can point at the primary action.
- Repeated things share a rhythm. The section gap is obviously larger than the item gap.
- Color has one temperature. The accent is rare enough to count on one hand.
- Type has at most two families and real size jumps.
- The layout would still have an idea if you removed the color.
- Text is specific. It does not say Elevate, Unlock, Seamless, or Next-gen.
- Focus, labels, contrast, and reduced motion still work.
- The screen does not match `skeleton.saas-landing` or `layout.dashboard-costume` unless the product is actually a marketing landing or a monitoring tool, and even then it has its own structure.

## What you refuse, even as a "quick polish"

These are named in `taste/anti-patterns.yaml`. The ones agents reach for while "improving" a page:

- A purple-blue mesh, gradient text, or a glow behind a card.
- Inter, Geist, Space Grotesk, Satoshi, or Instrument Serif used as a costume on the default skeleton.
- Gold rules and a high-contrast Didot on pure black, as a shortcut for luxury.
- Three equal cards with an icon in a tinted square.
- A bento of marketing sentences.
- Sidebar, four stat cards, a chart, and a table, for a product that is not monitoring.
- Staggered fade-up on load. Cards that lift and shadow on hover.
- A second filled button. A pile of New / AI / Pro badges. A sparkle icon as the concept.

Replacing Inter with Newsreader on the same skeleton is not a revision. Change what the page is, then set type.

## Directions

| Id | Use when this screen is… | Do not use when… |
| --- | --- | --- |
| `quiet-luxury` | an object, a room, a slow brand, a physical good | the user is scanning dense, repeating data |
| `cinematic-dark` | a dark room for images, film, music, or night culture | you only wanted a dark theme for a form |
| `precise-technical` | a tool for repeated decisions, data, or configuration | you wanted the page to feel like an object on a table |
| `editorial-print` | a long text, a story, a catalog essay, a spread | the user is operating a control |

## Files agents write against

- `taste/principles.md` — why a choice looks finished or cheap. Read for a new surface.
- `taste/principles.yaml` — the same rules as tests. Grep an id.
- `taste/anti-patterns.yaml` — named failures with visible signals.
- `taste/directions.yaml` — how to choose, and the first-screen recipe.
- `taste/references/index.yaml` — retrieval. Filter on `direction` and `job`.
- `skills/critique-ui/SKILL.md` — the revise loop. Output its template.
- `tokens/*.DESIGN.md` — optional example tokens in the Google Labs DESIGN.md format (`version: alpha`).
- `examples/before-after.md` — a worked critique. Fictional products only.

## MCP

`scripts/mcp_server.py` (version 1.1.0) exposes the catalog over stdio JSON-RPC. Tools: `pick_direction`, `get_reference`, `get_pattern`, `get_tokens`, `audit_ui`, `verify_url`. Resources use `premium-taste://` URIs such as `premium-taste://taste/principles.yaml`. Prompts: `critique-ui` and `choose-direction`.

## Stack

Principles are stack-agnostic. Implement them in whatever the repo uses. Map space to the local scale, type to the local styles, color to the local tokens. Do not add a component framework so you can follow this system. Do not invent a parallel set of token names in the product when it already has one.

If the repo has no tokens and you are building a new surface in one of the example directions, start from the matching `tokens/*.DESIGN.md` and then diverge as soon as the product has a real material (a photograph, a dataset, a place).

## Extending

Humans add references and rules. Agents may propose an addition when a real product taught a decision this gallery lacks. The procedure is in the root `README.md`. Do not add a reference you cannot describe from public material, and do not add a rule that only restates "make it clean".
