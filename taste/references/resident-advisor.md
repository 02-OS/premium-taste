---
id: resident-advisor
title: Resident Advisor
url: https://ra.co
direction: cinematic-dark
tags:
  - nightlife
  - listings
  - dense
  - black
  - red-signal
  - type-led
job: find an event tonight
medium: website
confidence: medium
observed: 2026-11
---

# Resident Advisor

**Tags:** `cinematic-dark` `nightlife` `listings` `dense` `black` `red-signal` `type-led`

The publication and listings at ra.co. Resident Advisor is an electronic-music magazine and an events guide. The reference surface is the night listing and the editorial type, not a fan redesign.

## Description

A black room, off-white type, and a bright red used as a signal. A third-party brand capture lists the red near `#FF4848` with black and an off-white; treat that as a hint, not a specification. The content is a list: city, date, venue, artist. Editorial pages use heavy grotesk headlines and photography of artists and rooms. Icons are few. The density is high because the night is a schedule, not a poster.

The Guide has been described by outside reviewers as poster-like and brutalist: pure black, pure white, heavy type, sharp contrast. That contrast is part of the voice, and it has a cost. Pure white on pure black is loud in a dark room and tires the eye.

## Key decisions

- Dark because the context is night, not because dark mode was in the brief (`product.direction-serves-job`).
- The listing is the interface. Rows of events beat a hero about events.
- Red marks a signal. It is not a wash and not a gradient.
- Type carries the page when there is no photograph. Artist names and dates are the material.
- Density is intentional. A club guide that looked like a gallery would hide the next thing on.
- Contrast is a cultural choice here. It is not a gift you copy into a reading app without softening.

## Why it works

The job is "what is on, where, and when." A dense, type-led list answers it (`density.match-job`). The red is scarce, so it can still mean "this, now" (`color.accent-rarity`). The page looks like the culture it covers, which is a stronger identity than a themed component kit.

## What to steal

- A night surface justified by the content's context.
- Rows with a stable order of facts: time, place, name.
- One saturated signal color on a field that is otherwise black and off-white.
- Heavy type for the name, quieter type for the metadata, same family.
- The courage to be dense when the user is scanning a schedule.

## What not to copy

- Pure `#000` and pure `#fff` as the default dark theme. For anything read at length, lift the black and dim the white (`color.dark-surfaces`). RA accepts the glare as a poster. Your settings screen should not.
- Red on every link, icon, and badge. Then it is no longer a signal.
- A brutalist listing for a product with nothing to list. Empty rows in a black void fail `density.not-empty`.
- Gold, blur, or a glow added "so it feels premium." That undoes the listing.
- The brand's red hex on an unrelated product.

## Uniqueness

MUBI gives the still a room and is happy to turn the lights on for text. Criterion frames a library. RA is the gallery's dense night paper: many real rows, one red, almost no illustration. Reach for it when cinematic dark is in danger of becoming a single centered poster with a play button.

## Product fit

Events, programs, nightlife, a magazine whose issue is "what is happening."

A poor fit for object retail, long essays (use editorial-print or a paper band), and any form-heavy flow.

## Source note

`confidence: medium`. Long-standing public character of ra.co since the 2021 rebuild, plus a third-party capture of black / off-white / red near `#FF4848`, plus outside descriptions of the Guide's pure-black poster contrast. No claim of a current CSS audit. Confirm the red before using it, and prefer not to use it outside this brand.
