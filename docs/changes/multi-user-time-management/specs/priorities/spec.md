# Capability: priorities

## First-Principles Delta

Priorities express a user's current concentration of scarce time and attention. Ownership must isolate each user's priority portfolio while allowing managers to see aggregate overload and abandonment signals.

## Modified Requirements

### Requirement: User-scoped priorities
Each priority SHALL carry indexed `user_id` ownership. All priority endpoints SHALL filter by `current_user.id`.

### Requirement: Manager aggregate visibility through dashboard only
Managers MAY see priority counts and abandonment-candidate counts through an authorized dashboard rollup, but SHALL NOT receive raw priority CRUD access to another user's records.

## Preserved Methodology

Four-criteria review, `would_start_today`, active priority limits, and posteriorities remain the core behavior.

## Acceptance Signal

Each user manages their own concentration and abandonment review; managers can see only whether a report's priority system needs coaching.
