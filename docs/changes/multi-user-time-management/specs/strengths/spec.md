# Capability: strengths

## First-Principles Delta

Strengths maps are judgment records about how work should be placed. Ownership must keep the recorder's map private while allowing `owner` to describe any person whose strength is being evaluated.

## Modified Requirements

### Requirement: User-scoped strengths
Each strength SHALL carry indexed `user_id` ownership. All strengths endpoints SHALL filter by `current_user.id`.

The existing `owner` field SHALL remain a descriptive field and SHALL NOT imply account ownership.

#### Scenario: Strength about another person
- **WHEN** user A records a strength with `owner = "Pat"`
- **THEN** the record still belongs to user A's journal.

## Preserved Methodology

Evidence-backed strengths and strength-to-work fit remain the core behavior.

## Acceptance Signal

A user can maintain a private strengths map for self and collaborators without exposing it as shared org data.
