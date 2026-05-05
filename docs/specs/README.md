# Specs

This directory is the source of truth for shipped product behavior. A spec is not a field list or endpoint inventory first. It is a causal argument for why a behavior must exist if the product is to help a knowledge worker become an effective executive.

## First-Principles Doctrine

Drucker's core claim is that effectiveness is a trained practice, not a personal trait. The product exists to turn that practice into repeated, observable actions for any user whose judgment affects organizational results.

Every capability SHALL be justified from these first principles:

1. Time is the limiting resource. It cannot be stored, replaced, or recovered.
2. Knowledge work is valuable only through outward contribution, not effort or activity.
3. People produce results through strengths. Weaknesses are managed by design, not by pretending everyone can be well rounded.
4. Significant results require concentration. Priority without posteriority is only a wish list.
5. A decision is not effective until it has action, responsibility, and feedback from reality.

Specs and changes SHALL explain necessity before implementation. The reader should be able to see:

- which Drucker habit is being served;
- what user behavior must change;
- what failure mode appears without the feature;
- what artifact proves the behavior happened;
- what is intentionally out of scope.

Requirements SHOULD be written as causal contracts:

`Because <constraint/failure mode>, the system SHALL <behavior> so that <observable outcome>.`

## System Loop

The five habits operate as one loop:

1. **Time** creates factual evidence.
2. **Contributions** turns evidence into an outward result commitment.
3. **Strengths** determines which person or work mode can produce that result.
4. **Priorities** concentrates scarce time and attention on a few choices.
5. **Decisions** turns judgment into assigned action and checked reality.
6. **Dashboard** exposes breaks in the loop and guides the weekly review.

No capability should optimize for generic productivity, task tracking, or collaboration unless it directly strengthens this loop.

## Spec Writing Standard

Each capability spec SHOULD include:

- **Purpose:** the Drucker habit and organizational result served.
- **First principles:** the non-negotiable constraints behind the feature.
- **Core user actions:** the repeated actions the product must make easy.
- **Requirements:** product contracts and scenarios.
- **Artifacts:** records, lists, reviews, or dashboard signals proving practice.
- **Non-goals:** tempting features that would dilute the habit system.

## Layout

```
docs/
  specs/
    <capability>/
      spec.md          # current behavior, requirements, API
  changes/
    <change-id>/
      proposal.md      # first-principles why + what
      tasks.md         # ordered implementation checklist
      design.md        # implementation design after necessity is clear
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

## Weekly Operating Rhythm

The product SHOULD support a weekly review that can be completed in 15-30 minutes:

1. review actual time and diagnose waste;
2. delete, delegate, or stop other-wasting work;
3. confirm the current contribution commitment;
4. check whether strengths are matched to important work;
5. reduce priorities to one to three active matters and name posteriorities;
6. complete decisions with owner, action, and feedback.

If a user cannot answer these questions from the system, the specs are incomplete:

- Where did my time actually go?
- What contribution am I responsible for now?
- Whose strengths are being used or wasted?
- What am I explicitly not doing?
- Which decisions still lack action or feedback?
