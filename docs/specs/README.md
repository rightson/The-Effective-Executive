# Specs

This directory holds the **current** specification of the system — what is built and shipped today. It is the source of truth that change proposals (in `../changes/`) modify.

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

## Primary Workflow

The expected use pattern is weekly:

1. Capture actual time during the week in small factual entries.
2. Diagnose the captured time: eliminate, delegate, stop wasting others' time, and consolidate usable blocks.
3. Reconfirm the user's current contribution commitment.
4. Check whether the next one to three priorities still deserve concentrated resources.
5. Assign or reshape work around documented strengths.
6. Review open decisions for owner, deadline, validation, and dissent.

The product SHOULD make this review easy to complete in 15-30 minutes and SHOULD turn every incomplete Drucker habit into a visible next action.
