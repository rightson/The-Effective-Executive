# Capability: strengths

## Purpose
Help the user design work around usable strengths instead of idealized, all-around competence. The module SHALL document evidence-backed strengths for the user and relevant collaborators, then use those strengths to shape priorities and decisions.

## Requirements

### Requirement: User-scoped strengths
Each strength SHALL carry `user_id` (NOT NULL, FK, indexed). All endpoints SHALL filter by `current_user.id`. The existing free-text `owner` field is unchanged — it still describes *whose* strength it is (self or another person), independent of *which account* recorded it.

### Requirement: Evidence-backed strength record
Each strength SHALL include:
- `owner`: the person or role whose strength is being recorded;
- `name`: the strength;
- `description`: where the strength is useful;
- `evidence`: observed performance facts.

#### Scenario: Unsupported claim
- **WHEN** a strength has no evidence
- **THEN** the UI SHOULD mark it as incomplete and ask for a concrete example of superior performance.

### Requirement: Work-fit guidance
The service SHOULD help the user connect strengths to work. A strength is useful when it can be applied to a contribution, priority, or decision action.

#### Scenario: Priority without strength fit
- **WHEN** a high-priority item has no obvious person or strength fit
- **THEN** the review flow SHOULD ask whether the work is assigned to the right person or needs a different design.

### Requirement: Weakness boundary
The module SHALL distinguish ordinary weaknesses from trust, integrity, or responsibility failures.

Ordinary weaknesses SHOULD be handled through task design, pairing, process boundaries, or reduced exposure. Trust, integrity, and basic responsibility problems SHALL NOT be treated as configurable weaknesses.

### Requirement: Self-management facts
For the current user, the service SHOULD capture effective work-mode facts such as:
- thinking best through writing or conversation;
- stronger at exploration or closure;
- stronger at architecture, execution, operations, analysis, or communication;
- required decision-analysis depth;
- conditions that reliably produce high-quality work.

These facts SHOULD be used by the dashboard when suggesting focus blocks or reviewing assignments.

### Requirement: Strengths map output
The module SHALL produce a strengths map answering:
- what each key person can do unusually well;
- where current responsibilities use or waste those strengths;
- which weaknesses require process, partner, or boundary controls.
