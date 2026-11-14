---
version: alpha
name: Warm Paper
direction: quiet-luxury
description: >
  Example identity for the quiet-luxury direction. Not a brand, and not a
  copy of any reference. Use it only when the product has no guide of its own,
  then diverge as soon as the product has a real material.
scale:
  name: Minor Third
  ratio: 1.2
  base: 16px
opentype:
  numeric: tabular-nums
  features: '"kern" 1, "liga" 1'
surfaces:
  step-0-canvas: "#f3efe6"
  step-1-raised: "#f7f4ee"
  step-2-subtle: "#eae4d8"
  step-3-inverted: "#1c1915"
colors:
  surface: "#f3efe6"
  surface-raised: "#f7f4ee"
  surface-subtle: "#eae4d8"
  ink: "#1c1915"
  ink-muted: "#5c564c"
  hairline: "#ddd4c6"
  line: "#8d8476"
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
    letterSpacing: -0.01em
  body:
    fontFamily: "Public Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: 0em
  ui:
    fontFamily: "Public Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0em
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
    letterSpacing: 0em
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
    borderColor: "{colors.line}"
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

`hairline` separates a definition list or a footer. It is mixed from the paper and the ink, so it stays warm. `line` clears 3:1 on `surface` and frames input controls.

`accent` is oxide. Use it once: a glaze line, a sold-out word, an error. `on-accent` is the paper-tinted text if the accent ever becomes a small filled mark. `danger` is for a real error and is not the accent.

## Surfaces

| Step | Token | Hex | Purpose |
| --- | --- | --- | --- |
| 0 | `surface` | `#f3efe6` | Primary warm paper canvas across sections |
| 1 | `surface-raised` | `#f7f4ee` | Dialogs, menus, and hovered swatch panels only |
| 2 | `surface-subtle` | `#eae4d8` | Image mattes and quiet recessed bands |
| 3 | `ink` | `#1c1915` | Inverted primary button fill and high-contrast footer bands |

## Typography

`display` and `title` are Newsreader at regular weight (`400`). Large sizes do not go bold. `display` is for the subject of the page, once. `title` is for a section.

`body` is Public Sans at 16px. Keep a measure near 65 characters. `ui` is navigation and buttons. `meta` is captions. Numeric tables and dimensions enable `font-variant-numeric: tabular-nums`.

`kicker` is the only tracked style (`+0.06em`), and only one kicker may appear on a screen. If you do not need it, do not use it. Do not set form labels in `kicker`.

## Type Scale Detail

| Role | Family | Size | Weight | Line Height | Letter Spacing |
| --- | --- | --- | --- | --- | --- |
| Display | Newsreader | 40px | 400 | 1.15 | -0.015em |
| Title | Newsreader | 28px | 400 | 1.20 | -0.01em |
| Body | Public Sans | 16px | 400 | 1.55 | 0em |
| UI | Public Sans | 14px | 400 | 1.40 | 0em |
| Kicker | Public Sans | 13px | 500 | 1.35 | 0.06em |
| Meta | Public Sans | 13px | 400 | 1.40 | 0em |

## Imagery

Natural daylight studio photography and tactile close-ups provide the warmth this chrome withholds. Place frames flush inside `#eae4d8` mattes or directly on `#f3efe6` with `0px` radius (`rounded.none`). Declare explicit `width` and `height`. Never invent warm cream boxes with pastel gradient blobs where object photography belongs.

## Layout

Page margin is at least 32px and grows with the viewport (around 6vw), up to a content width near 1120px. A spread is two columns: a large still, then a narrow text column, with a gap of `2xl` or `xl`. Section gaps are `2xl` (80px). Inside the text column, the title sits `md` or `lg` above the body. A label sits `xs` above its field.

The column starts at the same edge as the body under it. Do not center the stack. On a narrow viewport, the still comes first, then the column, and the section gap may drop to `xl`.

## Elevation & Depth

Flat. `surface-raised` (`#f7f4ee`) is a menu or a dialog only, one step lighter than the page, with a `hairline` border. No shadow on the product column, the still, or the button. If a dialog must float, one soft shadow tinted toward `ink` at low opacity is the entire elevation system.

## Shapes

Square. `rounded.none` (0px) is the default for buttons, fields, and images. `rounded.hairline` (2px) is allowed on a control if a platform demands it. Do not round the still into a large squircle.

## Components

`button-primary` is ink (`#1c1915`) on paper (`#f3efe6`), square, 44px tall, `16px` inline padding. On a quiet object page, prefer `button-quiet`: ink text, an underline, no fill. One filled action per view.

`field` is a square box (`height: 44px`) with a `1px` `line` border (`#8d8476`) and a visible label above it in `ui`. Placeholder text is not the label.

A product fact list is not a card grid. It is `<dl>` `dt`/`dd` pairs separated by `1px` `hairline` (`#ddd4c6`).

## Do's and Don'ts

- Do let the photograph or the object be the warmest thing on the page.
- Do keep headlines at regular weight (`400`) and tabular numerals aligned on prices/dimensions.
- Do leave a wide margin rather than stretch the paragraph.
- Don't put `accent` (`#7a3e2e`) on every link, icon, and secondary badge.
- Don't apply warm cream + Newsreader to a dense SaaS log or analytics table (`uniqueness.calm-editorial-slop`).
- Don't add a shadow stack, a gradient mesh, or a second display family.
- Don't set body text below 14px.
- Don't center the column under a centered headline with two buttons.

## Agent Prompt Guide

Quick Color Reference:
- canvas: `#f3efe6` (`--pt-surface`)
- raised panel: `#f7f4ee` (`--pt-surface-raised`)
- image matte: `#eae4d8` (`--pt-surface-subtle`)
- primary ink & action fill: `#1c1915` (`--pt-ink`)
- secondary copy: `#5c564c` (`--pt-ink-muted`)
- oxide emphasis (status/sold-out word once): `#7a3e2e` (`--pt-accent`)

Example Component Prompts:
1. Build the primary spread on `#f3efe6`: 1120px max-width, 64px gap between a sharp-cornered (`0px` radius) object still on `#eae4d8` and a 42ch right column with a left-aligned Newsreader 40px weight 400 heading, 16px Public Sans body, `1px` `#ddd4c6` hairline spec rows (`tabular-nums`), and one square `44px` tall `#1c1915` primary button (`#f3efe6` text).
2. Build a hairline header bar: `56px` height on `#f3efe6`, bottom border `1px solid #ddd4c6`, left wordmark in Newsreader 18px, right text links in Public Sans 14px `#5c564c` (`24px` gap), active link in `#1c1915` with `1px` underline—no search pills or colored buttons.
3. Build a square reservation form field: visible 14px label `#1c1915` positioned `8px` above a `44px` input (`#f7f4ee` fill, `1px solid #8d8476` border, `0px` radius), with inline helper text in `13px #5c564c` and `2px` offset `#1c1915` `:focus-visible` outline.
4. Build a firing availability note: flat layout with no card box, `Sold out · Next firing Dec 4` set inline in `14px #7a3e2e` above a single underlined text trigger `Join firing waitlist`.
