---
id: auth-sign-in
title: Focused Sign-In & Verification Gate
type: screen
directions:
  - precise-technical
  - quiet-luxury
job: authenticate quickly with clear autofill and recovery paths
tags:
  - auth
  - login
  - passkey
  - form
  - autofill
---

# Focused Sign-In & Verification Gate

Remove marketing distractions and let a returning or new member sign in cleanly via password manager, passkey, or SSO without losing input state.

## Layout & Hierarchy

- Center the single clean column (`max-width: 380px–420px`) or use a crisp asymmetric 2-column frame where the right/left side carries real product context or stays honest paper (`hierarchy.center-is-ceremonial` allows one focused gate).
- Lead directly with workspace/app wordmark, task title (`Sign in to Meridian`), primary form controls, and zero promotional feature carousels.
- Separate federation buttons (`Continue with GitHub`, `Sign in with SSO`) cleanly from the email form with a labeled horizontal hairline rule (`or`).

## Required States & Mechanics

- Set strict semantic `type="email"`, `autocomplete="username"` / `"current-password"` / `"one-time-code"`, and `inputmode="numeric"` on 6-digit codes so OS autofill and password managers work smoothly.
- Provide an accessible `Show` / `Hide` password toggle (`aria-pressed`, native button) and a visible `Forgot password?` link next to the Password `<label>`, never hiding it beneath submit errors.
- Show field-level inline errors (`"Check email format: missing @"`) preserving the typed email value on submission failure.
- Support paste on OTP fields across all inputs (`onPaste` fills slots rather than blocking).

## What to Include

- Unambiguous workspace context if authenticating to a specific tenant (`Signing in to acme-prod`).
- Explicit MFA fallback recovery wording when a device key is unavailable.

## What to Refuse

- Splitting sign-in behind five bright identical social buttons (`chrome.two-primaries`).
- Disabling paste (`onPaste` preventDefault) on email, password, or OTP inputs.
- Placeholder-only input labels (`a11y.placeholder-label`).

## Litmus Check

- Password managers autofill email + password seamlessly, keyboard Tab steps from Email -> Forgot link -> Password -> Show toggle -> Submit cleanly in visual order, and an invalid attempt keeps the email populated with a clear fix.
