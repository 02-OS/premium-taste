---
version: alpha
name: Instrument
description: >
  Example identity for the precise-technical direction. A light instrument
  for lists, logs, and documents. Not a dark dashboard theme, and not a
  marketing page.
colors:
  surface: "#f5f5f2"
  surface-raised: "#ffffff"
  ink: "#1b1d1c"
  ink-muted: "#4e5450"
  hairline: "#e2e3dc"
  accent: "#1e5c40"
  on-accent: "#f3f6f4"
  danger: "#8f2d1f"
  warning: "#8a5a12"
typography:
  title:
    fontFamily: "IBM Plex Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 20px
    fontWeight: 500
    lineHeight: 1.3
  body:
    fontFamily: "IBM Plex Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "IBM Plex Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.3
  mono:
    fontFamily: "IBM Plex Mono, ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.4
rounded:
  none: 0px
  control: 4px
spacing:
  2xs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
    height: 32px
    paddingInline: 12px
  button-quiet:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    rounded: "{rounded.control}"
    height: 32px
  row:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    rounded: "{rounded.none}"
    minHeight: 40px
    paddingInline: 12px
  field:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
    rounded: "{rounded.control}"
    height: 32px
---

## Overview

Instrument is a sample identity for a screen where someone repeats a decision: a revision list, a document, a set of layers. The ground is cool paper. Type sits in a narrow range. Status is a word in a known color. The page has no hero and no stat strip.

IBM Plex Sans and IBM Plex Mono are the open pair (SIL Open Font License). Mono is for identifiers and figures, not for headings. Links are ink with an underline. `accent` means a successful or live state. It is not the button color.

If the product already has a brand guide, keep its families and map these roles onto them. Do not introduce indigo so that it "looks like a tool."

## Colors

`surface` is the application ground. `surface-raised` is only for menus, dialogs, and the inside of a field.

`ink` is primary text and the primary button. `ink-muted` is column labels, timestamps, and authors. It stays above 4.5:1 on `surface`.

`hairline` divides rows.

`accent` is the shipped or live word. `warning` is an in-progress word. `danger` is a failed word. Each is used as text color beside the word itself, not as a filled pill. Do not add a fourth hue for links.

## Typography

`title` is the name of the collection on this screen (Revisions, Layers, Today), at 20px medium. One per view.

`body` is 14px for row content and document text inside the tool. Long-form documentation should rise toward 16px; this token is for the instrument, not for an essay.

`label` is column headers and the name of a filter. Sentence case, no tracking.

`mono` is a hash, an id, or a numeric column. Set `font-variant-numeric: tabular-nums` on figure columns even in the sans.

## Layout

Page padding is `md` or `lg`. The list runs the width of the page. Rows are a grid with a shared template: status, identifier, message, person, time. The message column takes the free space. Row minimum height is 40px. Groups of rows are separated from the title by `lg`, and from a filter by `sm`.

Do not place four summary cards above the list. If a number matters, put it on the row.

A document variant (see the Stripe Docs reference) uses the same colors and replaces the row grid with a column of about 68 characters, a nav, and a contents rail. Do not use both the row grid and the document column on one screen.

## Elevation & Depth

Rows are flat, divided by `hairline`. `surface-raised` plus a hairline is a menu or a dialog. One shadow exists, on that overlay only, and it is neutral and short. No shadow on rows, no blur, no nested panels.

## Shapes

Rows and the page are square (`rounded.none`). Controls — buttons and fields — use `rounded.control` (4px). Do not round the row into a pill or a card.

## Components

`button-primary` is the one filled action, ink, 32px tall, 4px radius. `button-quiet` is the second action if you truly need one: hairline border, ink text.

`row` is the repeating object. Status inside it is a word. A 6px dot may sit beside the word and is `aria-hidden`, because the word already carries the state.

`field` has a visible label. In a filter, the label sits on the same line as the input, in `label`, not as a placeholder.

## Do's and Don'ts

- Do align every row to one grid.
- Do say Failed, Building, Shipped. Do not rely on the dot.
- Do keep the first screen on the list itself.
- Don't add a sidebar, a greeting, and four stat cards (`layout.dashboard-costume`).
- Don't use a purple primary, a gradient header, or mono for the title.
- Don't put a shadow and a large radius on each row.
- Don't invent a dark version by inverting these hex values. A night instrument needs its own surface steps (see `color.dark-surfaces`).
