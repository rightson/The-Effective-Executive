# Capability: priorities (MODIFIED)

## MODIFIED Requirements

### Requirement: User-scoped priorities
Each priority SHALL carry `user_id` (NOT NULL, FK, indexed). All endpoints SHALL filter by `current_user.id`.

## UNCHANGED
- Four-criteria scoring, `would_start_today` semantics, `status` lifecycle.
