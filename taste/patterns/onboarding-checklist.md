---
id: onboarding-checklist
title: Progressive Activation Onboarding Flow
type: flow
directions:
  - precise-technical
  - quiet-luxury
job: reach first meaningful product value in under three steps
tags:
  - onboarding
  - activation
  - progress
  - wizard
  - skip
---

# Progressive Activation Onboarding Flow

Defer configuration the product does not need yet and guide the user straight to their first working artifact.

## Layout & Hierarchy

- Present one primary decision per step (`1 of 3` numeric progress in tabular type) inside a focused container, avoiding heavy multi-column marketing sidebars.
- Anchor the step heading cleanly left-aligned with a visible **`Skip for now`** or **`Configure later`** text escape hatch at consistent placement.
- Move completed workspace setup to a non-blocking dismissible checklist inside the real product canvas once minimum inputs are collected.

## Required States & Mechanics

- Preserve typed choices across Back/Next step navigation and browser reload (local draft or server step state).
- Disable only invalid submission—or better, validate inline on submit/blur with field-level instructions (`a11y.errors`).
- If requesting team invites or integrations, pre-populate sensible defaults and allow skipping with zero guilt copy (`"I'll do this later"` rather than `"No thanks, I hate shipping faster"`).

## What to Include

- Concrete preview of what the choices configure (e.g., showing the live CLI command or webhook URL updating as the user picks region/framework).
- Immediate working state upon finish—land on the populated workspace, not a confetti blocker.

## What to Refuse

- Five-page interrogation forms demanding job title, company size, and attribution before showing the product.
- Fake loading screens (`"Tailoring your workspace..."`) hiding empty sleeps (`motion.purpose`).
- Dark-pattern dismiss copy.

## Litmus Check

- A user can reach an operational screen in two clicks or fewer, navigate backward without losing form state, and dismiss setup cleanly.
