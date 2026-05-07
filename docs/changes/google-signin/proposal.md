---
status: active
created: 2026-05-07
---

# Change: frictionless Google sign-in

## First-Principles Problem

Drucker's habit practice depends on the user actually showing up. Friction at the front door — typing a password, or worse, pasting an ID token — discourages return visits and makes the journal sparse, which breaks the diagnostic value of the whole system.

The current "Continue with Google" button calls a browser `prompt()` and asks the user to paste a Google ID token. No real product asks this. It is a placeholder, not a sign-in.

The failure mode is methodological: if logging in is awkward, users skip a day; once skipped, time inventory becomes unreliable; once unreliable, contribution and priority review lose their evidentiary base.

## Behavior Change

After this change:

- A user clicks the Google button on the login screen, picks an account in the standard Google chooser, and lands signed in. No copy-paste, no manual token handling, no extra page.
- The Google button is rendered only when the deployment is configured for it; otherwise it stays hidden so the screen does not advertise a broken affordance.
- A first-time Google user is provisioned automatically with their verified Google email and display name.
- Returning Google users are matched by verified email and resume their existing journal.

## System Change

1. Update the `accounts` capability spec: drop `SSO in v1` from Non-Goals; add a Google sign-in requirement that the front-end SHALL use the official Google Identity Services flow, and that account provisioning SHALL key on the verified email.
2. Add `GET /api/config` returning the public `google_client_id` (or `null`) so the SPA knows whether and how to render the Google button without baking the value into the bundle.
3. Replace the `prompt()`-based handler in [static/app.js](static/app.js) with the Google Identity Services (GIS) script: render Google's official button, receive the `credential` (ID token) in the callback, and POST it to the existing `/api/auth/google` endpoint.
4. Document `GOOGLE_CLIENT_ID` setup (Google Cloud Console steps and authorized JavaScript origin) in [README.md](README.md).

The existing `/api/auth/google` ID-token verification on the server already does the right thing — that contract does not change.

## Boundaries

- Still no full OAuth Authorization Code flow with `client_secret`: GIS gives us a verified ID token via the Google chooser without a server-side callback, which keeps the deployment surface small.
- Still no account-linking UX: a Google login that matches an existing password account by email reuses that account; we do not yet expose a "link/unlink Google" affordance.
- Still no other SSO providers (Microsoft, GitHub, Apple). Adding any is a separate spec.

## Impact

- **Specs modified:** `accounts`
- **Data model:** unchanged (existing `password_hash = "!google:<sub>"` sentinel for Google-only accounts is retained)
- **API:** adds `GET /api/config`; `/api/auth/google` unchanged
- **UI:** login screen replaces custom Google button with GIS-rendered button; loads `https://accounts.google.com/gsi/client`

## Acceptance

- With `GOOGLE_CLIENT_ID` set, the login page renders the Google button on first paint and a click opens the standard Google account chooser.
- Choosing an account signs the user in without any further user action and lands on the dashboard.
- A first-time Google email creates a new user; a returning email resumes the existing user.
- With `GOOGLE_CLIENT_ID` unset, the Google button is not shown and password sign-in still works.
- No code path asks the user to paste an ID token.
