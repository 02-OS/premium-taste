---
id: pricing-table
title: SaaS Pricing & Tier Comparison
type: screen
directions:
  - precise-technical
  - quiet-luxury
job: compare plans and pick the right billing tier
tags:
  - pricing
  - billing
  - comparison
  - toggle
  - conversion
---

# SaaS Pricing & Tier Comparison

Let the buyer identify tier boundaries, per-unit costs, and upgrade triggers in under 15 seconds without guessing hidden limits.

## Layout & Hierarchy

- Open with the billing period control (`Monthly` / `Annual`, showing exact `%` or dollar delta inside the toggle label) and actual tier columns (2 columns if there are 2 tiers, 3 if 3—never pad a ghost tier).
- Set numeric prices with `font-variant-numeric: tabular-nums` and align unit subtitles (`per seat / month`) beneath the figure so billing swaps do not shift column width.
- Separate the upper plan strip from the compact specification matrix below using hairlines rather than stacking extra marketing banners between them.

## Required States & Mechanics

- Switching `Monthly` / `Annual` updates prices, totals, and query/URL hash immediately (`?billing=annual`) and keeps row heights identical.
- Emphasize at most **one** self-serve primary tier visually (1 border weight step or subtle surface shift), keeping secondary CTA treatments quieter (`chrome.two-primaries` avoided when Enterprise uses a text link or quiet outline).
- Repeat selected plan, billing cadence, and renewal terms cleanly at checkout handoff.

## What to Include

- One specific objection-killer line directly beneath each plan's primary CTA (e.g., `"No credit card for 14 days · Cancel in Settings"`).
- Hard operational limits up front (seats, retention days, rate limits) before soft feature lists.
- Dedicated procurement/security row for Enterprise (`SOC 2 Type II`, `SAML SSO`, `DPA`, `Custom SLA`) rather than hiding compliance in the footer.

## What to Refuse

- Centered hero filler or fake logo clouds pushing the plan columns below the fold (`hierarchy.first-screen`, `content.fake-proof`).
- `Most Popular` rainbow badge piles on two or more columns (`chrome.badge-pile`).
- Inaccurate `"Save 20%"` math or hiding per-seat minimums inside tooltips.

## Litmus Check

- Switching between Monthly and Annual changes only the numbers and saving string—zero vertical layout jump and zero ambiguous limit wording.
