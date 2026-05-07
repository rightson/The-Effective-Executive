# Capability: accounts

## Purpose

Protect each user's Drucker journal while allowing limited organizational visibility for coaching habit practice.

## First Principles

- Honest time and decision diagnosis requires private ownership.
- Identity is necessary to make habit records attributable, private, and reviewable.
- Org membership should not imply ownership of another person's records.
- Manager access should answer habit-health questions, not expose raw activity.

## Core User Actions

1. Sign up and log in.
2. Maintain a private user-owned journal.
3. Belong to one or more orgs.
4. As a manager, view only allowed report dashboard rollups.
5. Log out and revoke the active session.

## Requirements

### Requirement: User registration
Because each journal needs an owner, `POST /api/auth/signup` SHALL accept `{email, password, display_name}` and create a user with an argon2id password hash.

#### Scenario: Duplicate email
- **WHEN** the email already exists
- **THEN** the service SHALL return `409` and create no row.

### Requirement: Password login
Because users need authenticated access across sessions, `POST /api/auth/login` SHALL verify credentials and set an `HttpOnly; Secure; SameSite=Lax` session cookie.

### Requirement: Logout
Because sessions must be revocable, `POST /api/auth/logout` SHALL revoke the current session row and clear the cookie.

### Requirement: Current user
Because the SPA and API need user context, `GET /api/auth/me` SHALL return `{id, email, display_name, orgs: [{id, name, role}]}` for the current user or `401`.

### Requirement: Server-side sessions
Because direct revocation is simpler and safer for this app, sessions SHALL be stored in a `sessions` table with `id, user_id, created_at, expires_at, revoked_at`. Default lifetime SHALL be 30 days, sliding.

### Requirement: CSRF protection
Because session cookies authenticate browser requests, state-changing endpoints SHALL require a double-submit CSRF token matching the CSRF cookie.

### Requirement: Google sign-in via Google Identity Services
Because asking a user to paste an ID token is not a real sign-in, the SPA SHALL initiate Google sign-in through the Google Identity Services client (`https://accounts.google.com/gsi/client`) and SHALL NOT prompt the user for any credential string. On a successful Google response, the SPA SHALL POST the returned `credential` (ID token) to `POST /api/auth/google`, which SHALL verify `aud` against `GOOGLE_CLIENT_ID`, require `email_verified=true`, and start a session.

#### Scenario: First-time Google user
- **WHEN** the verified Google email does not match an existing user
- **THEN** the service SHALL create a new user keyed on that email, set `display_name` from the Google profile, and start a session.

#### Scenario: Returning Google user
- **WHEN** the verified Google email matches an existing user
- **THEN** the service SHALL resume that user's account and start a session — no second account is created.

#### Scenario: Unverified Google email
- **WHEN** the Google `email_verified` claim is not true
- **THEN** the service SHALL reject the sign-in with `401`.

### Requirement: Conditional Google button rendering
Because a sign-in button that does nothing is worse than no button, the SPA SHALL render the Google sign-in button only when the deployment exposes a non-empty `google_client_id` via `GET /api/config`, and SHALL hide it otherwise.

### Requirement: Public configuration endpoint
Because the SPA must know whether Google sign-in is available without leaking secrets, `GET /api/config` SHALL return `{google_client_id: string | null}`. It SHALL NOT require authentication and SHALL NOT return any server-side secret.

### Requirement: Identity-owned records
Because private reflection needs clear ownership, every domain record SHALL belong to exactly one user.

#### Scenario: Cross-user domain lookup
- **WHEN** user A requests a raw domain record owned by user B
- **THEN** the service SHALL return `404`.

### Requirement: Orgs and memberships
Because manager coaching needs bounded access, the service SHALL store `orgs(id, name)` and `org_memberships(user_id, org_id, role)` where role is one of `{member, manager}`.

### Requirement: Manager aggregate access
Because managers need habit-health visibility but not raw journals, a manager SHALL be able to read a report's dashboard rollup only when both share an org where the caller has `role=manager`.

#### Scenario: Manager write attempt
- **WHEN** any state-changing endpoint receives `?user_id=<other>`
- **THEN** writes SHALL still target the caller.

## Artifacts

- user account;
- session record;
- org membership;
- manager report list;
- read-only dashboard authorization.

## Non-Goals

- raw manager access to another user's journal;
- account-linked assignee notifications;
- collaboration workspace semantics;
- SSO providers other than Google (Microsoft, GitHub, Apple, etc.);
- linking and unlinking Google to an existing password account through a UI affordance — Google sign-in matches existing accounts by verified email automatically.
