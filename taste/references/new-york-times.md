---
id: new-york-times
title: The New York Times
url: https://www.nytimes.com
direction: editorial-print
tags:
  - newspaper
  - front-page
  - position
  - rules
  - photography
job: see what matters today
medium: website
confidence: high
observed: 2026-11
---

# The New York Times

**Tags:** `editorial-print` `newspaper` `front-page` `position` `rules` `photography`

The front at nytimes.com, and the story page that follows from it. Not a card grid of equal headlines, and not the print edition's exact file.

## Description

A white page. A blackletter masthead. Stories assigned to positions: a lead with a photograph, secondary stories in narrower columns, a denser index further down. Hairline rules separate them. A story page is a headline, a dek, a byline, a measured column, and captions under photographs. Photography is the color. The ground is white, not a tinted sheet.

The news faces are licensed and role-specific. Headlines descend from Cheltenham, in cuts Matthew Carter drew for the paper (the 2003 news redesign settled the headline system on that family). Labels, navigation, and credits use a gothic. Print body has used Imperial. Digital body has often been a screen serif such as Georgia. A third-party capture of the homepage in October 2026 describes editorial headlines held in a tight band, about 16–20px, with position, column span, and photography doing the ranking, plus several small uppercase labels. Treat that size band as one capture of the site, not as a spec, and do not import the label size.

## Key decisions

- The homepage is a front page. Importance is a placement, a width, and whether the story has a picture (`hierarchy.three-levels`, `hierarchy.first-screen`).
- Rules do the dividing. Stories are not cards (`material.hairline-before-box`, `material.no-nested-cards`).
- The masthead and the photograph identify the paper. Chrome does not add a brand hue (`color.budget`).
- A story page has a sequence a reader can say out loud: headline, dek, byline, then the column (`hierarchy.one-job`).
- The newsroom uses more than two families. An agent building a new product does not (`type.two-families`). Steal the assignment of roles, then stop at a serif and a sans.

## Why it works

"What matters today" is a comparison. Equal cards cannot make it, because nothing is allowed to be larger or higher or pictured (`hierarchy.grayscale-test` still has to show a lead). Position and a photograph do that work even when the type sizes stay close, which is what a 2026 capture of the site describes. Print A1 has long used weight and width inside one headline family for the same job. Either surface is a ranking. Neither surface is a template of three featured posts.

## What to steal

- A lead, then stories that are visibly secondary by width and position, then a plain index.
- Hairline rules in the ink or a soft gray. Square pictures. Captions that are captions.
- On the story: one headline, a dek, a byline in the secondary face, a column near 65–72 characters, ragged or carefully justified only if you know why.
- Two families in the product you are making. Serif for the story, sans for the byline, the nav, and the caption.

## What not to copy

- Four licensed families, or the exact webfont file names. They change, and they are not yours (`type.license`). An open serif (Source Serif 4, Newsreader) and an open sans (Public Sans) can hold the two roles.
- Uppercase labels at a size a person cannot read. The capture's tiny eyebrows fail `a11y.size` if you copy the size, and they fail `type.all-caps-everything` if every label becomes one.
- A red breaking-news mark used as the link color, the button, and the brand.
- A white card with a shadow for each story. The rule is the divider.
- The blackletter masthead as a decorative font on an unrelated product. It is their nameplate.

## Uniqueness

The Financial Times ranks a daily too, on a salmon sheet, with a numeric rail and a claret kicker. Cereal refuses the ranking and gives one place a full photograph. Monocle binds a slower briefing into named sections. The Times is a white front: the lead is where it is, the picture is the color, and the masthead is the only ornament.

## Product fit

A publication with a real editor, a daily or a magazine home, a report that must show which finding leads.

A poor fit for a single-object shop, a player, or a settings screen. Also a poor fit when every item is equally important. Do not invent a lead.

## Source note

The 2003 headline change to a Cheltenham family drawn by Matthew Carter is documented by the paper and by contemporary design reporting. Role names (Cheltenham for headlines, a gothic for labels, Imperial in print) are the long-standing public account. An October 2026 third-party capture of nytimes.com is the source for the tight homepage size band and for the claim of several concurrent webfonts. This file did not re-measure the live CSS and it publishes no hex. Print sizes and web sizes are different surfaces.
