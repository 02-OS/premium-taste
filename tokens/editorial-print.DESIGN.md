---
version: alpha
name: Column
description: >
  Example identity for the editorial-print direction. A paper sheet and a
  reading column. Not a newspaper's own stock, and not a copy of any
  reference. Use it only when the product has no guide of its own.
colors:
  surface: "#f6f1e8"
  surface-raised: "#fbf7f1"
  ink: "#1c1917"
  ink-muted: "#4e4944"
  hairline: "#d8d0c4"
  line: "#8a8176"
  accent: "#1c1917"
  danger: "#8d2f2f"
typography:
  display:
    fontFamily: "Source Serif 4, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 44px
    fontWeight: 500
    lineHeight: 1.15
  title:
    fontFamily: "Source Serif 4, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 28px
    fontWeight: 500
    lineHeight: 1.25
  body:
    fontFamily: "Source Serif 4, Iowan Old Style, Palatino, Georgia, serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.55
  ui:
    fontFamily: "Public Sans, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.4
  caption:
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

`hairline` is a quiet seam (a footer, a thin separation inside a caption block). It is not strong enough to be the only edge of a control. `line` clears 3:1 on `surface` and is the field border. A rule that ends a piece or divides two stories is `ink`, 1px, not `hairline`.

`danger` is for a real error in a form. It is not a brand red. `accent` does not add a color. If you feel the page needs a hue, the piece is missing a photograph or a fact, not a token.

## Typography

`display` is the story title, once. `title` is a section inside the piece. A front page that must rank several stories may add one size above `display` for the lead and keep the other headlines at `title` or below. Do not invent five sizes, and do not make every story `display`.

`body` is Source Serif 4 at 18px, ragged right, with a measure near 65–72 characters. Do not justify on the web. `caption` and `ui` are Public Sans. Captions sit under the figure, smaller in role than the prose, at 14px so they still pass. `kicker` is the only tracked style, and only one kicker may appear on a story. Tracking is a Latin-script device. In another writing system, drop the letter-spacing and keep the size. Do not set the kicker in all capitals as a habit, and do not set form labels in it.

No drop cap. Italic is for a real textual reason (a title of a work, a word the writer emphasized), not a second brand.

## Layout

A masthead in `ui`, small, at the top. Then either a full image with a `caption`, or the column. Page margin is at least 24px and grows with the viewport. The column's maximum measure stays. Do not stretch the paragraph to the window. Space above a section is `xl` or `2xl`. Space between paragraphs is `md`. The title sits `md` above the body.

A newspaper front replaces the single column with several. The lead is wider. Secondary stories are narrower. Rules in `ink` separate them. The sheet color does not change between columns.

On a narrow viewport there is one column. The image, if it is the way in, comes first. Type sizes stay. Do not center the stack.

## Elevation & Depth

Flat. Paper does not lift. `surface-raised` is a menu only. No shadow on a paragraph, a figure, or a pull quote. If a dialog must float, one soft shadow tinted toward `ink` at low opacity is the entire elevation system.

## Shapes

Square. Figures, buttons, and fields use `rounded.none`. Do not round a photograph into a card.

## Components

Prefer `button-quiet` in a story: ink text, an underline, no fill. `button-primary` is ink on paper, square, 44px, and at most one per view (a subscribe control in the masthead, not a second one at the end of every paragraph). Do not show both as equals.

`field` is rare. It has a visible label in `ui` above it, a `line` border, and no placeholder standing in as the label.

A pull quote, if the piece truly needs one, is `title` italic in the column, with an `ink` rule above and below. It is not a colored card.

Focus is a 2px `ink` ring, offset from the control.

## Do's and Don'ts

- Do keep one sheet color for the whole page.
- Do set prose in the serif and apparatus in the sans.
- Do leave the right edge ragged.
- Do use a 1px ink rule where a card would have been.
- Don't justify the column.
- Don't add a link hue, a highlight behind a paragraph, or a tinted card.
- Don't combine a drop cap, a pull quote, a huge headline, and a texture on the same page.
- Don't set body text below 16px. This sample uses 18px.
- Don't center a headline over an image with a gradient scrim.
