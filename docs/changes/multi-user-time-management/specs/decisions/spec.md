# Capability: decisions

## First-Principles Delta

Decision records contain judgment, dissent, and responsibility. Ownership must protect the recorder's decision journal while preserving the distinction between recorder and assignee.

## Modified Requirements

### Requirement: User-scoped decisions
Each decision SHALL carry indexed `user_id` ownership representing the recorder. All decision endpoints SHALL filter by `current_user.id`.

### Requirement: Free-text assignee remains descriptive
The `assignee` field SHALL remain free text in v1 and SHALL NOT grant access to another user's account or create notifications.

#### Scenario: Assignee is another user
- **WHEN** user A writes user B's name in `assignee`
- **THEN** the decision remains owned by user A and user B does not gain record access.

## Preserved Methodology

Problem type, boundary conditions, right answer, compromise, dissent, assignee, feedback, and outcome remain the core decision record.

## Acceptance Signal

Each user can maintain private decision records while manager dashboards expose only aggregate open and implemented counts.
