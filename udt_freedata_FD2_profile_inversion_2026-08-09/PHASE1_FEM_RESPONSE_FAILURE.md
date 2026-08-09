# FD2 Phase-I finite-element response failure — preserved

Date: 2026-08-09  
Status: preregistered blind response run completed; response-convergence gate failed

The registered 320-row profile-response census was run at both finite-element grids before any
Planck or SNe value entered FD2. Both atlases are complete and reproduce the frozen FD1 baseline
frequencies extremely well:

- grid 180: 320/320 rows; maximum FD1 frequency drift `3.2922e-12`; maximum raw backward residual
  `2.9614e-11`;
- grid 240: 320/320 rows; maximum FD1 frequency drift `1.1973e-11`; maximum raw backward residual
  `5.3323e-11`;
- maximum grid-180/grid-240 unperturbed-frequency drift: `0.00337201`.

The derivative surface did **not** pass its frozen convergence rule. Under the preregistered
relative response-norm comparison, only 25/320 rows satisfy both the 2% half-step and 5% inter-grid
criteria; 295 are unresolved. The maximum relative response drift is `566.7597`. Four rows also
exceed the 2% half-step gate.

Diagnosis made before observational inversion: low-order uniform-Liouville FEM frequencies are
stable, but differentiating their small discretization error with respect to a localized profile
motif produces a grid-phase artifact. A diagnostic grid sequence for one unresolved row oscillates
with a decaying envelope rather than approaching a stable derivative monotonically. Increasing the
finite-difference amplitude from `1e-4` through `0.05` does not remove it, so it is not subtraction
roundoff or a too-small step.

This failure is not erased and the 5% criterion is not relaxed. Neither atlas can select or reject
a TT-responsive profile. Phase II remains unopened.

Frozen evidence hashes:

```text
94fff3ad18fd33dec35708f7cf08a62b1b4d5565ad557d10bae041ecaf71578c  phase1_response_g180.json
a30bdc090d4cb51d098e272f55548df22d28e42ff08d092d0c6d8e1a9aae070d  phase1_response_g240.json
ef27187a1760ba30997d9dd36363c9cb83499f491b1d61327a3fa80acf37dc93  phase1_verification.json
```

This is a numerical response-certification failure, not a physical negative.

