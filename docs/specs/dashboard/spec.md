# Capability: dashboard

## Purpose
Make the five Drucker habits reviewable from one place. The dashboard SHALL show whether the user is practicing the effective-executive operating loop, not merely how many records exist.

## Requirements

### Requirement: Self dashboard
`GET /api/dashboard` (no query params) SHALL return the rollup for `current_user`.

The response SHALL include:
- `user` and `is_self`;
- `time`: total hours, total entries, undiagnosed entries, and category breakdown;
- `contributions`: total, planned, active, completed;
- `priorities`: total, active, abandonment candidates;
- `decisions`: total, open, implemented.

### Requirement: Weekly review surface
The dashboard SHALL organize the user's next review actions in Drucker order:
1. diagnose time;
2. clarify contribution;
3. apply strengths;
4. reduce priorities and name posteriorities;
5. complete decisions with action and feedback.

#### Scenario: Multiple gaps
- **WHEN** a user has undiagnosed time, too many active priorities, and open decisions without implementers
- **THEN** the dashboard SHOULD present the gaps in operating-loop order, not by database table order or severity alone.

### Requirement: Habit health signals
The dashboard SHOULD compute and display habit-level signals:
- time evidence coverage and undiagnosed count;
- consolidated minutes available for knowledge work;
- active contribution clarity;
- strengths without evidence or unused strengths;
- active priority load and abandonment count;
- open decisions without owner, dissent, or feedback.

These signals SHALL be diagnostic, not gamified productivity scores.

### Requirement: Actionable callouts
Dashboard callouts SHALL point to the next concrete action, such as diagnose entries, define contribution, reserve a 90-minute block, review abandonment candidates, assign an owner, or add feedback.

#### Scenario: Empty account
- **WHEN** a new user has no records
- **THEN** the dashboard SHALL start with time capture and contribution definition rather than asking the user to fill every module.

### Requirement: Manager dashboard view
`GET /api/dashboard?user_id=<id>` SHALL return the rollup for the target user iff the caller is a `manager` in an org the target also belongs to. Otherwise `403`.

#### Scenario: Self via query param
- **WHEN** `?user_id=<self.id>` is passed
- **THEN** the response is identical to the no-param call.

### Requirement: Org members listing
`GET /api/org/members` SHALL return the union of members in every org where the caller has `role=manager`, as `[{user_id, email, display_name, org_id, org_name, role}]`. Used by the SPA to populate the manager picker.

### Requirement: Manager view boundary
Manager views SHALL remain read-only and oriented around coaching questions:
- does this person have undiagnosed time?
- are priorities overloaded or marked for abandonment?
- are decisions missing action?
- is the contribution unclear?

The manager dashboard SHALL NOT expose raw private notes unless the user explicitly shares them in a future capability.

### Requirement: No false completion
The dashboard SHALL NOT imply that a habit is complete just because at least one record exists. Completeness depends on the required diagnostic fields and review outputs for that habit.
