# Capability: accounts (delta)

## First-Principles Delta

A login that requires copy-pasting an ID token is not a login. The accounts capability protects honest journaling, and that protection is meaningless if the user gives up at the door. SSO via Google therefore moves from "out of scope" to a first-class authentication path, on the same first principle that made password auth in scope: the user must be able to come back.

## Removed Non-Goals

- `SSO in v1` — withdrawn. The original spec deferred SSO when only password auth existed; the product now needs a frictionless return path, and the Google ID-token verification path is already implemented server-side.

## Added Requirements

### Requirement: Google sign-in via Google Identity Services
Because asking a user to paste an ID token is not a real sign-in, the SPA SHALL initiate Google sign-in through the Google Identity Services client (`https://accounts.google.com/gsi/client`) and SHALL NOT prompt the user for any credential string. On a successful Google response, the SPA SHALL POST the returned `credential` (ID token) to `POST /api/auth/google`, which establishes a session.

#### Scenario: First-time Google user
- **WHEN** the verified Google email does not match an existing user
- **THEN** the service SHALL create a new user keyed on that email, set `display_name` from the Google profile, and start a session.

#### Scenario: Returning Google user
- **WHEN** the verified Google email matches an existing user (whether previously created via password or Google)
- **THEN** the service SHALL resume that user's account and start a session — no second account is created.

#### Scenario: Unverified Google email
- **WHEN** the Google `email_verified` claim is not true
- **THEN** the service SHALL reject the sign-in with `401`.

#### Scenario: Audience mismatch
- **WHEN** the ID token `aud` does not match the configured `GOOGLE_CLIENT_ID`
- **THEN** the service SHALL reject the sign-in with `401`.

### Requirement: Conditional Google button rendering
Because a sign-in button that does nothing is worse than no button, the SPA SHALL render the Google sign-in button only when the deployment exposes a non-empty `google_client_id` via `GET /api/config`, and SHALL hide it otherwise.

### Requirement: Public configuration endpoint
Because the SPA must know whether Google sign-in is available without leaking secrets, `GET /api/config` SHALL return `{google_client_id: string | null}`. It SHALL NOT require authentication and SHALL NOT return any server-side secret.

## Acceptance Signal

A user with a configured deployment clicks the Google button, picks an account in Google's chooser, and lands signed in on the dashboard, with no manual token handling at any step.
