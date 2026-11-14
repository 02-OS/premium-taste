---
id: ia-writer
title: iA Writer
url: https://ia.net/writer
direction: precise-technical
tags:
  - writing
  - column
  - focus
  - one-family
  - chrome-leaves
job: write the next sentence
medium: app
confidence: high
observed: 2026-11
---

# iA Writer

**Tags:** `precise-technical` `writing` `column` `focus` `one-family` `chrome-leaves`

The writing app by Information Architects. The marketing site is only where they explain the app. The reference is the editor.

## Description

A text column. The library is a list of files, and it can be hidden. Focus Mode, documented for the current apps, dims every sentence except the one at the cursor, or every paragraph except the current one. A separate typewriter option keeps the cursor vertically centered and does not dim the text. Statistics (words, characters, a reading time) can be turned off. The type in the column is one of their writing faces: iA Writer Mono, Duo, or Quattro. Duo is duospace. Quattro keeps wide word spacing and monospaced punctuation while letting a few letters take different widths. They were built from IBM Plex and published for other people to use. The toolbar does not compete with the paragraph.

## Key decisions

- The document is the screen (`hierarchy.one-job`). Panels leave when you are writing.
- Focus is a dimming of the text you are not in. It is not a modal, a blur overlay, or a second theme (`motion.purpose`).
- One face for the writing. Style comes from Markdown structure (a heading, a list, a link), not from a ribbon of formatting icons (`type.two-families` at its strictest: one).
- The library is a plain list of the user's files. It is not a dashboard of writing advice (`density.repeat-rhythm`).
- They ship the fonts and tell people not to rebuild the app as a costume.

## Why it works

The repeated decision is the next sentence. Anything that is not the sentence is in the way (`hierarchy.first-screen`). Dimming the surrounding lines keeps the cursor findable without hiding the context completely, which a lightbox would do. Stripe Docs needs three zones because the job is to read and copy. This job needs the zones to disappear.

## What to steal

- A single readable column, with the file's name and almost nothing else above it.
- A library that is a list, shown when you are choosing a file and gone when you are writing.
- Focus as type color: the current sentence in ink, the rest in a muted ink that still clears contrast (`color.contrast`). Do not blur the page.
- One text face drawn for long reading. Mono if the writing benefits from alignment. A proportional face if it does not.
- Preferences for the apparatus (stats, syntax color) so the default can stay quiet.

## What not to copy

- Rebuilding iA Writer. They have said not to. Use the idea in a product that has its own documents.
- Their faces on a marketing hero. The faces are for a column of writing (`type.license` still applies if you ship them; read their license).
- A hex from memory. This file does not record the app's colors. Light text on a light ground and the reverse are both offered. The identity is the column, not a theme.
- Focus Mode that removes the paragraph you need to edit. Dimming is the move. Deleting the context is not.
- A fake "distraction-free" landing: a giant wordmark, a gradient, and a download button. That is the page their chrome is trying to get away from.

## Uniqueness

Things is rows of tasks and a colored section heading. Figma is panels that must stay, because the canvas is beside them. Stripe Docs is a measure plus a contents rail plus a code well. iA Writer is the case where the precise interface succeeds by leaving. Load it when the user's own paragraph is the whole product.

## Product fit

Editors, notes, a draft, any tool whose artifact is continuous text.

A poor fit for a dashboard, a store, a settings form with many fields, or documentation that must show navigation and a code sample at once. Those jobs need the chrome this reference removes.

## Source note

Information Architects' own support pages document Focus Mode (sentence, paragraph, and typewriter scrolling) on the current Mac, Windows, and iOS apps, and document hiding the library. Their typography note describes Mono, Duo, and Quattro, the IBM Plex basis, and the request not to recreate the app. The product page is https://ia.net/writer. This file did not sample colors from a running build. No hex.
