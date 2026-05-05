# Capability: dashboard

## Purpose

Expose breaks in the effective-executive loop and guide the weekly review in Drucker order. The dashboard is a diagnostic surface, not a scorecard.

## First Principles

- The five habits are interdependent. A downstream record can be misleading when upstream evidence is missing.
- The user needs visible next actions, not passive totals.
- Dashboard metrics should expose practice gaps, not gamify productivity.
- Manager visibility must support coaching questions without turning private journals into surveillance.

## Core User Actions

1. See the next review action.
2. Diagnose time before rearranging work.
3. Confirm contribution before judging priorities.
4. Check strength fit before assigning important work.
5. Review overload, posteriorities, and open decisions.
6. For managers, inspect only habit rollups for coaching.

## Requirements

### Requirement: Self dashboard rollup
Because the user needs one review surface, `GET /api/dashboard` SHALL return the rollup for `current_user`.

The response SHALL include:
- `user` and `is_self`;
- `time`: total hours, total entries, undiagnosed entries, and category breakdown;
- `contributions`: total, planned, active, completed;
- `priorities`: total, active, abandonment candidates;
- `decisions`: total, open, implemented.

### Requirement: Drucker-order review
Because time evidence precedes contribution and priority judgment, dashboard prompts SHALL be ordered by the operating loop:

1. diagnose time;
2. clarify contribution;
3. apply strengths;
4. concentrate priorities and name posteriorities;
5. complete decisions with action and feedback.

#### Scenario: Multiple gaps
- **WHEN** the user has undiagnosed time, too many priorities, and open decisions
- **THEN** the dashboard SHOULD present the review in loop order rather than table order.

### Requirement: Habit health signals
Because one record does not prove habit practice, the dashboard SHOULD surface:
- undiagnosed time;
- consolidated minutes;
- missing active contribution;
- strengths without evidence;
- active priority overload;
- abandonment candidates;
- decisions without owner, dissent, feedback, or outcome.

### Requirement: Actionable callouts
Because effectiveness is built through action, each callout SHOULD link to a concrete next step such as diagnose entries, define contribution, add evidence, review abandonment, assign owner, or add feedback.

### Requirement: Empty-account start
Because users should not fill every module before receiving value, a new user SHALL be guided first toward time capture and contribution definition.

### Requirement: Manager dashboard view
Because managers may coach habit practice without owning another user's journal, `GET /api/dashboard?user_id=<id>` SHALL return the target user's rollup only when the caller is a manager in a shared org. Otherwise it SHALL return `403`.

#### Scenario: Self via query param
- **WHEN** `?user_id=<self.id>` is passed
- **THEN** the response SHALL match the no-param dashboard.

### Requirement: Org members listing
Because the manager picker needs a bounded target list, `GET /api/org/members` SHALL return members in orgs where the caller has `role=manager`.

### Requirement: Manager visibility boundary
Because coaching is not surveillance, manager views SHALL remain read-only aggregate rollups. They SHALL NOT expose raw private notes or raw time-entry lists in v1.

## Artifacts

- weekly review queue;
- habit health signals;
- next-action callouts;
- self dashboard;
- manager read-only rollup.

## Non-Goals

- productivity score;
- employee surveillance;
- raw manager access to private notes;
- replacing one-on-one coaching conversations.
