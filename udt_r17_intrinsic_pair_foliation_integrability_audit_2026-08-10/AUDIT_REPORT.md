# R17 intrinsic pair foliation audit

Date: 2026-08-10

Grade: **VERIFIED-WITH-CAVEATS; EXTERNAL ADVERSARIAL REVIEW ACCEPTED**

## Outcome

The R17 complete metric does contain a stronger structure than the previous pointwise projector
and vertical-factor results showed. On all six supplied regular C01--C06 configurations:

- the intrinsic clock/ruler plane integrates globally into a family of `R x S1` Hopf cylinders;
- those cylinders foliate `R x S3` and are parametrized by `S2`;
- the angular plane is instead a nonintegrable rank-two normal bundle in 4D and the contact plane
  on each spatial `S3` slice;
- the full induced clock/ruler metric keeps the twist and has determinant exactly `-1`;
- the terminal reciprocal evaluator returns `phi`, so relative endpoint depth is `delta_K`; and
- the complete angular carry, path/winding, and endpoint reset remain open.

The accepted local landing is

```text
GLOBAL_PAIR_FOLIATION_AND_SCALAR_DEPTH_DERIVED__FULL_NORMAL_BUNDLE_ARROW_OPEN.
```

This is a genuine narrowing: the previously open R17 pair-surface integrability gate closes
positively and without a new postulate. It is not complete observer-arrow closure.

## Candidate census

All five preregistered candidates remain in `SURFACE_CLASSIFICATION.tsv`. The metric-owned
reciprocal leaves survive; the screen survives as a normal bundle rather than as integral
surfaces; arbitrary Killing tubes remain query-dependent; and cross-leaf/winding comparisons
remain path-labelled.

## Evidence gates

1. **Preregistered:** yes, commit `c79881d2` predates the algebra.
2. **Full space or bounded scope:** full analytic classification of the named smooth regular
   stationary C01--C06 family; other branches and degenerate/time-live strata excluded explicitly.
3. **Independent verification:** yes, after replacing the externally identified hard-coded local
   reconstruction with a constructive no-SymPy derivation; the fresh external reviewer independently
   rederived the load-bearing algebra and accepted the bounded landing.
4. **Premise audit:** yes; every selection and promotion guard remains false.

The package is banked **VERIFIED-WITH-CAVEATS** only in the named conditional R17 scope.

## Exact counts

```text
frozen sources                 15/15
production exact checks        10/10
constructive independent checks 72/72
exercised catch proofs          14/14
supplied lambda strata          6/6
selected leaves                 0
selected windings               0
selected lambda values          0
complete physical arrows        0
```

See `EXACT_DERIVATION.md`, `DERIVATION_RESULT.json`,
`INDEPENDENT_VERIFICATION_RESULT.json`, and `CATCH_PROOFS.tsv`.
