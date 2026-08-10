# Audit report — R17 magnitude-to-grading selection

Date: 2026-08-10

Status: **VERIFIED-WITH-CAVEATS; CORRECTED EXTERNAL REVIEW ACCEPTED**

## Result

Conditional on the supplied complete R17/W01 C01--C06 coframes, the founded reciprocal
normalization excludes identity as a realization of
nonzero `delta_K`. Smooth projector-preserving composition gives a one-parameter vertical action.
The founded pair fixes its clock/ruler weights; the complete R17 coframe fixes the symmetric screen
weight to the supplied configuration value `lambda`. The remaining `wJ` screen generator is exactly
`SO(2)` presentation rotation and changes neither the metric nor terminal reciprocal density.

Accepted conditional landing:

```text
COMPLETE_COFRAME_CONDITIONAL_VERTICAL_RECIPROCAL_METRIC_CLASS_MOD_SO2__
FULL_PHYSICAL_ARROW_OPEN
```

The full raw arrow remains nonunique and physically unowned. G42's demotion of
`U_gamma exp(delta_K X_p)` to a conditional assembly remains in force.

## Exact gates

- primary SymPy algebra: 16/16;
- independent standard-library `Fraction`/rank reconstruction: 12/12, with no production-result
  import;
- source manifest: 17/17 hashes replayed;
- exercised semantic mutations: 13/13 rejected;
- exact witness density arguments: `(rho_1,rho_2,Q)=(1/4,1,16)`;
- all six supplied `lambda` configurations retained without selecting one.

## Interpretation boundary

This derives one branch-local vertical metric class, not a physical cross-fibre comparison functor.
The path/query, isometric factor, endpoint reset, pair surface, on-shell branch selection, and
degenerate continuation remain open. No universal `c_eff` or downstream physics follows.

## Banking gates

1. **Preregistered:** yes, commit `053498fb` before derivation.
2. **Full or bounded:** complete for the declared projector-preserving smooth vertical class on
   R17 C01--C06; not every branch or every raw general-linear arrow.
3. **Independent:** corrected local implementation-independent exact reconstruction passes. The
   first external reviewer accepted only the complete-coframe-conditional theorem but exposed a
   real verifier-independence weakness and mistakenly reported the manifested sources absent. The
   corrected manifest-confined adversarial review independently replayed all 17 sources and both
   algebra controllers, found no surviving refutation, and returned
   `ACCEPT_ONLY_AS_COMPLETE_COFRAME_CONDITIONAL`.
4. **Premises audited:** yes for pair-only versus complete-coframe input, screen phase, lambda,
   path/isometry, reset, pair surface, and excluded downstream claims.

The maximum grade is `VERIFIED-WITH-CAVEATS` in the declared bounded conditional scope.
