# Capability: decisions

## Purpose
Turn important judgment into action with explicit problem definition, boundary conditions, dissent, responsibility, and feedback. The module SHALL reduce decision volume while improving the quality and follow-through of consequential decisions.

## Requirements

### Requirement: User-scoped decisions
Each decision SHALL carry `user_id` (NOT NULL, FK, indexed) representing the recorder. All endpoints SHALL filter by `current_user.id`. The existing free-text `assignee` field is unchanged — multi-user does not (in v1) link `assignee` to a real account.

### Requirement: Decision record structure
Each decision SHALL capture:
- `title`: the decision being made;
- `problem_type`: `generic` for recurring structural problems, `unique` for true exceptions;
- `boundary_conditions`: minimum conditions a valid decision must satisfy;
- `right_answer`: the answer before compromise;
- `compromise`: the practical adjustment, if any;
- `assignee`: the person responsible for action;
- `feedback_mechanism`: how reality will be checked;
- `has_dissent`: whether conflicting views were considered;
- `status`;
- `outcome`.

#### Scenario: Generic problem treated as one-off
- **WHEN** `problem_type` is `generic`
- **THEN** the UI SHOULD ask for the principle, policy, or process change that prevents repeated case-by-case handling.

#### Scenario: Missing boundary conditions
- **WHEN** a decision has no `boundary_conditions`
- **THEN** the decision SHALL be considered incomplete because options cannot be evaluated.

### Requirement: Correct answer before compromise
The service SHALL separate `right_answer` from `compromise`. Users SHOULD identify the answer that fits the problem before negotiating constraints.

#### Scenario: Compromise without right answer
- **WHEN** `compromise` is filled but `right_answer` is empty
- **THEN** the UI SHOULD prompt the user to define the uncompromised answer first.

### Requirement: Action commitment
A decision SHALL NOT be considered effective until action is assigned. The product SHOULD require or strongly prompt for:
- assignee;
- due date or review date;
- resources or authority needed;
- people who must be informed;
- feedback mechanism.

The current API stores `assignee` and `feedback_mechanism`; date, resources, and informed parties MAY be added as fields in a future migration or represented in structured notes until then.

#### Scenario: Open decision without owner
- **WHEN** a decision is open and `assignee` is empty
- **THEN** the dashboard SHALL count it as pending implementation.

### Requirement: Dissent discipline
The service SHALL make absence of dissent visible for important decisions. `has_dissent = false` does not block saving, but it SHOULD trigger a review prompt for high-impact or irreversible decisions.

### Requirement: Feedback review
Every decision SHOULD have a feedback date or mechanism that tests whether assumptions matched reality. Closing a decision SHOULD record `outcome`.

#### Scenario: Implemented decision without outcome
- **WHEN** a decision is marked implemented
- **THEN** the UI SHOULD ask how the result will be verified and later ask what happened.

### Requirement: Status lifecycle
Decision status SHALL support at least `open`, `implemented`, and a closed state for decisions that are no longer active. The dashboard SHALL distinguish discussion from action by highlighting decisions with no assignee or feedback.

## DEFERRED
- Linking `assignee` to a `user_id`, and notifying that user, is a follow-up change.
