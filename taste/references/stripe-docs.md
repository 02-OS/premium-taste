---
id: stripe-docs
title: Stripe Docs
url: https://docs.stripe.com
direction: precise-technical
tags:
  - docs
  - measure
  - toc
  - code-as-material
  - three-zones
job: read and copy a technical document
medium: website
confidence: high
observed: 2026-11
---

# Stripe Docs

**Tags:** `precise-technical` `docs` `measure` `toc` `code-as-material` `three-zones`

docs.stripe.com. The homepage at stripe.com is a different, more graphic product. Do not import it because you loaded this file.

## Description

Three zones. A navigation column of the documentation, a reading column with a title and a short dek, and a rail of the headings on this page. Prose has a measure. Code sits in a quiet well, visually a different material from the paragraph, and it is something you are meant to copy. Language choice is a control for the sample, not a visual motif. The page is a document: title, introduction, then sections. There is no hero, no logo cloud, and no feature grid.

Stripe's brand hue appears as a link and action color. That hue has since become a default in unrelated products. The lesson in this file is the document structure, not the purple.

## Key decisions

- A documentation page is a document (`density.match-job`). The first screen is a title and the start of the answer.
- Three zones, each with one job: where else can I go, what am I reading, where am I in this page.
- The reading column is capped. The margins and the rails can be empty (`spacing.measure`).
- Code is a material: its own surface, mono, intact indentation (`type.roles`).
- The brand color is allowed here because it is the brand. It is still not a wash behind the article (`color.accent-rarity`).
- The marketing site's gradients, diagrams, and campaign headlines stay on the marketing site (`product.two-registers`).

## Why it works

Someone arrived with a question. A title, a dek, a column, and a table of contents answer it faster than a branded experience (`hierarchy.first-screen`). The code well makes the part you take visually distinct without a second design language. Restraint is what keeps a long technical page from feeling like a brochure.

## What to steal

- Title, one-sentence dek, then the document. No hero.
- A measured column. A contents rail only if the page is long enough to need one.
- Code or data samples on a separate surface, in mono, with the surrounding prose in the text family.
- Navigation that is a catalog of the docs, not a brand bar of product links.
- The separation between a graphic marketing page and a reading page.

## What not to copy

- The indigo or blurple, unless you are Stripe. On a new product it trips `color.indigo-default`.
- Three columns on a short page. A rail of two links is clutter. Use the rail when the document has real sections.
- This layout for a film, a bowl, or a task list. A table of contents beside a still is a mismatch (`product.direction-serves-job`).
- Gradient bands, glowing buttons, or the stripe.com homepage illustration style, "to make the docs feel like the brand."
- Tabs, callouts, and cards on every paragraph. One callout style, used when the reader will be hurt if they miss it.

## Uniqueness

Figma's precision is a tool chrome around a canvas. Things' precision is a personal list. Stripe Docs is precision as reading: measure, rails, and a second material for code. It is in this gallery so agents stop treating "technical" as "dark dashboard." It is also here as a warning: the brand hue is now a tell when you are not this brand.

## Product fit

Documentation, API references, changelogs, long technical explanations, knowledge bases.

A poor fit for the marketing homepage of the same company, and for any screen whose subject is an image or a single object.

## Source note

`confidence: high` for the three-zone document structure, which is the public, long-standing shape of Stripe's docs. No hex values are specified, on purpose. The homepage at stripe.com is excluded so its graphic language is not mistaken for this reference.
