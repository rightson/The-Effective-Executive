# Capability: time

## Purpose
Help the user discover where time actually goes before trying to manage it. The module SHALL produce factual time evidence, deletion candidates, delegation candidates, other-wasting work, and protected blocks for knowledge work.

## Requirements

### Requirement: User-scoped time entries
Every time-entry row SHALL carry `user_id` (NOT NULL, FK to `users.id`, indexed). All `GET/POST/PUT/DELETE /api/time-entries` and `GET /api/time-entries/analysis` requests SHALL be scoped to `current_user.id`.

#### Scenario: Cross-user read
- **WHEN** user A requests `GET /api/time-entries/{id}` for an entry owned by user B
- **THEN** the response is `404` (not `403` — we do not leak existence).

#### Scenario: Cross-user write
- **WHEN** any write carries an explicit `user_id` in the body
- **THEN** the field is ignored; the row is owned by `current_user`.

### Requirement: Actual-time capture
The service SHALL record actual time, not intended calendar plans. Each entry SHALL include `activity`, `duration_minutes`, `category`, `timestamp`, and optional notes.

The UI SHOULD make capture fast enough for 15- or 30-minute granularity while allowing longer entries for continuous work blocks.

#### Scenario: End-of-day reconstruction
- **WHEN** a user records several time entries after the fact
- **THEN** the system SHOULD let the user set the actual timestamp and duration rather than forcing the current time.

### Requirement: Drucker time diagnosis
Each time entry SHALL support the three diagnostic questions:
- `worth_doing`: if this were not done at all, would there be serious consequences?
- `can_delegate`: could another person do this at least as well enough?
- `wastes_others`: did this activity consume other people's time without contribution?

Entries with any unanswered diagnostic SHALL count as undiagnosed.

#### Scenario: Worthless work
- **WHEN** `worth_doing` is `false`
- **THEN** the entry SHALL appear in an elimination list during review.

#### Scenario: Delegable work
- **WHEN** `can_delegate` is `true`
- **THEN** the entry SHALL appear in a delegation list during review.

#### Scenario: Other-wasting work
- **WHEN** `wastes_others` is `true`
- **THEN** the entry SHALL appear in a stop-wasting-others list during review.

### Requirement: Time analysis
`GET /api/time-entries/analysis` SHALL return:
- `total_minutes`;
- `by_category`;
- diagnosis counts for diagnosed entries, worth-doing entries, delegable entries, and other-wasting entries;
- `consolidated_minutes`.

The consolidated-block threshold SHALL be 90 minutes. The product SHALL treat these blocks as usable knowledge-work capacity, not as a productivity score.

### Requirement: Consolidation guidance
The weekly review SHALL help the user convert fragmented time into larger discretionary blocks.

#### Scenario: No consolidated time
- **WHEN** a user has time entries but `consolidated_minutes` is zero
- **THEN** the dashboard SHOULD prompt the user to reserve at least one 90-minute block for a current contribution or priority.

### Requirement: Category discipline
Categories SHOULD distinguish outcome-producing work from coordination, maintenance, administration, learning, and interruptions. The service SHOULD avoid category sets that imply every activity is equally valuable.

### Requirement: Review outputs
The module SHALL support four outputs from time review:
- a time inventory;
- an elimination list;
- a delegation list;
- a consolidated-work-block plan.
