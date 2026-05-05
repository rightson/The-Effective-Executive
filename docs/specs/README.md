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
| `accounts` | proposed | see `changes/multi-user-time-management` |
