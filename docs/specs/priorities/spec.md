# Capability: priorities

## Purpose
Score each priority against Drucker's four criteria and prompt systematic abandonment.

## Requirements

### Requirement: Priority CRUD
`GET/POST/PUT/DELETE /api/priorities` SHALL be exposed.

### Requirement: Four-criteria scoring
Each row SHALL carry the booleans `future_oriented`, `opportunity_not_problem`, `own_direction`, `high_meaning`. All default to `false`.

### Requirement: Abandonment prompt
Each row SHALL carry the nullable boolean `would_start_today`. `NULL` means not yet reviewed; `false` flags the row for abandonment.

### Requirement: Status lifecycle
`status` SHALL be one of `active | abandoned | done`. Default: `active`.
