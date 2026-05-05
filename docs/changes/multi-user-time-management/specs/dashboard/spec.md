# Capability: dashboard

## First-Principles Delta

The dashboard is the safest shared surface because it exposes habit health without exposing raw private reflection. Manager rollups belong here, not in broad cross-user record access.

## Modified Requirements

### Requirement: Self dashboard
`GET /api/dashboard` without query parameters SHALL return the rollup for `current_user`.

### Requirement: Manager dashboard view
`GET /api/dashboard?user_id=<id>` SHALL return the target user's rollup only when the caller is a manager in a shared org. Otherwise it SHALL return `403`.

#### Scenario: Self via query param
- **WHEN** `?user_id=<self.id>` is passed
- **THEN** the response SHALL match the no-param call.

### Requirement: Org members listing
`GET /api/org/members` SHALL return members in orgs where the caller has `role=manager`, enabling the dashboard picker.

### Requirement: Aggregate-only manager boundary
Manager dashboard responses SHALL remain aggregate habit signals and SHALL NOT expose raw private notes or raw domain records.

## Preserved Methodology

The dashboard still reports time diagnosis, contribution state, priority overload and abandonment, and decision implementation gaps in Drucker-order review.

## Acceptance Signal

Managers can identify coaching gaps without gaining surveillance access to a report's journal.
