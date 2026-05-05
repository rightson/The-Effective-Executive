# Capability: platform

## Purpose

Provide the runtime and product boundaries for a Drucker habit system. The platform SHALL make the five-habit loop secure, repeatable, and hard to confuse with a generic task manager.

## First Principles

- Effectiveness is a practice system. The app must lead users back to repeated diagnostic actions, not passive record keeping.
- The methodology is the product. Technical choices are subordinate to preserving the causal loop from time evidence to decision feedback.
- Private reflection is required for honest diagnosis. Identity and visibility features must preserve ownership and limit access.
- The system must produce artifacts that can be reviewed: inventories, definitions, maps, posteriorities, and decision records.

## Core User Actions

- Open the app and see the next Drucker review action.
- Capture incomplete records quickly during work.
- Return during review to complete diagnostics.
- Trust that domain records are scoped to the authenticated user.

## Requirements

### Requirement: Habit loop as the primary product shape
Because the product is meant to train effectiveness rather than collect notes, the first authenticated surface SHALL show review state and next actions across the five habits.

#### Scenario: First app load after login
- **WHEN** a user opens the app
- **THEN** the app SHALL show the dashboard review state before any marketing, landing, or generic task view.

### Requirement: Structured diagnostics over free-form notes
Because Drucker's method depends on specific questions, each capability SHALL store required diagnostics in structured fields where possible. Free-text notes MAY add context but SHALL NOT replace required diagnostic answers.

#### Scenario: Vague record
- **WHEN** a user records a contribution, priority, or decision with only vague language
- **THEN** the UI SHOULD prompt for an observable result, owner, metric, action, or review condition.

### Requirement: Progressive capture and later completion
Because knowledge workers must record facts while work is happening, the system SHALL allow lightweight capture and later surface incomplete diagnostics in review.

#### Scenario: Fast capture
- **WHEN** a user only knows an activity and duration
- **THEN** the user can save a time entry and complete the Drucker diagnosis later.

### Requirement: Authenticated API
Because reflection records are private by default, all `/api/*` routes except `/api/auth/*` SHALL require an authenticated session. Unauthenticated requests SHALL return `401`.

### Requirement: User-owned domain records
Because user isolation is required for honest reflection, domain create and update requests SHALL derive ownership from `current_user`; clients SHALL NOT set ownership through request bodies.

#### Scenario: Explicit user override
- **WHEN** a client sends `user_id` in a domain write request
- **THEN** the service SHALL ignore it and write only to `current_user`.

### Requirement: Durable persistence
Because habit evidence must survive review cycles and schema evolution, production persistence SHALL use Postgres through SQLAlchemy 2.x. SQLite MAY remain supported for local development.

#### Scenario: Production start
- **WHEN** `DATABASE_URL` points at Postgres
- **THEN** the service connects on startup and requires migrations to be current before accepting traffic.

### Requirement: Schema migrations
Because habit records are durable evidence, schema changes SHALL ship as Alembic migrations. Deleting the database SHALL NOT be the upgrade path.

### Requirement: Methodology boundary
Because generic collaboration features would dilute the practice loop, the service SHALL NOT add task assignment, chat, comments, or real-time collaboration unless they directly improve one of the five Drucker habits.

## Artifacts

- authenticated session;
- user-scoped records;
- migration history;
- dashboard review state;
- incomplete-diagnostic queue.

## Technical Shape

- FastAPI app on port 8000.
- SQLAlchemy 2.x models.
- Alembic migrations.
- Postgres for durable persistence; SQLite for local development.
- Static SPA served from `static/`.
- OpenAPI at `/docs`.

## Non-Goals

- generic project management;
- team chat or comments;
- raw surveillance of another user's journal;
- optimizing for feature parity with productivity tools.
