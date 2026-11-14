---
version: alpha
name: Night Room
description: >
  Example identity for the cinematic-dark direction. A night room for one
  work. Not a dark-mode toggle, and not a copy of any reference. Use it only
  when the product has no guide of its own.
colors:
  surface: "#141311"
  surface-raised: "#1e1c19"
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
  title:
    fontFamily: "Schibsted Grotesk, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 24px
    fontWeight: 500
    lineHeight: 1.2
  body:
    fontFamily: "Schibsted Grotesk, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  ui:
    fontFamily: "Schibsted Grotesk, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
  meta:
    fontFamily: "Schibsted Grotesk, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.4
  credit:
    fontFamily: "Source Serif 4, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.4
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

`ink` is text, the wordmark, the primary button fill, and the focus ring. `ink-muted` is the secondary line (a year, a duration, a supporting name). Both clear 4.5:1 on `surface` and on `surface-raised`. Do not push the muted ink toward the ground to make it "softer."

`hairline` is a seam between stacked facts. It is deliberately quiet, and it is not strong enough to be the only boundary of a control. `line` is that boundary. It clears 3:1 on both surfaces. Use it on a field or any control whose edge has to be visible.

`accent` is clay. Use it once, as a word: a live state, a single mark. It clears 4.5:1 as text on both surfaces. `on-accent` is the room color, for the rare case where the clay is a small fill. The button does not use `accent`. `danger` is a lighter rose, reserved for a real error, so clay does not mean "everything important." Do not communicate either state by color alone.

## Typography

`display` is the title of the work, once, at regular weight. Do not set it in all capitals by default. Capitals are a voice you may choose for one credit or one section label, not for the page.

`title` is a section, if the screen has one. `body` is a short text beside the work, at 16px. This direction is not a long essay. If the text runs long, move the screen to editorial print. `ui` is the transport and the links. `meta` is the quiet fact under the title.

`credit` is Source Serif 4 italic, and it appears at most once (a director, a label, a date line that needs a second voice). If you do not need it, do not load the second family.

## Layout

The work occupies most of the first screen, or the first screen is a single column of works in rows. Page margin is at least 24px and grows with the viewport. The title sits on the work or in a hard column beside it, with `md` between the title and the meta line. Section gaps, when a second band exists, are `xl` or `2xl`. Do not center a title, a paragraph, and two buttons in the middle of an empty field.

On a narrow viewport the work comes first, then the title and the one action. Type sizes stay.

## Elevation & Depth

Flat. The still is the depth. `surface-raised` plus a `line` border is the whole elevation system, used for a dialog or for the transport if it must float over the art. No glow, no colored shadow, no blur used as a material. A shadow, if a dialog cannot be a band, is one soft shadow tinted toward black at low opacity.

## Shapes

Square. Stills, sleeves, buttons, and fields use `rounded.none`. Do not round the work into a large squircle.

## Components

`button-primary` is off-white ink on the room, square, 44px tall, used for the one action (play, enter, subscribe). There is no glow on it. On a screen where the action can be a word, prefer `button-quiet`: ink text, an underline, no fill. One of them, not both as equals.

`field` is rare in this direction. When it exists, it has a visible label in `ui`, a `line` border, and no placeholder standing in as the label.

Transport is a row of `ui` controls. The primary control is the button. The others are quiet. State (playing, unavailable) is a word. A clay word may accompany it once.

Focus is a 2px `ink` ring, offset from the control, visible on `surface`.

## Do's and Don'ts

- Do let the still, the sleeve, or the poster be the colored thing in the room.
- Do keep the room empty of chrome when the work is removed. An empty room is the test. A dashboard with the lights off fails it.
- Do keep headlines at regular weight unless the title is genuinely a section label.
- Don't put `accent` on the button, the links, and the icons.
- Don't add a purple glow, a gradient mesh, gold rules, or a blurred enlargement of the art in place of the art.
- Don't invert a light layout and call it cinematic.
- Don't set body text below 14px.
- Don't set every label in capitals.
