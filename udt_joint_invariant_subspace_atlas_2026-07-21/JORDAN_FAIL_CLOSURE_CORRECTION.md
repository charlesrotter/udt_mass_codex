# Preregistered Jordan Fail-Closure and Certification Correction

Date: 2026-07-21

This correction is registered after, and in direct response to, the preserved failed fresh review
`FRESH_ADVERSARIAL_CORRECTION_REVIEW.md`.  It must be committed before classifier, verifier, report,
or generated-output mutation.

## Frozen defect

For the Lorentzian null-basis metric

```text
g = [[0,1,0,0],
     [1,0,0,0],
     [0,0,1,0],
     [0,0,0,1]]
```

and the `g`-self-adjoint nilpotent operator with only `J[0,1]=1`, both implementations currently
return `NUMERIC_CLASSIFIED` even though `J^2=0`, `J!=0`, and the sole eigenvalue is defective.  The
real-primary interpolation used by the atlas is valid only after semisimplicity of every primary
cluster is established.  An unresolved or defective cluster must fail closed.

## Registered corrections

1. The builder will test algebraic multiplicity against independently rank-certified geometric
   multiplicity for every complex eigenvalue cluster before constructing primary projectors.
2. The independent verifier will implement the same mathematical requirement through its own
   Vandermonde/CRT route and a separately written semisimplicity check.
3. Any defective cluster, ambiguous cluster multiplicity, or uncertain eigenspace rank will return
   `NUMERIC_UNCERTAIN_CENTRAL_BLOCKS` and propagate to `NUMERIC_UNCERTAIN`.
4. The exact Lorentzian nilpotent example above becomes a tenth exercised catch and must be rejected
   as a classified result by the same classifier paths used for saved atlas rows.
5. All projector acceptance gates will use the controlling preregistered tolerance `1e-9`, not
   `1e-7`.  Existing classifications are not presumed to survive this tightening.
6. Saved operator-family registry, saved bivector census, saved coverage, saved uncertainty ledger,
   saved result contract, and saved family-row coverage will each be checked through reusable
   validators.  Their registered mutations will pass through those same validators; catch-only
   predicates do not satisfy this contract.
7. The lay report will say "nine named pointwise families" wherever it currently says or implies
   "complete local geometry" without that scope.

## Outcome discipline

The prior `11,983` unique and `2,225` multiple row counts are observations to be retested, not
targets.  If the corrected fail-closed classifier changes any row, the new census controls and the
change must be reported.  No row may be silently discarded.  Uncertain rows remain in the atlas.

Before any new output is generated, compact pre-correction results, transcripts, catches, manifest,
and repository-gate record will be preserved under `PRE_JORDAN_FAIL_CLOSURE_*` names.  The full
builder, independent verifier, manifest, and repository gates will then run in that order.  A new
fresh read-only adversarial review is required before final banking.

Maximum conclusion before those steps pass:

`BOUNDED_FULL_JOINT_FAMILY_IRREDUCIBILITY_OBSERVED; ATLAS_CERTIFICATION_OPEN`.
