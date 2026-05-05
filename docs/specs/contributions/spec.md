# Capability: contributions (MODIFIED)

## MODIFIED Requirements

### Requirement: User-scoped contributions
Each contribution SHALL carry `user_id` (NOT NULL, FK, indexed). All endpoints SHALL filter by `current_user.id`.

## UNCHANGED
- `layer ∈ {direct_results, values, talent}`.
- `status` lifecycle, `expected_outcome` / `actual_outcome` semantics.
