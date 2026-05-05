# Capability: priorities

## Purpose
Force concentration on a few important matters and make posteriorities explicit. The module SHALL help the user decide what to do first, what to delay, and what to abandon.

## Requirements

### Requirement: User-scoped priorities
Each priority SHALL carry `user_id` (NOT NULL, FK, indexed). All endpoints SHALL filter by `current_user.id`.

### Requirement: Priority criteria
Each priority SHALL be evaluated against Drucker's four concentration criteria:
- `future_oriented`: future opportunity matters more than past investment;
- `opportunity_not_problem`: the item pursues opportunity, not only problem repair;
- `own_direction`: the user is choosing direction instead of merely reacting to pressure;
- `high_meaning`: success would materially change an important result.

The service SHALL preserve each criterion as an explicit boolean rather than compressing them into a single score.

#### Scenario: Low-criteria priority
- **WHEN** a priority satisfies fewer than two criteria
- **THEN** the UI SHOULD ask whether it is maintenance work, a problem repair, or a candidate for deferral.

### Requirement: Few active priorities
The system SHOULD encourage no more than one to three active priorities at a time. It SHALL surface overload when too many active priorities compete for the same time and strengths.

#### Scenario: Too many active priorities
- **WHEN** the user has more than three active priorities
- **THEN** the dashboard SHALL prompt a portfolio review before suggesting new work.

### Requirement: Systematic abandonment
Each priority SHALL support `would_start_today`, answering: if this were not already underway, would we choose to start it now?

#### Scenario: Would not start today
- **WHEN** `would_start_today` is `false` and status is `active`
- **THEN** the priority SHALL appear as an abandonment candidate.

#### Scenario: Abandonment review
- **WHEN** an abandonment candidate is reviewed
- **THEN** the user SHALL choose whether to keep, abandon, defer, or redesign it.

### Requirement: Posteriority list
The module SHOULD maintain an explicit stop/defer list derived from abandoned priorities, time diagnosis, and new contribution commitments. A priority system without posteriorities SHALL be considered incomplete.

### Requirement: Status lifecycle
Priority status SHALL support at least `active`, `done`, and `abandoned`. The product SHOULD also support or emulate `deferred` for work intentionally postponed without pretending it remains active.

### Requirement: Capacity connection
The service SHOULD connect priorities to time and strengths:
- active priorities SHOULD have scheduled 90-minute work blocks where appropriate;
- high-priority work SHOULD identify the person or strength that gives it the best chance of success;
- priorities unrelated to current contribution SHOULD be flagged for review.
