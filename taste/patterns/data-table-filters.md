---
id: data-table-filters
title: Searchable Ledger & Filterable Data Table
type: screen
directions:
  - precise-technical
  - editorial-print
job: slice, sort, and inspect dense operational records
tags:
  - table
  - filters
  - search
  - tabular-nums
  - sorting
  - url-state
---

# Searchable Ledger & Filterable Data Table

Put the filter bar and aligned rows immediately at the top of the viewport so operators inspect, sort, and act on individual records without dashboard ceremony.

## Layout & Hierarchy

- Start on the collection title, compact filter bar (`Search`, scoped selects/tabs, active filter count), and the repeating table/list itself—no greeting banner or four summary KPI cards (`layout.dashboard-costume`).
- Share a fixed row height (minimum `40px`, comfortable `44px`), horizontal divider hairlines, and `font-variant-numeric: tabular-nums` across numeric, date, and ID columns (`density.not-cramped`, `type.numbers`).
- Left-align text columns, right-align or decimal-align counts/latencies/prices, and keep status in a consistent column with word + quiet hue mark (`a11y.not-color-alone`).

## Required States & Mechanics

- **URL state sync:** Encode active search, filters, sort column/direction, and page inside URL query parameters so reload, back button, and shared links restore exact state.
- **Sortable headers:** Use real `<button>` inside `<th scope="col">` with explicit ascending/descending `aria-sort` state indicators.
- **Responsive narrow viewport:** Pin the primary identifier and status columns or wrap the table in an accessible horizontal scroll region (`tabindex="0"`, `role="region"`) rather than hiding half the data.
- **Bulk selection (if supported):** Surface a conditional toolbar only when `>= 1` row is selected, announcing selection count politely.

## What to Include

- Explicit match count (`"14 of 208 builds shown"`) and a `Clear filters` escape hatch whenever active filters narrow results.
- Live row timestamps in a unambiguous fixed or localized `Intl.DateTimeFormat` format plus hover/title ISO timestamp for precision debugging.

## What to Refuse

- Nested rounded cards around each table row (`layout.nested-cards`, `material.gray-card-shadow`).
- Filled rainbow status pills louder than the row identifier (`color.rainbow-pills`).
- Full client-side DOM dumps exceeding 50–100 unpaginated/unvirtualized heavy rows.

## Litmus Check

- Refreshing the browser preserves filter/sort state, digits line up vertically down every column, and hiding color still leaves every row status unambiguous.
