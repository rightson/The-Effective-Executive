# Capability: decisions

## Purpose

Turn consequential judgment into effective action by defining the problem, setting boundary conditions, considering dissent, assigning responsibility, and checking reality.

## First Principles

- Executives are paid for judgment on consequential matters, not for making many decisions.
- Recurring problems require principles, policies, or process changes; treating them as one-off cases preserves dysfunction.
- A decision is not real until someone is responsible for action.
- Feedback from reality is required because reports and assumptions can be wrong.
- Dissent improves decision quality by exposing alternatives and hidden assumptions.

## Core User Actions

1. Define the decision and problem type.
2. State boundary conditions before debating options.
3. Name the right answer before compromise.
4. Record dissent or the absence of dissent.
5. Assign action and define feedback.
6. Review outcome against assumptions.

## Requirements

### Requirement: User-scoped decision records
Because decision records are part of the user's judgment practice, each decision SHALL belong to `current_user`. The free-text `assignee` field describes the person responsible for action and is not linked to an account in v1.

Each decision SHALL include:
- `title`;
- `problem_type`;
- `boundary_conditions`;
- `right_answer`;
- `compromise`;
- `assignee`;
- `feedback_mechanism`;
- `has_dissent`;
- `status`;
- `outcome`.

### Requirement: Problem type distinction
Because generic problems require rules rather than repeated exceptions, `problem_type` SHALL distinguish `generic` from `unique`.

#### Scenario: Generic problem
- **WHEN** `problem_type` is `generic`
- **THEN** the UI SHOULD ask what principle, policy, process, or system change prevents repeated case-by-case handling.

### Requirement: Boundary conditions before options
Because options cannot be judged before minimum success conditions are known, a decision with empty `boundary_conditions` SHALL be considered incomplete.

### Requirement: Right answer before compromise
Because premature compromise produces incoherent choices, the system SHALL separate `right_answer` from `compromise`.

#### Scenario: Compromise without right answer
- **WHEN** `compromise` is filled and `right_answer` is empty
- **THEN** the UI SHOULD prompt the user to define the uncompromised answer.

### Requirement: Action commitment
Because a decision without action is only an opinion, open decisions without `assignee` SHALL be counted as pending implementation.

The product SHOULD also capture or prompt for:
- due or review date;
- needed resources or authority;
- people who must be informed;
- feedback mechanism.

### Requirement: Dissent discipline
Because disagreement reveals assumptions, `has_dissent = false` SHOULD trigger a review prompt for high-impact or hard-to-reverse decisions. It SHALL NOT block saving.

### Requirement: Feedback and outcome
Because effectiveness is checked against reality, each implemented decision SHOULD have `feedback_mechanism` and later `outcome`.

#### Scenario: Implemented without feedback
- **WHEN** a decision is marked implemented without `feedback_mechanism`
- **THEN** the UI SHOULD ask how the result will be checked.

## Artifacts

- decision record;
- generic-problem principle or process note;
- action owner list;
- dissent flag;
- feedback mechanism;
- outcome review.

## Non-Goals

- meeting minutes as a substitute for decisions;
- voting or consensus tracking;
- maximizing decision speed for irreversible choices;
- assigning work to other accounts in v1.
