# Capability: dashboard

## Purpose
Roll the five modules into a single read-only view.

## Requirements

### Requirement: Aggregate endpoint
`GET /api/dashboard` SHALL return a JSON object with the keys `time`, `contributions`, `priorities`, `decisions`.

### Requirement: Time block
`time` SHALL contain `total_hours` (rounded to 1 dp), `total_entries`, `undiagnosed`, `by_category`.

### Requirement: Contributions block
`contributions` SHALL contain `total`, `planned`, `active`, `completed` counts.

### Requirement: Priorities block
`priorities` SHALL contain `total`, `active`, and `to_abandon` (active rows where `would_start_today is False`).

### Requirement: Decisions block
`decisions` SHALL contain `total`, `open`, `implemented` counts.
