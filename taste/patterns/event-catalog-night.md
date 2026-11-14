---
id: event-catalog-night
title: Night Program & Curated Work Index
type: screen
directions:
  - cinematic-dark
job: browse screenings, releases, or live dates where the work carries color
tags:
  - film
  - events
  - music
  - catalog
  - listings
---

# Night Program & Curated Work Index

Build a dark listening/watching/program surface where stills, posters, schedules, and dates sit in crisp monochrome rooms—never dark-mode form templates or glowing bento grids.

## Layout & Hierarchy

- Lead either with **one featured work spread** (large sharp-cornered still carrying all the chromatic richness beside title, director/artist credit, runtime/date meta, and one quiet action) OR a **dense night listing** ordered cleanly by date/city (`Resident Advisor` discipline) using thin hairlines and tabular dates.
- Keep dark planes stepped calmly (`#141311` canvas vs `#1e1c19` raised band only where hierarchy demands separation) with warm off-white text (`#f3f0e8`) and subdued warm gray credits (`#9c978e` passing `>= 4.5:1`).
- Place dates, durations, seat counts, or showtimes in a predictable aligned column with `tabular-nums` so scanning tonight vs Friday takes one eye sweep.

## Required States & Mechanics

- Switching day/city/format filter (`All | Tonight | 35mm | Live`) updates the listing immediately in place and syncs URL parameters (`?city=london&filter=tonight`).
- Sold-out or archived screenings stay cleanly readable via explicit word status (`Sold out`, `Waitlist`), using a single muted signal hue (`clay`/`red`) sparingly as text/indicator—not neon glowing badges.
- Audio/trailer preview toggles keep explicit keyboard-focusable Pause/Mute controls cleanly separated from row navigation links.

## What to Include

- Hard artistic metadata beside each title: director/label, year, venue, duration, format (`35mm`, `Vinyl`, `Live A/V`).
- Explicit contrast-checked solid scrim or split panel whenever captions sit near dark photography (`a11y.contrast`).

## What to Refuse

- Indigo glows, purple radial blobs (`color.aurora`), rounded glass cards over blurred album art (`material.glass-on-flat`), or `"Good evening, curator"` dashboard chrome (`layout.dashboard-costume`).
- Truncating film/artist titles into 1-line ellipsis soup across narrow columns.

## Litmus Check

- Turning off imagery/posters leaves cleanly aligned tabular listings in an intentional dark room rather than glowing SaaS placeholders, and white-on-black contrast never flickers with harsh `#000000` inversion halos.
