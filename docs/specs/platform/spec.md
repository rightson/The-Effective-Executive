# Capability: platform

## Purpose
Provide the secure, opinionated runtime for a Drucker habit system. The platform SHALL make the effective-executive workflow easy to practice repeatedly while preserving clear user isolation and keeping the product from becoming a generic task manager.

## Requirements

### Requirement: Habit operating system
The service SHALL frame all domain modules as one operating loop: time facts, contribution definition, strengths placement, priority concentration, and decision execution.

#### Scenario: First app load after login
- **WHEN** a user opens the app
- **THEN** the first screen SHALL show the dashboard review state and the next Drucker action, not an empty landing page or marketing page.

#### Scenario: Incomplete habit chain
- **WHEN** records exist in later modules but upstream evidence is missing, such as active priorities with no current contribution definition
- **THEN** the service SHOULD surface the upstream gap as a review prompt.

### Requirement: Structured records over free-form notes
The service SHALL prefer structured fields, forced choices, and small review prompts over blank notes. Free-text fields MAY exist for context, but they SHALL NOT be the only place where a required Drucker diagnostic is stored.

#### Scenario: Vague outcome
- **WHEN** a user records an expected outcome, priority, or decision using vague language only
- **THEN** the UI SHOULD prompt for an observable result, owner, metric, or review condition before treating the record as complete.

### Requirement: Weekly review mode
The product SHALL support a weekly review flow that can be completed from the dashboard without visiting every module manually.

The review mode SHALL cover:
- undiagnosed time entries;
- eliminable, delegable, and other-wasting work;
- the current contribution commitment;
- active priority count and abandonment candidates;
- strengths that should shape assignments;
- open decisions missing owner, action, dissent, or feedback.

### Requirement: Progressive capture
The service SHALL allow fast capture before full reflection. Users MAY create lightweight records during the week, and the dashboard SHALL later collect incomplete diagnostics into a review queue.

#### Scenario: Fast time capture
- **WHEN** a user only knows the activity and duration
- **THEN** they can save the entry and diagnose it later.

#### Scenario: Decision completion
- **WHEN** a decision is marked implemented
- **THEN** it SHOULD have an assignee and feedback mechanism; otherwise the UI SHOULD ask the user to complete those fields.

### Requirement: Postgres persistence (was: SQLite persistence)
The service SHALL persist all data in **Postgres** via SQLAlchemy 2.x. The connection string is read from `DATABASE_URL`. SQLite remains supported for local development only.

#### Scenario: Production start
- **WHEN** `DATABASE_URL` points at Postgres
- **THEN** the service connects on startup; missing migrations cause a hard fail with a clear message.

### Requirement: Alembic migrations (was: No migrations)
Schema changes SHALL ship as Alembic migrations. `alembic upgrade head` is required before the app accepts traffic. Deleting the database is no longer the upgrade path.

### Requirement: Authenticated API (was: Single user, no auth)
All `/api/*` routes except `/api/auth/*` SHALL require an authenticated session. Unauthenticated requests receive `401`.

### Requirement: Stable domain API
The API SHALL keep user ownership implicit. Domain create and update requests SHALL NOT require `user_id`; the authenticated session supplies ownership.

#### Scenario: Explicit user override
- **WHEN** a client sends `user_id` in a domain request body or query string for a write endpoint
- **THEN** the service SHALL ignore it and write only to `current_user`.

### Requirement: Methodology boundary
The service SHALL NOT optimize for task assignment, team chat, comments, or real-time collaboration unless those features directly support one of the five habits. Manager features SHALL remain coaching and review oriented, not surveillance oriented.

## Technical Shape
- Single-process FastAPI app on port 8000.
- SPA delivery from `static/`.
- OpenAPI at `/docs` (now requires login when called from a browser session, but stays public for tooling that passes a session token).
