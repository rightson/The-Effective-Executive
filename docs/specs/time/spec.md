# Capability: time

## Purpose
Log activity duration and force the three Drucker diagnostic questions, then surface consolidated-block usage.

## Requirements

### Requirement: Time-entry CRUD
The service SHALL expose `GET/POST/PUT/DELETE /api/time-entries`.

#### Scenario: Create
- **WHEN** `POST /api/time-entries` is called with `{activity, duration_minutes, category?, notes?}`
- **THEN** a row is inserted with `timestamp = utcnow()` and `worth_doing/can_delegate/wastes_others = NULL` (undiagnosed).

### Requirement: Diagnostic fields
Each entry SHALL carry the three nullable booleans `worth_doing`, `can_delegate`, `wastes_others`. `NULL` means undiagnosed.

### Requirement: Categories
`category` SHALL be one of `deep_work | meeting | admin | communication | waste | uncategorized`. Default: `uncategorized`.

### Requirement: Analysis endpoint
`GET /api/time-entries/analysis` SHALL return:
- `total_minutes`
- `by_category` map
- `diagnosis.{total_diagnosed, worth_doing, can_delegate, wastes_others}` counts
- `consolidated_minutes` — sum of duration for entries where `duration_minutes >= 90`

#### Scenario: Empty
- **WHEN** there are no entries
- **THEN** all numeric fields are `0` and maps are `{}`.
