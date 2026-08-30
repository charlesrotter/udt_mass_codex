# G302 run record

Date: 2026-08-30

## Preserved first failures

1. `python3 -S .../derive_trace_span_and_geometry.py` failed because SymPy is unavailable with site
   loading disabled.  No scientific output was produced.
2. The first ordinary production run rejected structural equality between
   `(R0**2*r**6+72*b**2)/(6*r**6)` and `R0**2/6+12*b**2/r**6`.  Exact simplification of their
   difference returned zero.  The check was repaired to require zero difference and record the
   preregistered canonical form.
3. SymPy did not automatically simplify `tanh(-log(f)/2)`.  The identity was replayed through the
   exact exponential definition of `tanh`; no output formula changed.
4. The independent Riemann contraction encountered the same structural-expression issue and was
   repaired with an exact zero-difference assertion.
5. SymPy's interval root counter counted the algebraic `r=0` root of `r f(r)` even though the domain
   is `r>0`.  The boundary factor is now explicitly deflated before positive-root counting.
6. The repeated-root checker initially expected multiplicity from `count_roots`; the library counts
   the one distinct root.  Exact factorization and the roots dictionary now separately certify
   multiplicity two.

All repairs were representation or domain-bookkeeping repairs.  The preregistered equation,
candidate family, sign strata, expected ranks, and conclusion wording were unchanged.

## Passing production

```text
RECIPROCAL_SHAPE_SPANS_NINE_AND_COMPLETE_SCALE_RESTORES_TEN__NO_G301_CLASS_SELECTED__TRACEFREE_BRANCH_HAS_EXACT_CHANNEL_SEPARATION
shape rank 9
complete rank 10
solution -R0*r**2/12 + b/r + 1
angular 3*b/(2*r) -3*b/(2*r)
```

## Passing independent replay

```text
G302 independent verification PASS
orbit_count=133 generator_only_rank=8 shape_rank=9 complete_rank=10
solution_kretschmann=R0**2/6 + 12*b**2/r**6
```

## Passing hostile replay

```text
G302 catch proofs PASS (11/11)
```

## Repository-wide gates

```text
PASS: 285-row premise registry
197 passed, 1 xfailed in 135.79s
```

The xfail is the existing registered `test_no_habit_pins` matter-sector migration item; G302 does
not touch that sector.
