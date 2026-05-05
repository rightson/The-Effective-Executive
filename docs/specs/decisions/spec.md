# Capability: decisions

## Purpose
Record decisions in Drucker's five-step structure, surfacing dissent and the absence of an implementer.

## Requirements

### Requirement: Decision CRUD
`GET/POST/PUT/DELETE /api/decisions` SHALL be exposed.

### Requirement: Problem typing
`problem_type` SHALL be one of `generic | unique`. Default: `generic`.

### Requirement: Five-step fields
Each row SHALL carry: `boundary_conditions`, `right_answer`, `compromise`, `assignee`, `feedback_mechanism` (all free text, default empty).

### Requirement: Dissent flag
Each row SHALL carry a boolean `has_dissent` (default `false`). The methodology says a decision with no dissent is probably wrong; the API only stores the flag.

### Requirement: Status lifecycle
`status` SHALL be one of `open | implemented | reviewed`. Default: `open`. `outcome` is filled at review time.
