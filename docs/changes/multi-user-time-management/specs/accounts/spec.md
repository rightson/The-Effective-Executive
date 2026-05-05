# Capability: accounts

## First-Principles Delta

Private effectiveness practice needs identity. Without accounts, the system cannot protect honest time diagnosis or separate one user's journal from another's.

## Added Requirements

### Requirement: User registration
`POST /api/auth/signup` SHALL create a user from `{email, password, display_name}` and store an argon2id password hash.

### Requirement: Password login
`POST /api/auth/login` SHALL verify credentials and set an authenticated session cookie.

### Requirement: Logout
`POST /api/auth/logout` SHALL revoke the current session and clear the cookie.

### Requirement: Current user
`GET /api/auth/me` SHALL return the authenticated user's identity and org roles or `401`.

### Requirement: Server-side sessions
Sessions SHALL be stored in a table with `id, user_id, created_at, expires_at, revoked_at`.

### Requirement: CSRF protection
State-changing endpoints SHALL require a double-submit CSRF token.

### Requirement: Orgs and memberships
The service SHALL store org memberships with roles `{member, manager}` to authorize read-only manager dashboard rollups.

## Acceptance Signal

Two users can authenticate separately, own separate journals, and only authorized managers can view aggregate report rollups.
