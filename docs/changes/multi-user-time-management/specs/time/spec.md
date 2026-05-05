# Capability: time

## First-Principles Delta

Time evidence must be honest and personal. Ownership must prevent one user's time inventory from leaking into another's while keeping the diagnostic habit unchanged.

## Modified Requirements

### Requirement: User-scoped time entries
Every time entry SHALL carry indexed `user_id` ownership. All time entry CRUD endpoints and time analysis SHALL filter by `current_user.id`.

#### Scenario: Cross-user read
- **WHEN** user A requests a time entry owned by user B
- **THEN** the service SHALL return `404`.

#### Scenario: Cross-user write attempt
- **WHEN** a request body includes `user_id`
- **THEN** the service SHALL ignore it and assign ownership to `current_user`.

## Preserved Methodology

The three time-diagnosis questions and 90-minute consolidated-block analysis remain unchanged.

## Acceptance Signal

Each user sees only their own time inventory, elimination candidates, delegation candidates, and consolidated-block analysis.
