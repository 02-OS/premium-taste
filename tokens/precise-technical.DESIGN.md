---
version: alpha
name: Instrument
direction: precise-technical
description: >
  Example identity for the precise-technical direction. A light instrument
  for lists, logs, and documents. Not a dark dashboard theme, and not a
  marketing page.
scale:
  name: Major Second
  ratio: 1.125
  base: 14px
opentype:
  numeric: tabular-nums
  features: '"tnum" 1, "cv01" 1, "zero" 1'
surfaces:
  step-0-canvas: "#f5f5f2"
  step-1-raised: "#ffffff"
  step-2-subtle: "#ecece6"
  step-3-inverted: "#1b1d1c"
colors:
  surface: "#f5f5f2"
  surface-raised: "#ffffff"
  surface-subtle: "#ecece6"
  ink: "#1b1d1c"
  ink-muted: "#4e5450"
  hairline: "#e2e3dc"
  line: "#c4c6bd"
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
    letterSpacing: -0.015em
  body:
    fontFamily: "IBM Plex Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: 0em
  label:
    fontFamily: "IBM Plex Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: 0.01em
  mono:
    fontFamily: "IBM Plex Mono, ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0em
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
    borderColor: "{colors.line}"
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
    borderColor: "{colors.line}"
    rounded: "{rounded.control}"
    height: 32px
---

## Overview

Instrument is a sample identity for a screen where someone repeats a decision: a revision list, a document, a set of layers. The ground is cool paper. Type sits in a narrow range. Status is a word in a known color. The page has no hero and no stat strip.

IBM Plex Sans and IBM Plex Mono are the open pair (SIL Open Font License). Mono is for identifiers and figures, not for headings. Links are ink with an underline. `accent` means a shipped/healthy state. It is not a blanket marketing color.

If the product already has a brand guide, keep its families and map these roles onto them. Do not introduce indigo so that it "looks like a tool."

## Colors

`surface` is the application ground. `surface-raised` (`#ffffff`) is for the working sheet, menus, dialogs, and inside fields. `surface-subtle` (`#ecece6`) marks header bands or selected table tabs.

`ink` (`#1b1d1c`) is primary text and the default compact button fill. `ink-muted` (`#4e5450`) is column labels, timestamps, and authors; it maintains `>= 7:1` contrast on `#f5f5f2` and `#ffffff`.

`hairline` (`#e2e3dc`) divides dense rows; `line` (`#c4c6bd`) frames input edges and quiet buttons.

`accent` (`#1e5c40`) is shipped/live, `warning` (`#8a5a12`) is in-progress/degraded, and `danger` (`#8f2d1f`) is failed/destructive. Each sits directly on the word itself (`a11y.not-color-alone`), not as a saturated filled badge circus.

## Surfaces

| Step | Token | Hex | Purpose |
| --- | --- | --- | --- |
| 0 | `surface` | `#f5f5f2` | Cool gray-paper outer shell and navigation chrome |
| 1 | `surface-raised` | `#ffffff` | Data tables, form controls, menus, and active code panes |
| 2 | `surface-subtle` | `#ecece6` | Segmented toggle tracks, column headers, and row hover states |
| 3 | `ink` | `#1b1d1c` | Primary ink, high-emphasis control fills, and dark console panels |

## Typography

`title` is the name of the collection on this screen (`Revisions`, `Layers`, `Deployments`), at 20px medium (`500`). One per view.

`body` is `14px` for operational row content (`16px` for long documentation). `label` is `12px` medium for column headers and filter labels (`sentence case`, minimal `+0.01em` clarity).

`mono` is hashes, IDs, latencies, and payloads (`13px`). Enable `font-variant-numeric: tabular-nums` and OpenType `"tnum" 1, "zero" 1` on every column of counts, durations, prices, or build hashes so columns stay aligned.

## Type Scale Detail

| Role | Family | Size | Weight | Line Height | Letter Spacing |
| --- | --- | --- | --- | --- | --- |
| Title | IBM Plex Sans | 20px | 500 | 1.30 | -0.015em |
| Body | IBM Plex Sans | 14px | 400 | 1.45 | 0em |
| Mono Data | IBM Plex Mono | 13px | 400 | 1.40 | 0em |
| Label | IBM Plex Sans | 12px | 500 | 1.30 | 0.01em |

## Imagery

Product UI and documentation rely on real interface state, crisp SVG sparklines/diagrams grounded in telemetry, or honest terminal captures. Keep crops crisp (`0px–4px` border-radius) framed by `1px solid #e2e3dc`. Never insert stock lifestyle avatars or floating 3D illustrations.

## Layout

Page padding is `md` (16px) or `lg` (24px). Rows share a unified grid template (`status`, `identifier`, `message`, `person`, `time`) with a minimum row height of `40px`. Groups separate from titles by `lg` and from filter controls by `sm`.

A document variant (Stripe Docs structure) keeps `#f5f5f2` / `#ffffff` surfaces, locks a `68ch` reading measure, and brackets it with left nav + right Table of Contents without inserting marketing heroes.

## Elevation & Depth

Rows are flat, divided by `1px` `hairline`. `surface-raised` plus a `hairline` border and one short neutral shadow exists on true overlays (`command palette`, `dropdown`) only. Zero shadow on rows or in-flow summary strips.

## Shapes

Rows and containers sit square (`rounded.none`, `0px`). Compact interactive controls—buttons, filter pills, text fields—use `rounded.control` (`4px`). Do not round operational rows into `16px` cards.

## Components

`button-primary` is `#1b1d1c` fill with `#f5f5f2` ink (`height: 32px`, `4px` radius, `12px` inline padding). `button-quiet` uses transparent fill, `1px solid #c4c6bd` border, `#1b1d1c` ink.

`row` enforces `minHeight: 40px`, bottom hairline `#e2e3dc`, single-line aligned status word + `6px` `aria-hidden` status dot.

`field` pairs a visible `12px–14px` `<label>` aligned horizontally or directly above a `32px–38px` `#ffffff` input with `#c4c6bd` border and `2px` `#1e5c40` `:focus-visible` ring.

## Do's and Don'ts

- Do start on the repeating object (`Revisions`, `Deploys`, `Endpoints`) within the first viewport.
- Do say `Failed`, `Building`, `Shipped` in legible contrast (`#8f2d1f`, `#8a5a12`, `#1e5c40`), never color-only dots.
- Do enforce `tabular-nums` on every numeric/metric column.
- Don't add a left sidebar + greeting + four summary KPI cards above a table that already shows those facts (`layout.dashboard-costume`).
- Don't wrap each list row in a shadowed rounded box (`material.gray-card-shadow`).
- Don't inject purple accents, gradient headings, or Inter/Geist defaults.
- Don't invert these light hex values mechanically for a dark mode—redesign stepped dark surfaces instead.

## Agent Prompt Guide

Quick Color Reference:
- shell ground: `#f5f5f2` (`--pt-surface`)
- content sheet & inputs: `#ffffff` (`--pt-surface-raised`)
- subtle track/hover: `#ecece6` (`--pt-surface-subtle`)
- primary ink & action fill: `#1b1d1c` (`--pt-ink`)
- muted metadata: `#4e5450` (`--pt-ink-muted`)
- shipped / warning / failed: `#1e5c40` / `#8a5a12` / `#8f2d1f`

Example Component Prompts:
1. Build an operational filterable table inside `#ffffff` bordered by `1px solid #e2e3dc`: header row in `12px` weight 500 `#4e5450`, fixed `44px` rows (`IBM Plex Sans` `14px` text + `IBM Plex Mono` `13px` SHA/latency columns with `tabular-nums`), status word (`Failed` `#8f2d1f`, `Shipped` `#1e5c40`), zero card shadows.
2. Build an inline filter toolbar: `32px` height search input (`#ffffff`, `1px solid #c4c6bd`, `4px` radius, explicit `<label>` beside it), segmented filter buttons inside `#ecece6` track, and one `32px` `#1b1d1c` primary trigger (`New deploy`) on the right.
3. Build an inspection console strip: `#1b1d1c` background, `4px` radius, header bar displaying command label in `#a6aca7`, `13px IBM Plex Mono` payload text in `#edf0ec`, and a crisp `1px solid #4e5450` Copy button.
4. Build a documentation 3-zone grid: `240px` left nav on `#f5f5f2`, flexible center prose column capped at `68ch` on `#ffffff` (`16px` body, `1.5` leading), `200px` sticky section ToC on the right with `1px solid #e2e3dc` active indicator line.
