# Capability: accounts

## Purpose
Authenticate users, group them into orgs, and let managers see read-only Drucker habit rollups for coaching. Accounts SHALL protect private journals while allowing limited team visibility into habit health.

## Requirements

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

### Requirement: Identity-owned journal
Every domain record SHALL belong to exactly one user. Users SHALL NOT see another user's raw domain records through list/get endpoints.

#### Scenario: Cross-user domain lookup
- **WHEN** user A requests a domain record owned by user B
- **THEN** the service SHALL return `404` for direct record endpoints to avoid leaking existence.

### Requirement: Server-side sessions
Sessions SHALL be persisted in a `sessions` table with `id, user_id, created_at, expires_at, revoked_at`. Default lifetime: 30 days, sliding.

### Requirement: CSRF protection
State-changing endpoints (`POST/PUT/DELETE`) SHALL require a double-submit CSRF token matching a `csrf` cookie value.

### Requirement: Orgs and memberships
The service SHALL store `orgs(id, name)` and `org_memberships(user_id, org_id, role)` where `role ∈ {member, manager}`. A user MAY belong to multiple orgs.

Managers SHALL receive read-only aggregate access only where explicitly allowed by dashboard requirements. Org membership SHALL NOT grant access to another user's create, update, delete, or raw list endpoints.

#### Scenario: Manager dashboard read
- **WHEN** a manager calls `GET /api/dashboard?user_id=<report>`
- **AND** caller and target share an org where caller has `role=manager`
- **THEN** the response is the target's dashboard rollup.

#### Scenario: Manager write attempt
- **WHEN** any state-changing endpoint receives `?user_id=<other>`
- **THEN** the parameter is ignored — writes always target the caller.

### Requirement: Coaching, not surveillance
Manager-facing account features SHALL support Drucker coaching questions, not activity surveillance. The first manager surface is habit rollup visibility, not raw time-entry browsing.

#### Scenario: Manager wants detail
- **WHEN** a manager needs to discuss a user's time or priorities
- **THEN** the product SHOULD direct the manager to the aggregate gap and let the user decide what raw context to share outside the current v1 surface.

### Requirement: Password hashing
Passwords SHALL be hashed with argon2id, never stored or logged in cleartext.

### Requirement: Account lifecycle
The system SHOULD eventually support invite links, org join approval, password reset, and account export. Until those exist, their absence SHALL be documented as operational limitations rather than hidden assumptions.
