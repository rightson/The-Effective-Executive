# Capability: time (MODIFIED)

## MODIFIED Requirements

### Requirement: User-scoped time entries
Every time-entry row SHALL carry `user_id` (NOT NULL, FK to `users.id`, indexed). All `GET/POST/PUT/DELETE /api/time-entries` and `GET /api/time-entries/analysis` requests SHALL be scoped to `current_user.id`.

#### Scenario: Cross-user read
- **WHEN** user A requests `GET /api/time-entries/{id}` for an entry owned by user B
- **THEN** the response is `404` (not `403` — we do not leak existence).

#### Scenario: Cross-user write
- **WHEN** any write carries an explicit `user_id` in the body
- **THEN** the field is ignored; the row is owned by `current_user`.

## UNCHANGED
- The diagnostic fields, categories, and analysis math.
- Consolidated-block threshold of 90 minutes.
