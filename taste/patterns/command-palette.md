---
id: command-palette
title: Keyboard Command Palette & Quick Jump
type: screen
directions:
  - precise-technical
  - cinematic-dark
job: jump directly to records, routes, or actions from the keyboard
tags:
  - command
  - search
  - keyboard
  - shortcuts
  - overlay
---

# Keyboard Command Palette & Quick Jump

Serve power users sub-second navigation and action dispatch with zero pointer travel.

## Layout & Hierarchy

- Present one centered modal overlay (`surface-raised` with a single `1px` hairline or border and one tight overlay shadow, zero outer gradient glow).
- Open straight onto an auto-focused borderless/hairline search field (`role="combobox"`, `aria-expanded="true"`, `aria-controls`), immediately showing grouped recent items or primary commands before the user finishes typing.
- Align action label on the left and subtle category (`Settings`, `Build`) + crisp `kbd` shortcut caps on the right (`tabular-nums`, `IBM Plex Mono`).

## Required States & Mechanics

- Bind `Cmd+K` / `Ctrl+K` globally (when not conflicting with explicit text editor chords) and `Esc` to close while returning focus to the triggering element or last focusable control.
- Full Arrow Up/Down cycling (`aria-activedescendant`), Enter to execute, and nested prefix scoping (`>` commands, `/` routes, `#` records) indicated via clear chip/prefix state inside the search bar—not nested popovers.
- Empty query search state must distinguish `"No commands match 'zqx'"` and preserve instant clearing with Backspace.

## What to Include

- Subtle 1-line keyboard footer (`↑↓ Navigate · ↵ Open · Esc Close`) so shortcuts remain discoverable without cluttering rows.
- Exact match substring emphasis via ink contrast/weight rather than noisy background pills.

## What to Refuse

- Making the command palette the *only* navigation when primary app views lack visible semantic links (`a11y.names`, `hierarchy.first-screen`).
- Floating decorative blur over unreadable background contrast (`material.glass-on-flat`).
- Truncating long record paths without preserving trailing file/service names.

## Litmus Check

- Opening with `Cmd/Ctrl+K`, typing 3 letters, pressing Down twice, and hitting Enter completes the target jump without touching a mouse, and `Esc` cleanly restores focus.
