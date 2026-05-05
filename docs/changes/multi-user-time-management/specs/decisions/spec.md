# Capability: decisions (MODIFIED)

## MODIFIED Requirements

### Requirement: User-scoped decisions
Each decision SHALL carry `user_id` (NOT NULL, FK, indexed) representing the recorder. All endpoints SHALL filter by `current_user.id`. The existing free-text `assignee` field is unchanged — multi-user does not (in v1) link `assignee` to a real account.

## UNCHANGED
- Five-step fields, `problem_type`, `has_dissent`, `status` lifecycle.

## DEFERRED
- Linking `assignee` to a `user_id`, and notifying that user, is a follow-up change.
