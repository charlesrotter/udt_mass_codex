# External adjudication — G82 fixed-C1 Radau replay

## Landing

`VERIFIED_WITH_CAVEATS`.

The fresh sealed `gpt-5.4` review found no scientific or numerical correction. It verified all
`26/26` payload hashes, exact identity of the frozen G81/G82 `C1_FULL_ANGULAR` control, genuine use
of `Radau` with no hidden DOP853 fallback in the reviewed path, and the saved matrix algebra. Its
maximum supported G82 statement is exactly:

`G81_C1_SCREEN_COVARIANCE_SURVIVES_ONE_FIXED_NON_DOP853_RADAU_REPLAY`.

The scientific ceiling remains:

`DERIVED_CONDITIONAL_SCREEN_COVARIANCE_ON_TWO_FIXED_CONTROLS`.

The independently reproduced load-bearing numbers are:

```text
Radau/DOP853 maximum matrix difference  9.459627107202695e-12
Radau coarse/fine maximum               3.449865616964161e-8
unrotated reciprocity residual          1.139757402684705e-8
rotated covariance residual             1.1582146620151037e-8
area reciprocity residual               1.2229577572853145e-8
```

All remain far below the preregistered `2e-4` gate.

## Commit-language adjudication

The reviewer correctly declined to infer Git chronology from a sealed file intake. It noted that
`PREREGISTRATION.md` names `e36752ed5e01d45f46812cb154415683a353030f` as its base while the audit
report says the calculation was preregistered at `88afa190`.

The live repository resolves the wording without changing either historical file:

- `e36752ed5e01d45f46812cb154415683a353030f` is the parent/base on which the calculation was
  preregistered;
- `88afa190737df9f461e303f6dd88812a2bc8fb09` is the direct descendant commit titled
  `Preregister fixed-C1 Radau covariance replay` that first banks `PREREGISTRATION.md` and the
  frozen calculation inputs.

These statements are compatible. The sealed reviewer did not verify this repository fact; the
post-review live verifier does.

## Binding caveats

1. The fifteen hostile mutations are useful but not catch-complete. They do not individually
   mutate every partial-reversal, omitted-transform, or changed-control possibility. Exact sealed
   hashes, the six-row source boundary, and direct reviewer inspection constrain those routes, but
   the original catch harness alone must not be described as exhaustive.
2. The sealed review did not credit repository-wide claims in `REPOSITORY_GATES.json`, because its
   executable depends on files outside the intake. Those gates are replayed separately in the live
   repository and remain repository evidence rather than sealed scientific evidence.
3. The exact packaged CLI attempted to write its result and therefore could not finish on the
   read-only intake. The reviewer instead suppressed writes in-process; the same numerical path
   produced JSON byte-identical to the sealed `DERIVATION_RESULT.json` (`2972` bytes). This is
   strong supportive reproducibility, not a literal packaged CLI rerun.
4. G82 changes only the integrator family on one already-frozen control. It is not an independent
   geometry implementation and does not establish absolute method independence or an all-direction
   theorem.

## Authority boundary and next gate

No physical profile, endpoint, scale, `X_max`, SNe/CMB observable, `cmb_temp`, source, action,
matter, bootstrap closure, signalling law, or future signal is selected. G82 closes the specific
registered fixed-C1 non-DOP853 method check. It does not justify adding more directions or solvers
merely to collect confirmations.

The next scientific decision returns to the already-deferred physical endpoint/`X_max` curve or
thermal-map question. That work requires a new bounded preregistration; it is not launched here.
