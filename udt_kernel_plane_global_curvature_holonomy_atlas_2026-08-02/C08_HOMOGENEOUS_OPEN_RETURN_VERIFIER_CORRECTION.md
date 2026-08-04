# C08 homogeneous OPEN-return verifier correction

Date: 2026-08-04
Branch: `grok`
Base before this correction: `d543d58e`

## Trigger

The frozen production return has already reported `dim=1`, `mult=640`, and 505 basis elements, so
the preregistered 124-multiplicity production gate correctly returned
`OPEN_PROCESS_OR_HOMOGENEOUS_CERTIFICATE_FAILURE`. No independent verifier has yet been run.

The prewritten independent verifier contains a control-flow defect: it asserts that the production
status is the successful 124 case before parsing the evidence. It would therefore abort instead of
independently characterizing a valid OPEN return.

## Fixed correction before verifier execution

Change only the status-handling control flow:

1. accept either the successful pending-review status or the frozen non-resource OPEN status as a
   parseable return;
2. record the exact production status and an explicit successful-production gate;
3. retain the original success criteria unchanged, including exact eventual Hilbert constant 124;
4. return `OPEN_HOMOGENEOUS_OBSTRUCTION_INDEPENDENTLY_CONFIRMED` when the certificate is internally
   sound but its exact eventual constant is not 124;
5. retain `REFUTED_OR_VERIFIER_ERROR` for broken algebra, hashes, transformations, Gröbner replay,
   homogeneity, rational lower-bound replay, or catch-proofs.

No coefficient, source, homogenization, leading monomial, Hilbert rule, stabilization threshold,
target value, physical premise, or scientific conclusion may change. The frozen machine return is
immutable. Saturation, removal of infinity components, a different prime/order, and retries remain
forbidden.

## Maximum conclusion

An independently sound 640 result confirms only that the unsaturated generated homogeneous closure
does not supply the registered 124 upper bound. Rational reverse containment and C08 all-zero ideal
equality remain OPEN. It does not show that the extra homogeneous degree is a physical branch or a
real affine solution.
