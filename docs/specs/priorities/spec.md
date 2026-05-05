# Capability: priorities

## Purpose

Concentrate scarce time, attention, and strengths on a few matters that can produce significant results, while making posteriorities explicit.

## First Principles

- Concentration is required because important work cannot be done in leftover fragments.
- Priority without explicit posteriority does not protect capacity.
- Future opportunity matters more than past investment.
- The user must choose direction rather than merely respond to pressure.

## Core User Actions

1. List active priorities.
2. Evaluate each priority against Drucker's four criteria.
3. Keep only a few active priorities.
4. Review whether existing work would be started today.
5. Abandon, defer, or redesign work that no longer deserves resources.

## Requirements

### Requirement: User-scoped priority records
Because priorities reflect the user's current resource allocation, each priority SHALL belong to `current_user`.

Each priority SHALL include:
- `title`;
- `description`;
- `future_oriented`;
- `opportunity_not_problem`;
- `own_direction`;
- `high_meaning`;
- `would_start_today`;
- `status`.

### Requirement: Four concentration criteria
Because Drucker's priority test is qualitative judgment, each criterion SHALL remain explicit rather than hidden inside a single score.

The criteria are:
- `future_oriented`: future opportunity matters more than sunk cost;
- `opportunity_not_problem`: the item pursues opportunity, not only problem repair;
- `own_direction`: the user chooses direction instead of only reacting to pressure;
- `high_meaning`: success materially changes an important result.

#### Scenario: Weak priority
- **WHEN** a priority satisfies fewer than two criteria
- **THEN** the UI SHOULD ask whether it is maintenance, repair, deferrable work, or a candidate for abandonment.

### Requirement: Few active priorities
Because concentration is impossible with too many first-class commitments, the product SHOULD encourage one to three active priorities.

#### Scenario: Too many active priorities
- **WHEN** the user has more than three active priorities
- **THEN** the dashboard SHALL prompt a portfolio review before encouraging new commitments.

### Requirement: Systematic abandonment
Because the past should not automatically command the future, each active priority SHALL support `would_start_today`.

#### Scenario: Would not start today
- **WHEN** `would_start_today` is `false` and status is `active`
- **THEN** the priority SHALL appear as an abandonment candidate.

### Requirement: Posteriority list
Because capacity is created by deciding what not to do, abandoned or deferred priorities SHOULD produce an explicit posteriority list.

### Requirement: Capacity connection
Because a priority without time is only an intention, active priorities SHOULD be connected to consolidated time blocks and relevant strengths.

## Artifacts

- active priority list;
- four-criteria review;
- abandonment candidates;
- posteriority list;
- capacity check.

## Non-Goals

- unlimited P0 tasks;
- task backlog management;
- ranking by urgency alone;
- rewarding easy low-value wins.
