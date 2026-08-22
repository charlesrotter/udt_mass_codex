# G222 repair implementation

Date: 2026-08-22

Preregistration commit: `2db0c76d`

## Implemented repairs

- **R1:** the standard-library replay is now graded as finite exact algebra cross-checking, not a
  sampling proof of the general geometry. It independently replays the explicit flat ribbon and the
  finite screen projector algebra on 12,000 rational cases.
- **R2:** the 18 field flips are now named and reported only as payload-contract mutations.
- **R3:** `verify_package.py` snapshots the complete G222 tree plus all 10 frozen sources and compares
  the entire state after replay. Synthetic additions, modifications, and deletions are rejected.
- **R4:** `EXACT_DERIVATION.md` now carries the differentiated-projector calculation and the curvature
  representative calculation. Both are mirrored by symbolic and exact-rational checks.

## Replayed gates

- production symbolic/direct derivation: 43/43 pass;
- finite algebra replay: 12,000 cases, 396,000 exact rational assertions;
- payload-contract guard: 18/18 field mutations rejected;
- complete-tree no-write replay: pass;
- optimized mode: rejected as required;
- premise registry: 205 rows pass before any G222 startup promotion;
- repository tests: 126 pass, 1 expected xfail.

## Grade

```text
ACCEPT_WITH_REPAIRS__REPAIR_REVIEW_PENDING
```

The bounded scientific landing is unchanged. No startup-surface promotion is made before a fresh
sealed repair-only follow-up review accepts the registered repairs.
