# Capability: platform

## First-Principles Delta

The platform must protect the Drucker habit loop: raw diagnosis belongs to a specific user, durable records must remain reviewable, and manager visibility must be bounded to coaching signals. Authentication, migrations, and persistence are mechanisms for that method, not goals by themselves.

## Modified Requirements

### Requirement: Authenticated habit runtime
All `/api/*` routes except `/api/auth/*` SHALL require an authenticated session.

#### Scenario: Unauthenticated API request
- **WHEN** a request without a valid session calls a private API
- **THEN** the service SHALL return `401`.

### Requirement: Deployable persistence
Durable persistence SHALL use Postgres through SQLAlchemy 2.x, with `DATABASE_URL` selecting the database.

### Requirement: Alembic migrations
Schema changes SHALL ship as Alembic migrations. The app SHALL NOT depend on deleting and recreating production data.

### Requirement: Self-scoped writes
Domain writes SHALL derive ownership from `current_user` and ignore client-supplied `user_id`.

## Acceptance Signal

The same Drucker records can be created after login, migrated with Alembic, durably stored, and isolated by authenticated user.
