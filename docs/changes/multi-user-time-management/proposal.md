# Change: multi-user-time-management

**Status:** accepted
**Owner:** rightson
**Branch:** `claude/multi-user-time-management-JsFIn`

## Why
The Effective Executive currently runs as a single-user, local-first journal. The methodology benefits as much from a shared team practice as from a private one — managers want to:

- See their own Drucker journal *and* know which of their reports have flagged a priority for abandonment, or have undiagnosed time.
- Co-own decisions (assignee + dissent) that today live as plain strings.
- Use the service from a phone or another laptop without copying a SQLite file around.

Single-user, no-auth, and SQLite each block this directly.

## What changes
1. Introduce an **`accounts` capability**: users, sessions, password auth (argon2). Add `user_id` to every domain row.
2. Scope every existing endpoint to `current_user`. Add a minimal **org/membership** model so a manager can see (read-only) reports' aggregates.
3. Replace SQLite with **Postgres**, add real migrations, and run the service as a multi-tenant deployable.
4. Keep the API shape stable where possible — `user_id` is implicit from the session, not in the request body.

## What does NOT change
- The methodology: the five modules, the diagnostic fields, the dashboard rollups.
- The opinionated, structured-journal stance. Multi-user does not turn this into a Jira clone.
- The static SPA at `/` keeps working; auth is layered in front.

## Impact
- **Specs added:** `accounts`
- **Specs modified:** `platform`, `time`, `contributions`, `strengths`, `priorities`, `decisions`, `dashboard` (all gain `user_id` scoping; dashboard gains a team view).
- **Breaking:** existing `effective_executive.db` is not migrated; an import script is offered.

## Out of scope
- Real-time collaboration, comments, notifications.
- SSO / OAuth providers (deferred; password auth first).
- Mobile apps.
