# Capability: strengths

## Purpose
Register strengths (own and others') with evidence so work can be assigned to the shape of the person.

## Requirements

### Requirement: Strength CRUD
`GET/POST/PUT/DELETE /api/strengths` SHALL be exposed.

### Requirement: Owner field
Each strength SHALL carry an `owner` string (default `"self"`) so strengths of others can be tracked.

### Requirement: Evidence field
Each strength SHALL carry a free-text `evidence` field. The methodology requires evidence; the API does not enforce non-empty.
