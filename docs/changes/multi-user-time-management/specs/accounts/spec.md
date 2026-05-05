# Capability: accounts (ADDED)

## Purpose
Authenticate users, group them into orgs, and let managers see (read-only) their reports' Drucker rollups.

## ADDED Requirements

### Requirement: User registration
The service SHALL expose `POST /api/auth/signup` accepting `{email, password, display_name}` and create a new user with an argon2 password hash.

#### Scenario: Duplicate email
- **WHEN** the email already exists
- **THEN** the response is `409` and no row is created.

### Requirement: Password login
`POST /api/auth/login` SHALL accept `{email, password}`, verify the hash, and set an `HttpOnly; Secure; SameSite=Lax` session cookie.

### Requirement: Logout
`POST /api/auth/logout` SHALL revoke the current session row and clear the cookie.

### Requirement: Current user
`GET /api/auth/me` SHALL return the current user's `{id, email, display_name, orgs: [{id, name, role}]}` or `401`.

### Requirement: Server-side sessions
Sessions SHALL be persisted in a `sessions` table with `id, user_id, created_at, expires_at, revoked_at`. Default lifetime: 30 days, sliding.

### Requirement: CSRF protection
State-changing endpoints (`POST/PUT/DELETE`) SHALL require a double-submit CSRF token matching a `csrf` cookie value.

### Requirement: Orgs and memberships
The service SHALL store `orgs(id, name)` and `org_memberships(user_id, org_id, role)` where `role ∈ {member, manager}`. A user MAY belong to multiple orgs.

#### Scenario: Manager dashboard read
- **WHEN** a manager calls `GET /api/dashboard?user_id=<report>`
- **AND** caller and target share an org where caller has `role=manager`
- **THEN** the response is the target's dashboard rollup.

#### Scenario: Manager write attempt
- **WHEN** any state-changing endpoint receives `?user_id=<other>`
- **THEN** the parameter is ignored — writes always target the caller.

### Requirement: Password hashing
Passwords SHALL be hashed with argon2id, never stored or logged in cleartext.
