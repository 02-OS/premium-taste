---
id: object-detail-spread
title: Physical Object Spread & Specification Plate
type: screen
directions:
  - quiet-luxury
  - precise-technical
job: examine materials, dimensions, price, and reserve or buy one object
tags:
  - commerce
  - product
  - object
  - spread
  - dimensions
---

# Physical Object Spread & Specification Plate

Treat one physical item as a studio spread or specification plate so material facts, proportions, stock state, and the purchase action stay immediately legible.

## Layout & Hierarchy

- Anchor the first viewport with a 2-column spread: generous studio photograph or orthographic view on the left (`aspect-ratio` preserved, sharp corners or subtle 2px seam, zero decorative overlay pills), and one start-aligned factual column (`~36ch–48ch`) on the right.
- Inside the right column, stack: one quiet category/material kicker (optional), object title at regular display weight, concrete price (`tabular-nums`), one grounded paragraph naming clay/fabric/alloy and provenance, and **one** clear primary action (`Add to bag ($68)` or `Reserve from firing`).
- Below the action, present hard physical specifications (`Dimensions`, `Weight`, `Material`, `Batch / Dispatch window`) as a hairline-ruled `<dl>` definition list rather than floating pill cards (`material.hairline-before-box`).

## Required States & Mechanics

- Variant selection (Finish, Size, Edition) uses a crisp segmented control or hairline swatch list updating price, lead time, and image frame immediately without full-page jumps.
- Sold-out / waitlist state states the exact status as words (`Sold out · Next firing Dec 4`) in muted or oxide text (`a11y.not-color-alone`), replacing/disabling the primary action with a single clean notification field when needed.
- On narrow viewports (`< 768px`), render image first at full readable framing followed cleanly by the title and action within the first fold.

## What to Include

- Explicit dimensions, materials, shipping window, and return policy right in plain typography—never buried inside nested tabs or accordion traps.
- Explicit `width` / `height` on product photography (`a11y.semantics`) and high-contrast zoom view if inspecting fine grain or ports.

## What to Refuse

- Three-column "Free shipping / 30-day warranty / Secure checkout" icon tiles stacked below the hero (`material.icon-tile`).
- Countdown scarcity timers, `"14 people viewing now"` fake proof (`content.fake-proof`), or badge piles (`chrome.badge-pile`).
- Warm cream + serif applied as an empty costume without real product photography (`material.fake-media`).

## Litmus Check

- Covering nav chrome leaves the object, its material specifications, its price, and its single acquisition action unmistakable in grayscale.
