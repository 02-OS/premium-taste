---
id: editorial-longform
title: Single-Column Essay & Dispatch Reading View
type: screen
directions:
  - editorial-print
job: read an argument or report cleanly without modal interruptions
tags:
  - article
  - essay
  - longform
  - serif
  - measure
---

# Single-Column Essay & Dispatch Reading View

Respect the reader's sustained attention with a deliberate line measure (`60ch–72ch`), clear structural hierarchy between masthead, standfirst, prose, and quiet captions, and zero pop-up interruptions.

## Layout & Hierarchy

- Start with a concise top masthead (`ui` sans, 1px `ink` or `hairline` bottom rule), publication date/category line, display headline (`1.12–1.18` leading), factual dek, byline, and optionally one lead photograph with an attributed caption in smaller sans beneath it.
- Keep running prose in serif at `18px–20px` with `1.5–1.6` line-height, ragged right (never justified on screen), capped strictly at `62ch–70ch` (`spacing.measure`).
- Reserve side-margins (or footnote/figure rail on wide desktop viewports) for figure numbers, citations, or inline clarifications rather than trapping prose in a bordered card.

## Required States & Mechanics

- Footnotes, references, and `#section` anchors set `scroll-margin-top` above any sticky bar (`a11y.semantics`) and highlight target paragraphs gently when jumped to.
- Preserve browser native text selection, Cmd+F, reader mode, and zoom cleanly.
- If displaying related dispatches at the end of the piece, separate with one full-column `1px` rule and factual title + date + reading time list (`hierarchy.alignment`), not rounded card carousels.

## What to Include

- Clear distinction between prose (`serif`) and apparatus—captions, dates, credits, footnotes (`sans` / `mono`).
- Specific image/diagram attribution and caption describing *what* the plate shows rather than generic filler (`content.abstract-verbs`).

## What to Refuse

- Newsletter modal gates popping over paragraph 2, sticky floating share sidebars overlapping text, or inline animated gradients.
- Combining oversized drop caps, pull-quote cards, italic highlight boxes, and textured paper overlays on one screen (`uniqueness.one-detail`).
- Reading text below `16px` (`a11y.size`).

## Litmus Check

- Print/gray mode retains effortless reading cadence across a 1,500-word article, every link is distinguishable by underline, and zero banners overlap any sentence on desktop or mobile.
