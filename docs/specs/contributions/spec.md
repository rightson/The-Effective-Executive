# Capability: contributions

## Purpose
Force every planned activity to declare its expected outward outcome before it starts.

## Requirements

### Requirement: Contribution CRUD
`GET/POST/PUT/DELETE /api/contributions` SHALL be exposed.

### Requirement: Layer classification
`layer` SHALL be one of `direct_results | values | talent`.

### Requirement: Status lifecycle
`status` SHALL be one of `planned | active | completed | cancelled`. Default: `planned`.

### Requirement: Outcome fields
Each row SHALL store `expected_outcome` (set at creation) and `actual_outcome` (filled on completion). Both default to empty string.

#### Scenario: Create with no expected outcome
- **WHEN** `POST` omits `expected_outcome`
- **THEN** the row is created with empty string (the UI is responsible for warning the user; the API does not block).
