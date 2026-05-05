# Change: owned habit records

**Status:** accepted
**Owner:** rightson
**Branch:** `claude/multi-user-time-management-JsFIn`

## First-Principles Problem

Drucker's system requires a user to build reliable evidence and act on it repeatedly. The product must therefore protect the method's core operations:

1. **Time diagnosis must be honest.** The user needs a private journal where actual time, waste, delegation candidates, and other-wasting work can be recorded without turning into performance theater.
2. **Contribution and priority review must be attributable.** The system must know whose commitments, strengths map, posteriorities, and decisions are being reviewed.
3. **Manager visibility must serve coaching, not ownership.** A manager may need to see habit-health gaps, but raw reflection remains the user's record.

The failure mode is methodological: if identity, ownership, and visibility boundaries are unclear, users will either avoid honest diagnosis or the product will drift into generic task surveillance.

## Behavior Change

After this change:

- every time entry, contribution, strength, priority, and decision is owned by exactly one user;
- a manager can see read-only dashboard rollups for reports in a shared org;
- raw records remain private unless a future sharing capability explicitly changes that boundary;
- writes always target the authenticated user.

## System Change

1. Add an `accounts` capability: users, password auth, sessions, orgs, and org memberships.
2. Add `user_id` ownership to every domain row.
3. Scope every list, read, update, delete, analysis, and dashboard query by `current_user`.
4. Add manager dashboard authorization through shared org membership.
5. Use Postgres plus Alembic migrations for durable habit evidence.
6. Keep domain API ownership implicit so clients do not send `user_id` for writes.

## Boundaries

- Account and org support does not turn the product into a task tracker.
- Manager access is aggregate coaching visibility, not raw surveillance.
- Assignees on decisions remain free text in v1.
- No real-time collaboration, comments, notifications, SSO, or mobile app.
- Existing SQLite files are imported through a one-shot script only to preserve prior habit evidence.

## Impact

- **Specs added:** `accounts`
- **Specs modified:** `platform`, `time`, `contributions`, `strengths`, `priorities`, `decisions`, `dashboard`
- **Data model:** every domain table gains `user_id`
- **Persistence:** Postgres and Alembic preserve durable habit records
- **UI:** login, signup, auth guard, and manager dashboard picker

## Acceptance

- A new user signs up, logs in, creates domain records, and sees only their own records.
- A second user cannot read or mutate the first user's raw records through API requests.
- A manager in a shared org can view a report's dashboard rollup.
- A non-manager or unrelated user receives `403` for another user's dashboard.
- Write endpoints ignore any attempt to target another `user_id`.
- A legacy SQLite database can be imported under a chosen account.
