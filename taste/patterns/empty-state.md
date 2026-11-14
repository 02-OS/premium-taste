---
id: empty-state
title: First-Run & Zero-Data Empty State
type: screen
directions:
  - precise-technical
  - quiet-luxury
  - cinematic-dark
job: understand why this list is empty and create the first real record
tags:
  - empty
  - zero-state
  - onboarding
  - first-run
---

# First-Run & Zero-Data Empty State

Distinguish clearly between **never created**, **cleared by search/filters**, and **lacking permission**, and hand the user one concrete step out.

## Layout & Hierarchy

- Render the empty message **inside the real destination shell** (table header, sidebar navigation, or gallery canvas already visible) so the user understands what will live here once populated.
- Keep copy to two concise blocks: state what is missing (`"No deployment webhooks configured for staging"`), and explain what the primary action creates.
- Place at most **one** filled action button (`Add webhook`); pair an optional template/sample import as a quiet secondary link beside it.

## Required States & Mechanics

- **Zero records vs zero search hits:** When filters hide items, never show the first-run welcome message—show `"No runs match status:failed"` with a one-click `Clear 2 filters` action.
- **No permissions:** Explain which role grants access instead of offering a broken Create button.
- Preserve keyboard focus cleanly when transitioning from empty state into inline creation or a modal drawer.

## What to Include

- One honest example or structural preview (for tools, a pre-filled starter snippet or 1-click CLI command; for content apps, one crisp line describing the artifact).
- Exact copy for the empty reason instead of cute metaphors (`"Nothing here yet!"`).

## What to Refuse

- Floating cartoon blobs, generic sparkle icons (`chrome.sparkle`), or oversized illustrations pushing the button off screen (`material.fake-media`).
- Multi-card tutorial carousels blocking a single empty collection.

## Litmus Check

- Temporarily hiding all filters vs removing all database rows shows two distinctly helpful messages, each pointing at one concrete fix.
