# Capability: dashboard (MODIFIED)

## MODIFIED Requirements

### Requirement: Self dashboard
`GET /api/dashboard` (no query params) SHALL return the rollup for `current_user`. Shape unchanged.

## ADDED Requirements

### Requirement: Manager dashboard view
`GET /api/dashboard?user_id=<id>` SHALL return the rollup for the target user iff the caller is a `manager` in an org the target also belongs to. Otherwise `403`.

#### Scenario: Self via query param
- **WHEN** `?user_id=<self.id>` is passed
- **THEN** the response is identical to the no-param call.

### Requirement: Org members listing
`GET /api/org/members` SHALL return the union of members in every org where the caller has `role=manager`, as `[{user_id, display_name, org_id}]`. Used by the SPA to populate the manager picker.

## UNCHANGED
- The four blocks (`time`, `contributions`, `priorities`, `decisions`) and their fields.
