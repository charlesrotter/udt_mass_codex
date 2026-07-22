# Independent verification preregistration

Date: 2026-07-22

This verification selection is frozen after the production return but before any selected saved row
is read by the independent implementation.

## Outcome-blind anchors

For every one of the 3,072 identities compute

```text
SHA256("MOTIF_HOPF_INDEPENDENT_V1|" + identity_id)
```

Sort by the full hexadecimal digest and select the first 64 identities. Independently reconstruct
their analytic metric/phi fields without importing the production correspondence builder, canonical
geometry evaluator, motif core, or invariant-subspace core. Recompute all 17 path nodes and all 31
instrument families: 33,728 comparisons. Recompute both complete four-direction stencils for all 31
families at the 64 midpoints and independently check the saved distribution classifications.

## Complete adverse-margin escalation

Separately select every saved identity/family path that contains a motif transition or numerical
uncertainty and independently replay all 17 nodes for that family. Select every saved unstable
stencil identity/family and replay its complete two-step stencil. These selections are exhaustive
over the adverse categories and may not be sampled down after inspection.

## Exact control

Recompute the reciprocal-toric Hessian/dyad eigentuples, reflection, round cap limits, finite-endpoint
Chern-Simons formula, conditional unit limit, quotient norm, and Hopf-seed equality by a separate
symbolic route. The verifier may not import `derive_toric_control.py`.

## Catches

Exercise failures for a missing blind anchor, missing path node, missing family, mutated analytic
coefficient, omitted Christoffel term in the Hessian, projector permutation mismatch, manufactured
global eligibility, forced unit charge at finite endpoints, omitted circle-action premise, false
seed-to-relaxed-field promotion, and an imported carrier/action construction.

The maximum independent verdict is `VERIFIED-WITH-CAVEATS`; the local analytic families remain
configuration paths, and the unit Hopf result remains conditional on the explicit global toric/cap
premises.
