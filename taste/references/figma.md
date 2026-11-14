---
id: figma
title: Figma editor
url: https://www.figma.com
direction: precise-technical
tags:
  - tool-chrome
  - panels
  - hairline
  - selection-color
  - compact-type
job: edit a design on a canvas
medium: app
confidence: high
observed: 2026-11
---

# Figma editor

**Tags:** `precise-technical` `tool-chrome` `panels` `hairline` `selection-color` `compact-type`

The editor. The marketing site at figma.com is a different register and is not what you should load for a tool UI.

## Description

A neutral gray canvas surrounded by panels: layers on one side, properties on the other, a toolbar along an edge. Panels are separated by tone steps and 1px borders, not by cards. UI type is compact, around the size of a label, in a neutral sans. Icons in the chrome are monochrome and one weight. The accent is the selection color, a clear blue, used when an object is selected and for a few related controls. The work on the canvas is the color. The chrome is there to be ignored until you need a control.

## Key decisions

- The canvas is the product. Panels are tools and they look like tools (`product.direction-serves-job`).
- One accent, and it means "selected" (`color.accent-rarity`).
- Compact type, aligned labels, consistent control heights. Density without ornament (`density.not-cramped`).
- Properties read as a form: label, control, next label. Not as a stack of cards (`material.hairline-before-box`).
- Chrome icons do not each invent a hue.
- The marketing site may be loud. That loudness does not leak into the editor (`product.two-registers`).

## Why it works

A creation tool has to lose. If the panels were branded, they would compete with the file. Neutral steps and a single selection color keep the eye on the object the user is editing (`hierarchy.grayscale-test` still passes, because selection is position and a ring, not only blue). Alignment of the properties column makes a dense panel scannable.

## What to steal

- Tone-on-tone panels and 1px hairlines.
- One selection color that is not also the brand wallpaper.
- A properties pattern: aligned labels, one control height, groups separated by a gap or a hairline.
- Monochrome toolbar icons.
- Compact UI type (12–14px) only where the user is operating, not where they are reading prose. Keep `a11y.contrast` and do not put a paragraph at 11px.
- A hard line between the marketing register and the tool register.

## What not to copy

- This panel layout on a blog, a shop, or a landing page. A properties sidebar next to an essay is a costume.
- Tiny type for reading. Compact is for controls.
- A second and third blue. Selection, links, and primary actions can share one hue; illustrations on the canvas do not count against the budget.
- The marketing site's illustrations, gradients, or campaign type, imported into a tool "for consistency."
- Figma's specific blue as your brand accent. The lesson is the role, not the paint.

## Uniqueness

Things is a list of the user's sentences. Stripe Docs is a document. Figma is the gallery's example of chrome that must be quieter than the user's work. Load it when you are styling an editor, a canvas, a timeline, or a properties surface.

## Product fit

Editors, canvases, inspectors, timelines, any tool where the user's artifact is on screen beside the controls.

A poor fit for retail, cinema, and essays. Those screens are the artifact. They should not wear an inspector.

## Source note

`confidence: high` for the structure, which has been stable and public for years: left layers, canvas, right properties, neutral chrome, one selection blue, monochrome icons. `confidence: medium` for any specific hex or type size, which this file does not fix. The marketing site is out of scope on purpose.
