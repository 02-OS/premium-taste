---
id: destructive-confirmation
title: Destructive Action Confirmation & Recovery
type: flow
directions:
  - precise-technical
  - quiet-luxury
job: verify blast radius before irreversible deletion or revocation
tags:
  - delete
  - confirmation
  - modal
  - undo
  - safety
---

# Destructive Action Confirmation & Recovery

Prevent accidental irreversible loss without fatiguing operators with warning theater on trivial actions.

## Layout & Hierarchy

- For **reversible** removals (archiving, removing a tag, soft deleting a draft), execute immediately without a modal and present a polite toast (`role="status"`, `aria-live="polite"`) with an inline **`Undo`** action.
- Reserve confirmation dialogs for **irreversible** or cascading mutations (deleting a workspace, revoking an active API key, dropping a production database).
- Inside the modal, state the exact **target identifier** (`Delete cluster prod-eu-01?`) and the exact blast radius (`Revokes 4 tokens and stops 12 cron schedules immediately`).

## Required States & Mechanics

- **Focus safety:** Focus `Cancel` (or a neutral input) on dialog open—never pre-focus the red `Delete` confirm button; restore focus to the trigger control on Escape/Cancel.
- **High-risk friction:** For production resources, require typing the exact resource slug (`prod-eu-01`) with `autocomplete="off"` inside a visible labeled field before enabling the `danger` confirm button.
- Show an explicit in-flight state (`Deleting...`, disabled close actions) and route cleanly back to the parent index upon completion with a confirmation status line.

## What to Include

- Specific verb on the destructive button (`Revoke key`, `Delete workspace`) rather than ambiguous `Confirm` or `Yes` (`a11y.names`).
- `overscroll-behavior: contain` on the modal container so scrolling the dialog never scrolls the backdrop page.

## What to Refuse

- Modal confirmation prompts for non-destructive toggles (`"Are you sure you want to log out?"`).
- Vague boilerplate warnings (`"This action cannot be undone. Are you sure?"`) with no object name or consequence count.
- Placing two identical bright filled buttons side by side without separating safe dismissal (`chrome.two-primaries`).

## Litmus Check

- Triggering a deletion with Enter or accidental Spacebar cannot destroy a production record, and `Cancel` returns focus exactly to where the user pressed Delete.
