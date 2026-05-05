# Capability: contributions

## Purpose

Force the user to define effectiveness as outward contribution rather than activity, effort, or role responsibility.

## First Principles

- The executive is accountable for results outside the self: customer value, organizational performance, standards, and people development.
- Activity is not contribution unless it produces an observable state change.
- Contribution must be defined before priority and time allocation can be rational.
- A useful contribution commitment also names what will be reduced or stopped to create capacity.

## Core User Actions

1. Define the current contribution in observable outcome language.
2. Classify the contribution layer: direct results, values, or talent.
3. Compare expected outcome with actual outcome.
4. Name work to stop, reduce, delegate, or lower in quality.

## Requirements

### Requirement: User-scoped contribution records
Because contribution is part of the user's journal and accountability, each contribution SHALL belong to `current_user`.

Each contribution SHALL include:
- `activity`;
- `expected_outcome`;
- `layer`;
- `status`;
- `actual_outcome`.

### Requirement: Observable outcome standard
Because vague intention cannot guide executive action, `expected_outcome` SHOULD name at least one stakeholder, metric, delivery, decision, risk reduction, standard, or capability change.

#### Scenario: Activity without contribution
- **WHEN** a user creates a contribution with empty or vague `expected_outcome`
- **THEN** the UI SHOULD mark it incomplete and ask what observable result should happen.

### Requirement: Contribution layers
Because Drucker defines contribution more broadly than direct delivery, `layer` SHALL be one of:

- `direct_results`: delivery, revenue, reliability, quality, speed, cost, or risk result;
- `values`: standards, decision quality, integrity, culture, or operating norm;
- `talent`: growth of people and future organizational capability.

### Requirement: Current contribution horizon
Because executives need a concrete result horizon, the product SHOULD support one or a few active contribution commitments for roughly the next 6-18 months.

#### Scenario: Priorities without contribution
- **WHEN** the user has active priorities but no active contribution
- **THEN** the dashboard SHALL prompt the user to define the result those priorities serve.

### Requirement: Expected versus actual review
Because effectiveness must be tested against reality, completing a contribution SHOULD require `actual_outcome` so the user can compare promise and result.

### Requirement: Stop-or-lower list
Because contribution requires capacity, each major contribution SHOULD ask what existing work will be stopped, delegated, reduced, or intentionally done at a lower standard.

## Artifacts

- contribution definition;
- active contribution list;
- expected-versus-actual outcome review;
- stop-or-lower list.

## Non-Goals

- storing job descriptions;
- praising effort or attitude without outcome;
- tracking every task as a contribution;
- turning contribution into moral language instead of result language.
