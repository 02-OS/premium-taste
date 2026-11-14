---
version: alpha
name: Column
direction: editorial-print
description: >
  Example identity for the editorial-print direction. A paper sheet and a
  reading column. Not a newspaper's own stock, and not a copy of any
  reference. Use it only when the product has no guide of its own.
scale:
  name: Major Third
  ratio: 1.25
  base: 18px
opentype:
  numeric: oldstyle-nums proportional-nums
  features: '"kern" 1, "liga" 1, "onum" 1'
surfaces:
  step-0-canvas: "#f6f1e8"
  step-1-raised: "#fbf7f1"
  step-2-subtle: "#ece4d6"
  step-3-inverted: "#1c1917"
colors:
  surface: "#f6f1e8"
  surface-raised: "#fbf7f1"
  surface-subtle: "#ece4d6"
  ink: "#1c1917"
  ink-muted: "#4e4944"
  hairline: "#d8d0c4"
  line: "#8a8176"
  accent: "#1c1917"
  on-accent: "#f6f1e8"
  danger: "#8d2f2f"
typography:
  display:
    fontFamily: "Source Serif 4, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 44px
    fontWeight: 500
    lineHeight: 1.15
    letterSpacing: -0.015em
  title:
    fontFamily: "Source Serif 4, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 28px
    fontWeight: 500
    lineHeight: 1.25
    letterSpacing: -0.01em
  body:
    fontFamily: "Source Serif 4, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: 0em
  ui:
    fontFamily: "Public Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0em
  caption:
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
rounded:
  none: 0px
spacing:
  xs: 8px
  sm: 16px
  md: 24px
  lg: 32px
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

Column is a sample identity for a page whose subject is a text: an essay, a story, a section of a briefing. The surface is a warm sheet. Ink is soft black. A text serif sets the prose. A sans sets the caption, the navigation, and the one kicker. There is no second hue. Photography, if the piece has it, supplies the other color. Links are ink, and they are underlined.

This file follows the DESIGN.md format. Premium Taste's judgment still lives in `taste/principles.md`. If these tokens and the principles disagree, follow the principles.

`accent` is the same value as `ink` on purpose. A house with a real accent (a claret used only on a masthead, for example) should put that in the product's own guide. This sample will not invent one. A house with its own paper replaces `surface` entirely. The Financial Times salmon is that kind of paper: the whole page, never a tint behind a card.

Open substitutes: Source Serif 4 and Public Sans, both widely available under the SIL Open Font License. Do not swap in Playfair Display, Cormorant, or a costume grotesk.

## Colors

`surface` is the sheet. Every region of the page uses it. `surface-raised` is a menu or a note only, one step lighter, with a `line` border. It is not a card behind a paragraph.

`ink` is text, the masthead, the rules that structure the page, links, and the rare filled button. `ink-muted` is the caption, the byline's secondary fact, and the footer. It clears 4.5:1 on `surface`. Do not lighten it into a gray that fails.

`hairline` is a quiet seam (`#d8d0c4`). `line` clears 3:1 on `surface` (`#8a8176`) and frames input controls. A rule that ends a piece or divides stories is `ink`, 1px, not `hairline`.

`danger` is for a real error in a form. It is not a brand red.

## Surfaces

| Step | Token | Hex | Purpose |
| --- | --- | --- | --- |
| 0 | `surface` | `#f6f1e8` | Primary editorial paper sheet across masthead and columns |
| 1 | `surface-raised` | `#fbf7f1` | Margin notes, popovers, and dropdown menus only |
| 2 | `surface-subtle` | `#ece4d6` | Recessed index strips or archival table header bands |
| 3 | `ink` | `#1c1917` | Story rules, masthead ink, and primary CTA fill (`#f6f1e8` ink) |

## Typography

`display` is the story title, once (`44px`, weight `500`). `title` is a section inside the piece (`28px`). `body` is Source Serif 4 at `18px`, ragged right, with a measure near `65–72ch`. Do not justify on the web.

`caption` and `ui` are Public Sans at `14px`. `kicker` is the only tracked style (`+0.06em`), and only one kicker may appear on a story. Never set tracked caps on non-Latin scripts or form labels. Prose may enable `oldstyle-nums`; archival financial tables switch strictly to `tabular-nums`.

## Type Scale Detail

| Role | Family | Size | Weight | Line Height | Letter Spacing |
| --- | --- | --- | --- | --- | --- |
| Display | Source Serif 4 | 44px | 500 | 1.15 | -0.015em |
| Title | Source Serif 4 | 28px | 500 | 1.25 | -0.01em |
| Body | Source Serif 4 | 18px | 400 | 1.55 | 0em |
| UI / Caption | Public Sans | 14px | 400 | 1.40 | 0em |
| Kicker | Public Sans | 13px | 500 | 1.35 | 0.06em |

## Imagery

Documentary photography and archival plates earn full-column or bled width with square `0px` corners and explicit `width`/`height`. Always place a crisp `14px Public Sans` factual caption beneath the photograph naming subject and photographer. Never crop into glossy squircles or stack headline text over un-scrimmed photos.

## Layout

A masthead in `ui`, small, at the top. Then either a full image with a `caption`, or the reading column. Page margin is at least 24px and grows with the viewport. The column's maximum measure stays around `65ch–70ch`. Space above a section is `xl` (48px) or `2xl` (80px). Space between paragraphs is `md` (24px).

## Elevation & Depth

Flat. Paper does not lift. `surface-raised` (`#fbf7f1`) is a menu only. No shadow on a paragraph, a figure, or a pull quote.

## Shapes

Square. Figures, buttons, and fields use `rounded.none` (0px).

## Components

Prefer `button-quiet` in a story: ink text, an underline, no fill. `button-primary` is `#1c1917` on `#f6f1e8`, square, 44px, and at most one per view (a subscribe trigger in the masthead).

`field` has a visible label in `ui` above it, a `1px solid #8a8176` border, and `2px` `#1c1917` focus ring.

A pull quote is `title` italic (`28px Source Serif 4`) inside the reading column, bracketed top and bottom by `1px solid #1c1917` rules—not a pastel callout box.

## Do's and Don'ts

- Do keep one sheet color (`#f6f1e8`) for the whole page.
- Do set prose in Source Serif 4 and apparatus in Public Sans.
- Do leave the right prose edge ragged (`text-align: start`).
- Do use a `1px` `#1c1917` rule where a card border would have been.
- Don't pass the Editorial Test fail state (`uniqueness.calm-editorial-slop`): never dress an operational app or SaaS landing in editorial parchment without editorial substance.
- Don't justify the column or set body text below 16px (`18px` standard).
- Don't combine a drop cap, a pull quote card, a huge headline, and textured noise together.

## Agent Prompt Guide

Quick Color Reference:
- sheet canvas: `#f6f1e8` (`--pt-surface`)
- note / popover surface: `#fbf7f1` (`--pt-surface-raised`)
- archival strip: `#ece4d6` (`--pt-surface-subtle`)
- primary ink & structural rule: `#1c1917` (`--pt-ink`)
- bylines & captions: `#4e4944` (`--pt-ink-muted`)
- real error text: `#8d2f2f` (`--pt-danger`)

Example Component Prompts:
1. Build an essay opener on `#f6f1e8`: single hairline masthead (`52px`, `1px solid #1c1917` bottom border), centered or left-aligned `65ch` column opening with one `13px Public Sans` kicker (`+0.06em`), a `44px Source Serif 4` weight 500 headline, standfirst paragraph (`20px`), and author/date line in `#4e4944`.
2. Build a full-width documentary figure block inside the column: sharp `0px` image with declared dimensions, `8px` spacing to a `14px Public Sans` caption (`#4e4944`) and trailing italic photographer credit, closed by a `1px solid #d8d0c4` hairline.
3. Build a typographic pull quote: `28px Source Serif 4` italic quote in `#1c1917`, `24px` vertical padding, `1px solid #1c1917` border-top and border-bottom, zero background fill or side bar.
4. Build a dispatch archive list below a `1px solid #1c1917` divider: `1px solid #d8d0c4` rows pairing right-aligned `tabular-nums` date (`14px Public Sans #4e4944`), story headline (`20px Source Serif 4`), and section tag—zero card boxes.
