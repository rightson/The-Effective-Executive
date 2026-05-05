# Capability: contributions

## Purpose
Shift the user's attention from activity, responsibility, and effort toward outward contribution. A contribution is an observable result the organization or stakeholder needs, not a description of tasks performed.

## Requirements

### Requirement: User-scoped contributions
Each contribution SHALL carry `user_id` (NOT NULL, FK, indexed). All endpoints SHALL filter by `current_user.id`.

### Requirement: Contribution definition
Each contribution record SHALL capture:
- `activity`: the planned activity or commitment;
- `expected_outcome`: the outward result expected before work starts;
- `layer`;
- `status`;
- `actual_outcome` after completion.

`layer` SHALL be one of:
- `direct_results`: delivery, revenue, quality, reliability, speed, cost, risk, or other direct organizational result;
- `values`: standards, culture, decision quality, integrity, or operating norms;
- `talent`: development of people and future capability.

#### Scenario: Activity without contribution
- **WHEN** a user creates a contribution with an empty or vague `expected_outcome`
- **THEN** the UI SHOULD keep the record visibly incomplete and ask "what observable result should happen?"

#### Scenario: Completion
- **WHEN** a contribution is marked `completed`
- **THEN** the user SHOULD record `actual_outcome` so expected and actual contribution can be compared.

### Requirement: Observable outcome standard
The service SHOULD treat a contribution as clear only when the expected outcome names at least one stakeholder, state change, metric, decision, delivery, or capability that can be observed.

Invalid examples include only-attitude language such as "be more proactive", "help the team", or "increase influence" with no result.

### Requirement: Contribution horizon
The product SHOULD support a current contribution commitment for the next 6-18 months and connect weekly activities to that commitment.

#### Scenario: No current contribution
- **WHEN** the user has active priorities but no active contribution
- **THEN** the dashboard SHALL prompt the user to define the result those priorities are meant to serve.

### Requirement: Stop-or-lower list
Each contribution definition SHOULD identify work the user will stop, delegate, or lower in quality so the promised result has capacity.

#### Scenario: New major contribution
- **WHEN** a user creates a high-importance contribution
- **THEN** the service SHOULD ask what existing work will be reduced.

### Requirement: Status lifecycle
Contribution status SHALL support at least `planned`, `active`, and `completed`. The service SHOULD make active contributions reviewable from the dashboard and SHOULD avoid encouraging more active commitments than the user can realistically support.
