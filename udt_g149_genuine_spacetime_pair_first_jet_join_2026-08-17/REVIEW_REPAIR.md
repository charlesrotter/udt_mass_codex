# G149 adversarial repair record

Date: 2026-08-17

## Repair 1 — faithful G148 fixture

Production now reconstructs the exact registered G148 `B,Q,S,Y,Z` algebraic `lambda` jets,
constructs their combined `h_dot`, and obtains the same

```text
phi_dot_lambda = -0.009899893008986142
```

reported by G148. It is compared with G149's actual normalized pair-clock derivative only as a
specific invalid-substitution catch. The documentation explicitly says the two derivatives have
different types and that the mismatch is not a general invariant theorem.

## Repair 2 — independent liveness

The independent implementation now replays all five removal controls without importing production
code. Every family changes at least one output, and the largest disagreement with production among
all removal deltas is `9.10e-18`.

## Repair 3 — `Y,Z` scope

Every claim now says pair-clock-direction `Y,Z` first jet. The controls zero the base or screen row
blocks of `F_tau_tau,F_tau_sigma`, which are exactly `partial_tau Y,partial_tau Z`. No
`sigma`-direction liveness is claimed; `F_sigma_sigma` remains registered only as part of the smooth
quadratic immersion.

## Repair 4 — smooth versus affine

The preregistration now states that `B,Q,S` are coordinate-affine and that `E` is smooth. It no
longer calls assembled `E` affine because `Q(x)S(x)` is generally quadratic.

## Repair 5 — derivative ownership

The maximum conclusion now separates `PAIR_CLOCK_DERIVED_DOTPHI` from
`LEVI_CIVITA_DERIVED_AN_OMEGA`.

## Reverified gates

```text
production exact gates: PASS
independent identity and five-control replay: PASS
package verifier: 45/45 PASS before review-document inclusion
```
