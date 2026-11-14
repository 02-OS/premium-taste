---
id: things-3
title: Things 3
url: https://culturedcode.com/things/
direction: precise-technical
tags:
  - tasks
  - rows
  - platform-type
  - one-compose
  - section-color
job: see what to do today
medium: app
confidence: medium
observed: 2026-11
---

# Things 3

**Tags:** `precise-technical` `tasks` `rows` `platform-type` `one-compose` `section-color`

The Things app by Cultured Code, on Apple platforms. The marketing site is not the reference. The reference is the list you work in.

## Description

A calm light window. Tasks are rows, not cards. A checkbox column aligns down the list. The title is the user's own words, in the platform sans. Tags, dates, and notes sit quieter than the title, on the same row or just under it. Sections have colored headings: Today reads as a warm red, This Evening as a yellow, and later sections step down. Areas can carry a color the user chose. There is one compose control, the plus, rather than a hero button. Completing a task is a small check, not a page transition. The window does not look like a website.

## Key decisions

- The repeating object is a row (`density.repeat-rhythm`). A card around a sentence would add chrome to someone's own words.
- Color is assigned to meaning: a section of the day, or an area the user named. It is not painted on icons for decoration (`color.semantic-quiet`).
- One compose action, always available, never competing with a second primary (`hierarchy.one-primary-action`).
- Platform type. The app does not perform a brand font over the user's tasks (`type.roles`).
- Insets are consistent. The craft is the column of checkboxes and the gap between sections, not a texture.
- Motion confirms the check. It does not introduce the screen (`motion.purpose`).

## Why it works

The job is to read a list and mark one thing done. Rows, a single start edge, and a colored heading that means "now" make that scan fast (`hierarchy.alignment`, `density.match-job`). Because the chrome is native and quiet, the list feels finished rather than themed. This is the precise-technical antidote to the dashboard costume: there are no statistics about your tasks above the tasks.

## What to steal

- Rows for repeated text objects. Cards only when the object has a real body (an image, a document).
- One compose control.
- Color tied to a user-meaningful group, used in the heading, not in a badge on every row.
- A platform or system sans for a tool whose content is the user's writing.
- A small, specific confirmation when an action completes.
- Section gaps that are clearly larger than the gap inside a section.

## What not to copy

- The Today red and the Evening yellow as a brand palette for a bank or a store. Those hues mean time of day inside this app.
- A sidebar plus a plus button pasted onto a marketing page (`product.two-registers`).
- "Craft" as a drop shadow and a blur. Things is flat and aligned.
- Their information architecture (Today, Upcoming, Anytime, Someday, Areas) unless the product is actually a personal task list.
- A second accent for tags, priorities, and icons. The heading color is already the accent.

## Uniqueness

Figma is a dense creation tool whose chrome must disappear beside a canvas. Stripe Docs is a document with a table of contents. Things is a personal list: few type sizes, almost no chrome, color used as a chapter mark. Use it when a "dashboard" request is actually a list of the user's own items.

## Product fit

Task lists, inboxes, reading lists, any single-user list of short text objects.

A poor fit for a brand homepage, a film, or a data grid with many numeric columns (those numbers want mono and a stricter table).

## Source note

`confidence: medium`. Long-standing structure of Things 3 as shipped by Cultured Code: rows, checkbox column, Today / This Evening section colors, area color, a single plus, platform typography on Apple. Exact hex values are deliberately omitted. Confirm details against the current app before citing a pixel.
