---
version: alpha
name: Night Room
direction: cinematic-dark
description: >
  Example identity for the cinematic-dark direction. A night room for one
  work. Not a dark-mode toggle, and not a copy of any reference. Use it only
  when the product has no guide of its own.
scale:
  name: Minor Third
  ratio: 1.2
  base: 16px
opentype:
  numeric: tabular-nums
  features: '"kern" 1, "liga" 1'
surfaces:
  step-0-canvas: "#141311"
  step-1-raised: "#1e1c19"
  step-2-subtle: "#262420"
  step-3-inverted: "#f3f0e8"
colors:
  surface: "#141311"
  surface-raised: "#1e1c19"
  surface-subtle: "#262420"
  ink: "#f3f0e8"
  ink-muted: "#9c978e"
  hairline: "#2a2825"
  line: "#746e66"
  accent: "#c9846a"
  on-accent: "#141311"
  danger: "#e7b2aa"
typography:
  display:
    fontFamily: "Schibsted Grotesk, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 40px
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: -0.02em
  title:
    fontFamily: "Schibsted Grotesk, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: -0.015em
  body:
    fontFamily: "Schibsted Grotesk, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0em
  ui:
    fontFamily: "Schibsted Grotesk, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0em
  meta:
    fontFamily: "Schibsted Grotesk, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0em
  credit:
    fontFamily: "Source Serif 4, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0em
    fontStyle: italic
rounded:
  none: 0px
spacing:
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  2xl: 96px
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
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    borderColor: "{colors.line}"
    rounded: "{rounded.none}"
    height: 44px
---

## Overview

Night Room is a sample identity for a screen whose subject is one work in the dark: a still, a sleeve, a performance. The ground is a warm black. Type is off-white. Color is supposed to come from the work. A clay accent exists for a single signal word. A rose exists for a real error. Neither is a glow, and neither is the button.

This file follows the DESIGN.md format. Premium Taste's judgment still lives in `taste/principles.md`. If these tokens and the principles disagree, follow the principles. Do not get here by inverting `tokens/quiet-luxury.DESIGN.md` or `tokens/precise-technical.DESIGN.md`.

Open substitutes: Schibsted Grotesk for the room, and Source Serif 4 italic for one credit line. Both are widely available under the SIL Open Font License. Do not swap in a costume grotesk, and do not set the credit face on the title.

## Colors

`surface` is the room. It is warm, and it is not pure black. `surface-raised` is one step up, for a dialog or a transport bar that must separate from the still. It is not a card behind every fact.

`ink` is text, the wordmark, the primary button fill, and the focus ring. `ink-muted` is the secondary line (a year, a duration, a supporting name). Both clear 4.5:1 on `surface` and on `surface-raised`.

`hairline` is a seam between stacked facts. `line` clears 3:1 on both dark surfaces and frames interactive controls.

`accent` is clay (`#c9846a`). Use it once, as a word: a live state, a single mark. `danger` (`#e7b2aa`) is a lighter rose reserved for a real error. Do not communicate either state by color alone.

## Surfaces

| Step | Token | Hex | Purpose |
| --- | --- | --- | --- |
| 0 | `surface` | `#141311` | Warm theater ground; absorbs background chrome |
| 1 | `surface-raised` | `#1e1c19` | Transport bar, popover, or caption sidecar |
| 2 | `surface-subtle` | `#262420` | Highlighted row or hover plane on dense screening lists |
| 3 | `ink` | `#f3f0e8` | Off-white primary text and solid `0px` action fill |

## Typography

`display` is the title of the work, once, at regular weight (`400`). Do not set it in all capitals by default. `title` is a section (`24px`, weight `500`), if the screen has one. `body` is a short text beside the work, at 16px.

`ui` is the transport and the links (`14px`). `meta` is the quiet fact under the title (`13px`, `tabular-nums` for durations and dates).

`credit` is Source Serif 4 italic (`15px`), and it appears at most once (a director, a label, a date line that needs a second voice). If you do not need it, do not load the second family.

## Type Scale Detail

| Role | Family | Size | Weight | Line Height | Letter Spacing |
| --- | --- | --- | --- | --- | --- |
| Display | Schibsted Grotesk | 40px | 400 | 1.10 | -0.02em |
| Title | Schibsted Grotesk | 24px | 500 | 1.20 | -0.015em |
| Body | Schibsted Grotesk | 16px | 400 | 1.50 | 0em |
| Credit | Source Serif 4 (italic) | 15px | 400 | 1.40 | 0em |
| UI | Schibsted Grotesk | 14px | 400 | 1.40 | 0em |
| Meta | Schibsted Grotesk | 13px | 400 | 1.40 | 0em |

## Imagery

Photography, film stills, or album sleeves supply the only saturation in the room. Render edge-to-edge or inside sharp `0px` frames (`rounded.none`) with declared dimensions. If placing title text near an image, isolate the text beside the work on `#141311` or over an explicit opaque/stepped band—never a thin gradient glow.

## Layout

The work occupies most of the first screen, or the first screen is a single column of works in rows. Page margin is at least 24px and grows with the viewport. The title sits on the work or in a hard column beside it, with `md` (24px) between the title and the meta line. Section gaps, when a second band exists, are `xl` (64px) or `2xl` (96px).

On a narrow viewport the work comes first, then the title and the one action. Type sizes stay.

## Elevation & Depth

Flat. The still is the depth. `surface-raised` (`#1e1c19`) plus a `line` (`#746e66`) border is the whole elevation system. No glow, no colored shadow, no purple blur. A shadow, if a dialog must float, is one crisp short shadow tinted toward black.

## Shapes

Square. Stills, sleeves, buttons, and fields use `rounded.none` (0px).

## Components

`button-primary` is off-white ink (`#f3f0e8`) on the dark room (`#141311`), square, `44px` tall, `16px` inline padding, used for the one primary action (`Watch 35mm transfer`, `Buy ticket`). Prefer `button-quiet` (underlined `#f3f0e8` text) when text alone carries the link.

`field` is rare. When present (`14px` visible label above in `#f3f0e8`), it uses `#1e1c19` fill and `1px solid #746e66`. Focus is a `2px` `#f3f0e8` ring at `2px` offset.

## Do's and Don'ts

- Do let the still, sleeve, or poster be the colored thing in the room.
- Do keep the room empty of chrome when the work is removed. A dashboard with the lights off fails this test.
- Do align listing dates and durations using `tabular-nums`.
- Don't put `accent` (`#c9846a`) on the button, all links, and icons.
- Don't add purple/indigo glow, gradient meshes, gold rules, or a blurred backdrop enlargement of the art.
- Don't invert a light SaaS form into `#141311` and call it cinematic.
- Don't set body text below 14px.

## Agent Prompt Guide

Quick Color Reference:
- room canvas: `#141311` (`--pt-surface`)
- raised transport/dialog: `#1e1c19` (`--pt-surface-raised`)
- subtle row hover: `#262420` (`--pt-surface-subtle`)
- primary ink & action fill: `#f3f0e8` (`--pt-ink`)
- secondary meta: `#9c978e` (`--pt-ink-muted`)
- single live/signal word: `#c9846a` (`--pt-accent`)

Example Component Prompts:
1. Build a cinema feature spread on `#141311`: full-bleed or large sharp (`0px`) 16:9 film still alongside a `360px` column displaying a single live clay label (`#c9846a`, `13px`), a `40px` weight 400 Schibsted Grotesk title (`#f3f0e8`, `-0.02em`), Source Serif 4 italic credit (`15px`, `#9c978e`), 2-sentence synopsis, and one `44px` square `#f3f0e8` button (`#141311` text).
2. Build a dense night screening schedule row: flat `#141311` rows separated by `1px solid #2a2825`, hover state `#262420` with zero shadow/lift, 4-column grid (`19:30` in `tabular-nums`, title `#f3f0e8`, venue `#9c978e`, status `Tickets` or `Sold out`), `44px` minimum row height.
3. Build a minimal night audio transport bar (`#1e1c19` fill, top rule `1px solid #746e66`): track title + italic artist credit on the left, `02:14 / 04:50` (`tabular-nums`) centered, single square `Pause` button and underlined `Tracklist` toggle on the right.
4. Build a top dark masthead: `56px` height on `#141311`, `1px solid #2a2825` bottom seam, left lowercase wordmark (`#f3f0e8`), 3 plain navigation links (`14px`, `#9c978e` hovering to `#f3f0e8`), zero search pills or notification badges.
