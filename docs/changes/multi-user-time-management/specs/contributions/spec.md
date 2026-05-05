# Capability: contributions

## First-Principles Delta

Contribution commitments are personal accountability records. Ownership must keep each user's outward-result commitments separate while preserving the same contribution discipline.

## Modified Requirements

### Requirement: User-scoped contributions
Each contribution SHALL carry indexed `user_id` ownership. All contribution endpoints SHALL filter by `current_user.id`.

#### Scenario: Cross-user access
- **WHEN** user A requests a contribution owned by user B
- **THEN** the service SHALL not expose the record.

## Preserved Methodology

Contribution layers remain `direct_results`, `values`, and `talent`. Expected and actual outcome comparison remains the core review action.

## Acceptance Signal

A user can define, review, and complete contribution commitments without seeing another user's commitments.
