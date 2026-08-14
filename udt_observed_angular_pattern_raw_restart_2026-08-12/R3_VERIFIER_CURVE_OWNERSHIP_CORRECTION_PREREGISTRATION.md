# R3 verifier central-curve ownership correction preregistration

Date: 2026-08-14
Status: `PREREGISTERED_AFTER_GATE_FAILURE__IMPLEMENTATION_REPAIR_ONLY`

## Observed failure

The assembled 194-cell R3 atlas passed production assembly, but the independent verifier stopped
before reading any covariance conclusion.  No `R3_VERIFICATION_RESULT.json` was written.

The failing assertion compared a central curve built from the saved TreeCorr weighted components
against the corresponding curve built from the banked R2 Corrfunc weighted components with
`rtol=5e-9, atol=2e-10`.

A bounded read-only diagnosis established:

- all 776 saved central curves are bit-for-bit equal to an independent reconstruction from their
  saved TreeCorr DD, DR, and RR components and the frozen R2 normalizations;
- all 1,746 component families already passed the preregistered R3 gates: integer counts exact and
  weighted sums within relative `5e-9` or absolute `1e-7` of R2;
- the extra derived-curve check rejects 146 bins in 14 of 776 cell/lane records, all in the official
  weighted lane;
- its largest tolerance ratio is about 3.17, despite every input component satisfying the frozen
  component contract.

No covariance entry, eigenvalue, rank, feature, angular location, significance, or physical result
was inspected in making this diagnosis.

## Type error

`R3_PREREGISTRATION.md` freezes a cross-engine tolerance for each weighted pair component.  It does
not freeze a second, tighter tolerance on the nonlinear quotient formed from those already accepted
components.  The verifier silently added that extra gate.

The same inspection found that the verifier expressed the component alternative as NumPy
`allclose`, whose elementwise `atol + rtol*abs(expected)` rule is not identical to the frozen
whole-component rule `max_relative <= 5e-9 OR max_absolute <= 1e-7`.  The corrected helper must use
the latter expression exactly.  This hardens rather than relaxes the registered component gate.

This is internally inconsistent.  For normalized components `d`, `r`, and `q`, the curve is

```text
w = (d - 2r + q)/q.
```

An accepted accumulator difference in `d` or `r` can exceed a fixed absolute curve tolerance when
the expected curve is near zero.  That does not contradict the preregistered component gate.  A
synthetic catch proof must demonstrate this case without using an R3 outcome.

## Frozen repair

Before rerunning the verifier:

1. retain exact equality of every central DD, DR, and RR integer count against R2;
2. implement the preregistered whole-component weighted gate exactly: maximum relative difference
   `<=5e-9` or maximum absolute difference `<=1e-7`;
3. require every saved central curve to equal, bit for bit, an independent reconstruction from its
   own saved TreeCorr DD, DR, and RR weights and the frozen normalizations;
4. report the maximum R3-versus-R2 derived-curve residual and the number of records/bins that would
   have exceeded the removed unpreregistered gate, but do not use that redundant residual as a new
   pass/fail threshold;
5. leave the eight independently rerun leave-one Corrfunc anchor comparisons unchanged;
6. leave every covariance, support, PSD, rank, manifest, and repository test gate unchanged;
7. add a synthetic catch proof showing that (a) accepted component differences can violate the
   removed curve tolerance, (b) a corrupted saved curve is rejected, (c) an out-of-tolerance
   component is rejected, and (d) an integer-count mismatch is rejected.
   The proof must also catch a mixed-vector case that elementwise `allclose` would incorrectly pass.

This repair changes no catalog selection, component, central curve, leave-one curve, covariance,
rank, tolerance declared by the R3 preregistration, or scientific conclusion.  It cannot promote R3
beyond `VERIFIED-WITH-CAVEATS`, and the post-failure repair must remain explicit in the final grade.
