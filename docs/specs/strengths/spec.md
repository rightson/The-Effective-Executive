# Capability: strengths

## Purpose

Help the user place work where strengths can produce results and design around weaknesses that do not violate trust.

## First Principles

- No person is well rounded enough to be managed as an ideal role description.
- Results come from using strengths, not from averaging out weaknesses.
- Weaknesses can often be bounded by design, pairing, process, or role shape.
- Failures of integrity, trust, or responsibility are not ordinary weaknesses and cannot be designed around.

## Core User Actions

1. Record strengths with observed performance evidence.
2. Identify the work each strength is suitable for.
3. Check whether important work is assigned to a matching strength.
4. Define boundaries, partners, or process controls for non-fatal weaknesses.

## Requirements

### Requirement: User-scoped strengths map
Because strengths records are part of a user's judgment system, each strength SHALL belong to `current_user` while `owner` describes the person whose strength is being recorded.

Each strength SHALL include:
- `owner`;
- `name`;
- `description`;
- `evidence`;
- `created_at`.

### Requirement: Evidence-backed strengths
Because strengths must be performance facts rather than compliments, the service SHOULD mark a strength incomplete when it has no evidence.

#### Scenario: Unsupported strength
- **WHEN** a strength has no `evidence`
- **THEN** the UI SHOULD ask for a concrete example of unusually effective performance.

### Requirement: Work-fit guidance
Because the purpose of a strength is contribution, the product SHOULD help connect strengths to active contributions, priorities, and decision actions.

#### Scenario: Important work without strength fit
- **WHEN** a high-priority item has no clear owner strength
- **THEN** the review flow SHOULD ask whether the work is assigned to the right person or needs a different design.

### Requirement: Self-management facts
Because the user is also a resource to be placed well, the product SHOULD capture facts about the user's effective work mode:

- thinking through writing or conversation;
- exploration versus closure;
- architecture, execution, operations, analysis, or communication strength;
- decision speed and analysis needs;
- conditions that reliably produce high-quality work.

### Requirement: Weakness boundary
Because ordinary weakness and trust failure require different responses, the product SHALL distinguish:

- ordinary weakness: managed through role design, pairing, checklist, process, or reduced exposure;
- trust/integrity/responsibility failure: not treated as configurable.

## Artifacts

- strengths map;
- evidence list;
- work-fit review;
- weakness boundary notes;
- self-management profile.

## Non-Goals

- personality testing as an end in itself;
- forcing everyone to become well rounded;
- excusing trust or integrity failures as style differences;
- ranking people by generic competency scores.
