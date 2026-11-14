---
name: critique-ui
description: >
  Critique an interface against Premium Taste and return specific revisions.
  Use after generating any UI, when the user asks to review or refine a screen,
  or when a result looks generic. Works in any agent that can read a markdown
  skill. Cite rule ids from taste/principles.yaml. Do not restate the principles
  as the critique.
---

# Critique UI

A critique is a list of edits. It is not a mood, and it is not a second design essay.

The judgment lives in `taste/principles.yaml` (tests) and `taste/principles.md` (reasons). Failures you should name exactly live in `taste/anti-patterns.yaml`. Directions live in `taste/directions.yaml`. This file is only the procedure.

## When to run

- You just generated a screen, a page, or a component.
- The user asks for a review, a polish, or "make this less generic."
- You are about to restyle something by swapping the font or the primary color. Stop and run this first. A font swap on the same skeleton fails `uniqueness.diverge-from-reference`.

Do not run this on a non-visual change (a parser, a migration, a test). Do not expand the product while you critique it.

## What you need

- The artifact: markup, a component tree, or a description precise enough to point at elements.
- The job of this screen, in one sentence with a verb.
- One direction id.
- One reference id, already loaded, or "none yet" if you are about to pick one.
- One pattern id from `taste/patterns/index.yaml` when reviewing an interactive workflow (`pricing-table`, `data-table-filters`, `empty-state`, `destructive-confirmation`, `settings-form`, etc.), or "none".
- Visual Target Gate: what must not drift (`canvas surface`, `type roles`, `layout skeleton`, `accent role`, `media slot`).

If the job sentence uses "and" twice, that is the first finding (`hierarchy.one-job`). Do not score the rest until you name a single job or split the screen.

## Procedure

### 1. Name the structure & run the six litmus tests

Write one sentence: "This page is ___." If the sentence is a feature list, the finding is `uniqueness.one-idea` and the revision is structural. Cosmetic notes wait.

Check the first screen against `skeleton.saas-landing`, `layout.dashboard-costume`, and `uniqueness.calm-editorial-slop`. Then test the artifact against six quick gates:

- **Card test (`material.hairline-before-box`):** If removing border, radius, background, and shadow does not hurt understanding, delete the card.
- **Editorial test (`uniqueness.anti-calming`):** If replacing the product logo with a coffee shop or boutique hotel still makes the hero plausible, warm cream + serif is a costume.
- **Image test (`uniqueness.media-preservation`):** If an image slot works fine deleted—or uses a CSS gradient blob—make the subject dominant or drop photography altogether.
- **Copy test (`uniqueness.specific-copy`):** If deleting 30% of copy sharpens the page, keep deleting.
- **Brand/Identity test (`uniqueness.diverge-from-reference`):** Covering navigation chrome still leaves this product unmistakably distinguishable from another site in the same direction.
- **Anti-averaging test (`uniqueness.no-averaging`):** Sharp traits from the chosen direction (0px corners, dense row alignment, work-first dark room) were kept rather than softened into medium beige.

### 2. Score six dimensions

Score each from 1 to 5. A score without a cited id is not a score.

| Score | Meaning |
| --- | --- |
| 5 | The decision is deliberate and it serves the job. |
| 4 | Sound. Minor optical issues remain. |
| 3 | A template habit is visible beside a real decision. |
| 2 | A named anti-pattern dominates the dimension. |
| 1 | The generic skeleton, or the screen is hard to use. |

Dimensions and the ids to open first:

**Hierarchy.** Can a stranger point at the subject and the one action?

- `hierarchy.one-primary-action`
- `hierarchy.first-screen`
- `hierarchy.three-levels`
- `hierarchy.grayscale-test`
- `hierarchy.alignment`
- `hierarchy.center-is-ceremonial`

**Spacing.** Do groups read as groups, and is the section gap obvious?

- `spacing.proximity`
- `spacing.section-jump`
- `spacing.nested-padding`
- `spacing.measure`
- `spacing.scale`

**Uniqueness.** Is there one idea this product owns?

- `uniqueness.one-idea`
- `uniqueness.refuse-skeleton`
- `uniqueness.specific-copy`
- `uniqueness.one-detail`
- `uniqueness.diverge-from-reference`
- `content.abstract-verbs`
- `content.fake-proof`
- `chrome.sparkle`

**Restraint.** Did color, type, material, and motion stay inside a budget?

- `color.budget`
- `color.accent-rarity`
- `color.no-aurora`
- `color.temperature`
- `type.two-families`
- `type.avoid-tells`
- `material.one-system`
- `material.shadow-budget`
- `material.gray-card-shadow`
- `motion.no-load-theater`
- `motion.hover`

**Accessibility.** Can someone read it, tab it, and name the controls?

- `a11y.contrast`
- `a11y.focus`
- `a11y.targets`
- `a11y.size`
- `a11y.not-color-alone`
- `a11y.names`
- `a11y.errors`
- `color.contrast`

**Product fit.** Does this direction belong on this job?

- `product.sentence`
- `product.direction-serves-job`
- `product.two-registers`
- `density.match-job`

A dimension at 2 or below forces a structural change in the required list. Do not average a 2 away with a 5 somewhere else.

### 3. Write edits, not advice

Produce at most seven required changes, ordered by impact. Each change has all five lines:

- Element: which control, block, or region.
- Rule: an id from `principles.yaml` or `anti-patterns.yaml`.
- Now: the current decision, in concrete terms (alignment, count, color role, copy).
- Change: the replacement, specific enough to implement without another opinion. Name what you will delete.
- Leave: what you will not touch.

Forbidden findings, because they cannot be implemented:

- "Consider more whitespace."
- "Make it pop" or "make it more premium."
- "Add visual interest."
- "Use a better font" with no family and no role.
- A new feature the user did not ask for.

If the fix is "remove this," say what remains.

### 4. Refuse the usual repairs

List the anti-patterns you will not introduce while fixing. At minimum, check that your revision does not add:

- `color.aurora`, `color.gold-on-black`, `color.indigo-default`
- `material.icon-tile`, `material.glass-on-flat`, `material.gray-card-shadow`
- `motion.stagger-fade`, `motion.hover-lift`
- `chrome.two-primaries`, `chrome.badge-pile`, `chrome.sparkle`
- `type.avoid-tells` as the whole of the "fix"

### 5. Revise, then stop

If you are the agent who will edit the UI, apply the required changes in order. Structural changes first (what the page is), then spacing and type, then color.

Re-score. Stop when every dimension is 4 or 5, or after two revision passes. On the second stop, report the dimensions still below 4 and the rule that blocks them. Do not take a third lap unless the user asks. Further passes tend to decorate.

Do not raise a score because the revision "feels better." Re-run that dimension's tests.

## Output template

Use this shape. Omit a section only when it is empty.

```
Job:
Direction:
Reference:
Pattern:
Structure: This page is ___.

Decision Ledger
- Canvas & Surfaces: [step 0..3 / locked role]
- Type & Scale: [at most 2 families + ratios + tabular numerals]
- Media / Evidence: [photo / UI proof / SVG diagram role]
- Divergence: [what differs from reference to fit this product]

Scores
- Hierarchy: N — one sentence, with an id
- Spacing: N — one sentence, with an id
- Uniqueness: N — one sentence, with an id
- Restraint: N — one sentence, with an id
- Accessibility: N — one sentence, with an id
- Product fit: N — one sentence, with an id

Required changes
1. Element:
   Rule:
   Now:
   Change:
   Leave:

Refused while fixing
- id: why you will not use it here

Still failing after this pass
- dimension, id, what remains
```

## Worked shape

A failing uniqueness score sounds like this:

> Uniqueness: 2 — `skeleton.saas-landing`. The first screen is a centered headline ("Elevate your everyday rituals"), two filled buttons, and three icon tiles. `uniqueness.specific-copy` also fails.

The matching change sounds like this:

> Element: first viewport, including the three feature tiles.
> Rule: `uniqueness.refuse-skeleton`
> Now: centered hero and three icon cards.
> Change: delete the icon cards and the second button. One spread: a large still of the object, a 62ch column with a factual title, one paragraph, and a text action. Start edge aligned.
> Leave: the product name and the price.

A passing uniqueness score names the idea and the divergence:

> Uniqueness: 5 — `uniqueness.one-idea`. The page is the bowl and the facts of this firing. It takes Aesop's narrow factual column and does not take Aesop's catalog grid.

## Installing the skill elsewhere

Run `python3 scripts/install.py /path/to/your-project` to copy the core files into `.premium-taste/` and write lightweight pointer files for your coding agent, or wire them manually:

- Claude Code: copy this file to `.claude/skills/critique-ui/SKILL.md`, or rely on `CLAUDE.md` in this repo.
- Cursor: add a rule that says to follow `skills/critique-ui.md` before finishing UI work.
- Codex, Grok, and others: point the agent at this file plus `AGENTS.md`.

Do not paste the principles into the host agent's rule file. Link them, so the rules stay in one place.
