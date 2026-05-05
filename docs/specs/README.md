# Specs

This directory holds the **current** specification of the system — what is built and shipped today. It is the source of truth that change proposals (in `../changes/`) modify.

Specs and changes SHALL be written from first principles. They must make the feature's necessity understandable before describing fields, endpoints, or UI. The reader should be able to see which Drucker habit is served, why the system must intervene, and how the result becomes observable.

Layout follows [Open Spec](https://github.com/Fission-AI/OpenSpec) conventions:

```
docs/
  specs/
    <capability>/
      spec.md          # current behaviour, requirements, API
  changes/
    <change-id>/
      proposal.md      # why + what
      tasks.md         # ordered checklist
      design.md        # optional: trade-offs
      specs/
        <capability>/
          spec.md      # delta to apply on accept
```

## Capabilities

| Capability | Status | Spec |
|---|---|---|
| `platform` | shipped | [platform/spec.md](platform/spec.md) |
| `time` | shipped | [time/spec.md](time/spec.md) |
| `contributions` | shipped | [contributions/spec.md](contributions/spec.md) |
| `strengths` | shipped | [strengths/spec.md](strengths/spec.md) |
| `priorities` | shipped | [priorities/spec.md](priorities/spec.md) |
| `decisions` | shipped | [decisions/spec.md](decisions/spec.md) |
| `dashboard` | shipped | [dashboard/spec.md](dashboard/spec.md) |
| `accounts` | shipped | [accounts/spec.md](accounts/spec.md) |

## Product Doctrine

The service is a habit-formation operating system for Drucker's effective executive, not a generic productivity tracker. It SHALL help any knowledge worker whose judgment affects organizational results practice five trainable habits:

1. know where time actually goes;
2. define contribution in outward, observable results;
3. place work on strengths instead of idealized roles;
4. concentrate resources on a few priorities and explicit posteriorities;
5. convert important judgments into effective decisions with action and feedback.

The five capabilities SHALL operate as one causal chain. Time evidence feeds contribution clarity; contribution clarity determines priorities; strengths determine who should carry the work; priorities force abandonment; decisions turn judgment into action. The dashboard SHALL surface gaps in that chain instead of merely counting records.

## First-Principles Writing Standard

Every capability spec and change proposal SHALL answer these questions before or inside its requirements:

1. What organizational result or Drucker habit does this support?
2. What user behavior must the product make easier, more accurate, or more repeatable?
3. What scarce resource or first-principles constraint is being protected? Examples: time cannot be stored, contribution must be observable, strengths are uneven, attention must be concentrated, decisions require action and feedback.
4. What failure mode occurs without this feature?
5. What artifact proves the behavior happened? Examples: time inventory, elimination list, contribution definition, strengths map, posteriority list, decision record.
6. What is out of scope because it would dilute the habit system?

Requirements SHOULD be written as causal contracts:

`Because <constraint/failure mode>, the system SHALL <behavior> so that <observable outcome>.`

Specs SHOULD avoid feature-by-analogy language such as "like a project management app" unless the analogy is explicitly rejected or narrowed. Implementation details belong after the necessity and behavioral contract are clear.

## Primary Workflow

The expected use pattern is weekly:

1. Capture actual time during the week in small factual entries.
2. Diagnose the captured time: eliminate, delegate, stop wasting others' time, and consolidate usable blocks.
3. Reconfirm the user's current contribution commitment.
4. Check whether the next one to three priorities still deserve concentrated resources.
5. Assign or reshape work around documented strengths.
6. Review open decisions for owner, deadline, validation, and dissent.

The product SHOULD make this review easy to complete in 15-30 minutes and SHOULD turn every incomplete Drucker habit into a visible next action.
