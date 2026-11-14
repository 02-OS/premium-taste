---
id: financial-times
title: Financial Times
url: https://www.ft.com
direction: editorial-print
tags:
  - newspaper
  - salmon-paper
  - rules
  - numeric
  - size-as-rank
job: read the day's report
medium: website
confidence: high
observed: 2026-11
---

# Financial Times

**Tags:** `editorial-print` `newspaper` `salmon-paper` `rules` `numeric` `size-as-rank`

The paper and the site at ft.com, as a daily. Not a startup landing dressed in their pink.

## Description

One salmon sheet for the whole page. Ink is a soft near-black. The lead story is larger than the story beside it. Section labels and the wordmark use a claret that does not fill the buttons. Numbers in the markets line up in columns. Rules divide stories. A May 2026 capture of the homepage also shows a navy subscribe control and other UI hues in navigation and tickers. Those are product chrome. The page's idea is the colored paper, the ranked headlines, and the figures.

The 2014 redesign, directed by Kevin Wilson and Mark Leeds, introduced Financier, drawn by Kris Sowersby at Klim. Financier Display takes cues from Perpetua. Financier Text takes cues from Solus and Joanna. Metric, also Sowersby's, carries graphics and interface type. Both families are licensed retail faces.

## Key decisions

- The paper color is the canvas. It is not a tint behind a card on a white page (`color.temperature`, `material.one-system`).
- Headline size is how the front ranks importance. A quiet essay can refuse that jump. A daily cannot (`hierarchy.three-levels`, `type.scale-jumps`).
- Claret marks the paper's own name and the section kicker. It is rare (`color.accent-rarity`).
- Market moves use aligned figures (`type.numbers`). Color may reinforce a number. A word or a sign still has to say the direction (`a11y.not-color-alone`).
- Rules, not cards, separate stories (`material.hairline-before-box`).

## Why it works

A reader opening a daily is asking what changed and what is largest. Size, position, and a column of figures answer that faster than a stack of equal cards (`density.match-job`). The salmon does the brand's work across the entire surface, so the page does not need a second decorative hue to be recognizable. Cereal refuses this size ladder on purpose. The FT needs it, because the job is a ranking, not a single photograph.

## What to steal

- One sheet color for the whole view. If the product has a paper, it is the page.
- A front that makes importance obvious: one lead, then smaller stories, divided by rules.
- Numeric columns with tabular figures, a header, and a unit. Right-align the numbers.
- A serif for the story and a sans for labels, navigation, and figures. Two families (`type.two-families`).
- An accent used for the masthead and the kicker, then put away.

## What not to copy

- Financier or Metric, unless you have licensed them. Source Serif 4 or Newsreader can hold the serif role. Public Sans can hold the sans. The roles are the lesson (`type.license`).
- Salmon as a highlight on one card, or as a "warm mode" of a white app. If you take the paper, it is the background.
- Claret buttons, claret links, and a claret hero. The capture's point is how little of the page is claret.
- The rest of a homepage capture: navy pills, teal navigation, ticker greens and reds. Importing the whole UI palette produces a costume (`color.budget`).
- Their hex values as your tokens. The salmon online is widely cited as `#fff1e5`, including by the FT's own Alphaville. A May 2026 capture lists ink near `#33302e` and claret near `#990f3d`. Label them as observations.

## Uniqueness

Cereal is one photograph and a column, and it keeps type sizes close together. The New York Times ranks a daily on white, with photography and the masthead doing the brand work. Monocle is a bound briefing, sectioned and slower than a front page. The FT is the salmon sheet plus the numbers. Nothing else in this gallery has a colored paper as the entire ground.

## Product fit

A daily, a market report, a journal that ranks several stories, a research note that is actually typeset as a page.

A poor fit for a single essay with one photograph, a product page, or a tool. Salmon on a task list is a theme.

## Source note

Salmon paper since the nineteenth century is the paper's own history. The FT's Alphaville has described the online background as `#FFF1E5`. Klim's note on Financier (Kris Sowersby, 18 July 2016) documents the 2014 commission, Kevin Wilson and Mark Leeds, and the Gill models for Display and Text. Metric is the companion sans from the same designer, used for graphics. A third-party capture of ft.com dated 13 May 2026 is the source for the claret-as-kicker observation and for `#33302e` / `#990f3d`. This file did not re-measure the live CSS. Do not paste the faces or the hexes into another product.
