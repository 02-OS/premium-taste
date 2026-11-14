---
version: alpha
name: Warm Paper
description: >
  Example identity for the quiet-luxury direction. Not a brand, and not a
  copy of any reference. Use it only when the product has no guide of its own,
  then diverge as soon as the product has a real material.
colors:
  surface: "#f3efe6"
  surface-raised: "#f7f4ee"
  ink: "#1c1915"
  ink-muted: "#5c564c"
  hairline: "#ddd4c6"
  accent: "#7a3e2e"
  on-accent: "#f6f1e8"
  danger: "#8d2f2f"
typography:
  display:
    fontFamily: "Newsreader, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 40px
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: -0.015em
  title:
    fontFamily: "Newsreader, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 28px
    fontWeight: 400
    lineHeight: 1.2
  body:
    fontFamily: "Public Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  ui:
    fontFamily: "Public Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
  kicker:
    fontFamily: "Public Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: 0.06em
  meta:
    fontFamily: "Public Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.4
rounded:
  none: 0px
  hairline: 2px
spacing:
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 48px
  2xl: 80px
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.none}"
    height: 44px
    paddingInline: 16px
  button-quiet:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
  field:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    rounded: "{rounded.none}"
    height: 44px
---

## Overview

Warm Paper is a sample identity for a page whose subject is an object or a place. The surface is a warm sheet. Ink is soft black. A serif speaks only for names and titles. A grotesk does the rest. The accent is an oxide red reserved for a detail in the object or for a destructive state, not for the button.

This file follows the DESIGN.md format so an agent that already knows that spec can read the tokens. Premium Taste's judgment still lives in `taste/principles.md`. If these tokens and the principles disagree, follow the principles.

Open substitutes: Newsreader and Public Sans, both widely available under the SIL Open Font License. Do not swap in Playfair Display, Cormorant, or Instrument Serif.

## Colors

`surface` is the page. It is paper, not screen white.

`ink` is text, the wordmark, the primary button, and the focus ring. `ink-muted` is captions and secondary facts. It is darkened enough to clear 4.5:1 on `surface`. Do not "soften" it further.

`hairline` separates a definition list or a footer. It is mixed from the paper and the ink, so it stays warm.

`accent` is oxide. Use it once: a glaze line, a sold-out word, an error. `on-accent` is the paper-tinted text if the accent ever becomes a small filled mark. `danger` is for a real error and is not the accent.

## Typography

`display` and `title` are Newsreader at regular weight. Large sizes do not go bold. `display` is for the subject of the page, once. `title` is for a section.

`body` is Public Sans at 16px. Keep a measure near 65 characters. `ui` is navigation and buttons. `meta` is captions.

`kicker` is the only tracked style, and only one kicker may appear on a screen. If you do not need it, do not use it. Do not set form labels in `kicker`.

## Layout

Page margin is at least 32px and grows with the viewport (around 6vw), up to a content width near 1120px. A spread is two columns: a large still, then a narrow text column, with a gap of `2xl` or `xl`. Section gaps are `2xl`. Inside the text column, the title sits `md` or `lg` above the body. A label sits `xs` above its field.

The column starts at the same edge as the body under it. Do not center the stack.

On a narrow viewport, the still comes first, then the column, and the section gap may drop to `xl`. The type sizes stay.

## Elevation & Depth

Flat. `surface-raised` is a menu or a dialog only, one step warmer and lighter than the page, with a `hairline` border. No shadow on the product column, the still, or the button. If a dialog must float, one soft shadow tinted toward `ink` at low opacity is the entire elevation system.

## Shapes

Square. `rounded.none` is the default for buttons, fields, and images. `rounded.hairline` (2px) is allowed on a control if a platform demands it. Do not round the still into a large squircle.

## Components

`button-primary` is ink on paper, square, used when the action has to be found in a busy bar. On a quiet object page, prefer `button-quiet`: ink text, an underline, no fill. One of them per view, not both as equals.

`field` is a square box with a hairline and a visible label above it in `ui`. Placeholder text is not the label.

A product fact list is not a component with a fill. It is `dt`/`dd` pairs separated by `hairline`.

## Do's and Don'ts

- Do let the photograph or the object be the warmest thing on the page.
- Do keep headlines at regular weight.
- Do leave a wide margin rather than stretch the paragraph.
- Don't put `accent` on the button, the links, and the icons.
- Don't add a shadow stack, a gradient mesh, or a second display family.
- Don't set body text below 14px. The reference gallery includes smaller print-like sizes. Those stay in print.
- Don't center the column under a centered headline with two buttons.
