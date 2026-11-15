# Prompts

Paste these in front of a task. Point the agent at this repo first. The prompts tell it which file to load. They do not restate the principles.

## Quick prompt (simplest start)

```
Use Premium Taste (`AGENTS.md` in this repo or https://github.com/02-OS/premium-taste).
Follow its load order: pick one direction and one matching reference, build the screen without generic SaaS skeletons or default palettes, then critique and revise with `skills/critique-ui/SKILL.md`.

Screen job: [one sentence with a verb, e.g. "let a developer inspect failed builds"]
Real content: [names, prices, numbers, states]
```

## Generate a screen (explicit)

```
Read AGENTS.md in the Premium Taste repo and follow its load order.

This screen is a [job] for [who].
Direction: look up the closest one in taste/directions.yaml. Do not blend directions.
Load one reference from taste/references/index.yaml whose job is close to this screen.
Steal the structural decision named in that file. Do not copy its palette or its font.

Content you must use, and must not invent past:
- [real nouns, prices, names, states]

Then run skills/critique-ui/SKILL.md on your result and apply the required changes.
Output the critique template before the code, and cite rule ids.
```

## Critique something that already exists

```
Follow skills/critique-ui/SKILL.md from the Premium Taste repo.
The artifact is [file or description].
The job of this screen is [verb phrase].
Score the six dimensions. Cite ids from taste/principles.yaml and taste/anti-patterns.yaml.
At most seven required changes. Each one names the element, the current decision, and the replacement.
Do not add features. Do not restyle the same skeleton with a different font.
If uniqueness is 2 or below, the first change is structural.
```

## The agent is about to theme a template

```
Stop. The layout is still skeleton.saas-landing (or layout.dashboard-costume).
Changing the font, the primary color, or the dark mode does not pass uniqueness.diverge-from-reference.
Read the first_screen for [direction] in taste/directions.yaml.
Rebuild the first viewport from that recipe, using only the content in [file].
Then run the critique.
```

## The product already has a brand

```
Read the product DESIGN.md for color and type families. Those win.
Read taste/principles.yaml for hierarchy, spacing, restraint, and accessibility. Those win over the brand file when the brand file is silent.
Refuse anti-patterns in taste/anti-patterns.yaml even if a previous page in the product used them, and say which id you refused.
Do not load Premium Taste's tokens/*.DESIGN.md. Those are sample identities for products with no guide.
```

## Add a reference

```
Read taste/references/README.md and taste/references/_template.md.
Draft taste/references/[id].md for [product], only from public material you can point at.
Set confidence to medium if you did not measure the screen.
Fill "What not to copy".
Add the row to taste/references/index.yaml.
Run python3 scripts/check_catalog.py.
Do not add tokens for it in this change.
```

---

## Audit existing code prompt

```text
Run `python3 scripts/audit.py <path-to-ui-files>` (and `python3 scripts/critique_url.py <local-url>` if running a dev server).
Fix every structural, layout, contrast, focus, and copy violation flagged before polishing colors, then re-run until exit code 0.
```
