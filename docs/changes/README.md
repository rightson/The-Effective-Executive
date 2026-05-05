# Changes

Change proposals describe why the current system should change and what must become true after the change is accepted.

## First-Principles Rule

Every change SHALL start from necessity, not solution preference. Before naming tables, endpoints, libraries, or UI controls, the proposal should make the causal argument visible:

- Which Drucker habit or organizational result is currently blocked?
- What user behavior is failing or too hard to repeat?
- What first-principles constraint creates the need? Examples: time is non-storable, contribution must be outward and observable, people perform through strengths, attention must be concentrated, decisions are not real until assigned and checked.
- What goes wrong if nothing changes?
- What artifact or signal will prove the change worked?
- What remains out of scope to protect the product from becoming a generic task or collaboration system?

## Proposal Shape

Good proposals use this order:

1. **Why:** the current failure mode and first-principles constraint.
2. **What changes:** the smallest product behavior and data/API changes needed to remove that failure mode.
3. **What does not change:** boundaries that preserve the Drucker habit system.
4. **Impact:** specs, migrations, API behavior, and user workflows affected.
5. **Acceptance:** observable scenarios that prove the behavior is now possible.

Design documents MAY discuss implementation, but only after the product necessity is clear.
