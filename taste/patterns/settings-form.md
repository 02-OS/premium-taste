---
id: settings-form
title: Ruled Configuration & Workspace Settings
type: screen
directions:
  - precise-technical
  - editorial-print
job: configure account or workspace preferences without lost edits
tags:
  - settings
  - form
  - validation
  - save-bar
  - hairlines
---

# Ruled Configuration & Workspace Settings

Organize long configuration surfaces with clear typographic sections, 1px horizontal hairlines, persistent field labels, and unambiguous save feedback.

## Layout & Hierarchy

- Cap form field measure around `42ch–56ch` even on wide displays (`spacing.measure`); use a two-column split (`section title + 1-line summary` on the left `~240px`, controls stacked on the right) separated by `1px` hairlines instead of boxing every setting in a drop-shadowed card (`material.hairline-before-box`).
- Always place visible `<label for="...">` directly above each input; put helper descriptions beneath the input (wired with `aria-describedby`), never solely inside placeholder text (`a11y.placeholder-label`).
- Isolate irreversible danger settings (`Transfer ownership`, `Delete workspace`) in a clearly separated final hairline block at the bottom.

## Required States & Mechanics

- Dirty-state clarity: when per-section saving exists, keep `Save changes` clear per group; for full-page forms, show an explicit inline or sticky unsaved bar (`Unsaved changes` + `Discard` link + `Save settings` primary button) only when dirty.
- Never block paste (`onPaste` preventDefault), set `autocomplete` attributes (`email`, `organization`, `url`), and set `inputmode="numeric"` for ports/billing IDs.
- Validate cleanly at each field on blur/submit with `aria-invalid="true"` and concrete fix instructions (`"Must be a valid HTTPS origin without trailing slash"`).

## What to Include

- Unambiguous read-only values formatted in tabular monospace with explicit 1-click Copy confirmation (`Workspace ID`, `Webhook Secret`) announcing `"Copied"` politely.
- Exact role/permission warning when a field is locked by org admin (`Read-only: managed by Okta SAML`).

## What to Refuse

- Stacking five identical shadow-bordered cards down the settings route (`material.gray-card-shadow`).
- Silent autosave with no status indicator alongside explicit Save buttons (mixing both models creates ambiguity).
- Using green/accent toggle switches without state text when context needs explicit On/Off guarantees.

## Litmus Check

- Every input has an always-visible label and `2px` `:focus-visible` ring, Tab navigates strictly in visual section order, and invalid edits pinpoint the exact field without erasing neighboring inputs.
