# Changes

Change proposals describe why the current system must change and what will become possible after the change is accepted.

## First-Principles Rule

Every change SHALL start from necessity, not solution preference. Before naming tables, endpoints, libraries, or UI controls, the proposal SHALL make the causal argument visible:

- Which Drucker habit or organizational result is blocked?
- What user behavior is failing, inaccurate, or too hard to repeat?
- What first-principles constraint creates the need? Examples: time is non-storable, contribution must be outward and observable, people perform through strengths, attention must be concentrated, decisions require action and feedback.
- What goes wrong if nothing changes?
- What artifact or dashboard signal will prove the change worked?
- What remains out of scope to protect the product from becoming generic task, chat, or collaboration software?

## Required Proposal Shape

1. **First-principles problem:** the constraint and failure mode.
2. **Behavior change:** what the user or manager can now do.
3. **System change:** the smallest product, data, API, or workflow change needed.
4. **Boundaries:** what the change intentionally does not solve.
5. **Acceptance:** observable scenarios proving the behavior is possible.

Design documents MAY discuss implementation only after the product necessity is clear.

Tasks SHOULD remain traceable to the first-principles problem. A task that cannot be linked to a behavior or artifact is suspect.
