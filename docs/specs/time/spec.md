# Capability: time

## Purpose

Make actual time visible so the user can remove waste, delegate work, stop wasting others' time, and protect blocks large enough for knowledge work.

## First Principles

- Time is the scarcest resource because it cannot be stored, recovered, or substituted.
- People are poor judges of where their time goes from memory alone.
- Time management starts with diagnosis, not scheduling.
- Knowledge work needs consolidated blocks; fragmented fragments are often unusable for real contribution.

## Core User Actions

1. Record actual activity and duration in small factual entries.
2. Diagnose each entry with Drucker's three questions.
3. Produce elimination, delegation, and other-wasting lists.
4. Convert available time into 90-minute or larger work blocks for contribution and priorities.

## Requirements

### Requirement: User-scoped actual-time entries
Because time diagnosis must be personal and factual, every time entry SHALL belong to `current_user` and SHALL record actual work, not only intended plans.

Each entry SHALL include:
- `activity`;
- `duration_minutes`;
- `category`;
- `timestamp`;
- optional `notes`;
- `worth_doing`;
- `can_delegate`;
- `wastes_others`.

#### Scenario: Cross-user read
- **WHEN** user A requests a time entry owned by user B
- **THEN** the service SHALL return `404`.

#### Scenario: Fast capture
- **WHEN** the user records only activity, duration, and category
- **THEN** the entry SHALL be saved and counted as undiagnosed until the diagnostic questions are answered.

### Requirement: Three-question diagnosis
Because the first habit is to identify what should not consume the executive's time, each entry SHALL support these questions:

- `worth_doing`: if this were not done at all, would there be serious consequences?
- `can_delegate`: could another person do this well enough?
- `wastes_others`: did this consume other people's time without contribution?

#### Scenario: Elimination candidate
- **WHEN** `worth_doing` is `false`
- **THEN** the entry SHALL appear in the elimination list.

#### Scenario: Delegation candidate
- **WHEN** `can_delegate` is `true`
- **THEN** the entry SHALL appear in the delegation list.

#### Scenario: Other-wasting candidate
- **WHEN** `wastes_others` is `true`
- **THEN** the entry SHALL appear in the stop-wasting-others list.

### Requirement: Time analysis
Because the user needs facts rather than impressions, `GET /api/time-entries/analysis` SHALL return:

- `total_minutes`;
- `by_category`;
- diagnosis counts;
- `consolidated_minutes`.

`consolidated_minutes` SHALL count entries at or above the 90-minute usable-block threshold.

### Requirement: Consolidation prompt
Because important knowledge work requires large blocks, the weekly review SHOULD prompt the user to protect at least one 90-minute block when the user has time entries but no consolidated time.

### Requirement: Category discipline
Because categories influence interpretation, the product SHOULD distinguish outcome-producing work, coordination, maintenance, administration, learning, and interruption. Categories SHOULD NOT imply that every activity has equal value.

## Artifacts

- time inventory;
- undiagnosed entries queue;
- elimination list;
- delegation list;
- stop-wasting-others list;
- consolidated-block plan.

## Non-Goals

- maximizing logged hours;
- replacing a calendar;
- rewarding busyness;
- tracking employees minute by minute.
