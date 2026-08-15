# Evidence gates

## Gate 1 — preregistered

**PASS.** The question, complete degree-of-freedom census, falsifiers, `mu` type split, allowed
landings, and maximum conclusion were committed and pushed at `ad9a8090` before the production
derivation was run.

## Gate 2 — full space or bounded scope justified

**PASS WITH EXPLICIT BOUND.** The primary identities cover arbitrary symbolic `2x2` matrices
`B,Q,S,Y,Z` with regularity imposed only where their types require it. No invertibility of `Y` is
used in the primary pullback. The Gram quotient is separately bounded to `det(Y)!=0`. Terminal
claims are bounded to `h00<0, det(h)<0`.

Not covered: global topology, chart transitions, physical histories, physical pair selection,
actions, sources, matter, bootstrap, `X_max`, or observational models.

## Gate 3 — independently verified on the load-bearing premise

**PASS, including a fresh sealed external semantic adversary.**

- production: exact SymPy matrix identities;
- independent: standalone stdlib `Fraction` matrix implementation, importing neither SymPy nor the
  production code;
- terminal live derivative: shrinking-step black-box convergence through `1/10, 1/100, 1/1000,
  1/10000`;
- sensitivities: independent one-channel black-box differences;
- catch proofs: exact Fraction mutations omitting `dQ,dS,dY,dZ` and flipping the `dB` response;
- all registered checks passed.
- repository regression suite: `90 passed, 1 xfailed` (`test_no_habit_pins`, known matter-lane
  solution-space gate) in 1.41 seconds.
- external: a fresh `gpt-5.4` read-only review verified the scope digest and all 28 payloads, then
  independently reproduced the pullback, singular-`Y` witness, five-channel variation census,
  terminal ratio, compression fibers, and `mu` type result. It returned
  `VERIFIED_WITH_CAVEATS` with no blocking defect.

## Gate 4 — every premise audited

**PASS within scope.** `PREMISE_LEDGER.tsv` separates observed calibration, founding posits,
conditional coframe/query data, derived evaluation identities, and open physics. `MU_TYPE_LEDGER.tsv`
separates four-component modern mixing from the older conditional scalar.

## Current banking grade

`VERIFIED-WITH-CAVEATS__FRESH_EXTERNAL_SEMANTIC_REVIEW_PASSED`, not canon. The remaining caveats are
the explicit conditional scope: supplied metric and pair realization, kinematic rather than
dynamical live formulas, no physical history, and no uniquely selected scalar `mu`.
