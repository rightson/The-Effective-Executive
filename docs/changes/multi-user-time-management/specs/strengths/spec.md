# Capability: strengths (MODIFIED)

## MODIFIED Requirements

### Requirement: User-scoped strengths
Each strength SHALL carry `user_id` (NOT NULL, FK, indexed). All endpoints SHALL filter by `current_user.id`. The existing free-text `owner` field is unchanged — it still describes *whose* strength it is (self or another person), independent of *which account* recorded it.
