# Numerical-method scope correction — directed vector intervals

Date: 2026-07-22

Status: `PREREGISTERED_BEFORE_FULL_ATLAS_OUTCOME`

The initial high-precision interval prototype is mathematically sound but computationally
dependency-heavy: a single broad two-dimensional box requires excessive scalar subdivisions. The
first representative attempt was stopped before producing an atlas result.

The complete candidate universe, two interpolation charts, sheet classifications, expected counts,
and maximum conclusion remain unchanged. The certification implementation is corrected as follows:

1. The full 4,608-sheet census will use vectorized IEEE-754 binary64 intervals with explicit outward
   rounding by `nextafter` after every elementary operation.
2. Every exact rational input is converted to a containing binary64 interval, never to an
   unqualified point float.
3. Fixed dyadic `(u,lambda)` partitions cover complete sheets. Endpoint samples never substitute for
   box coverage.
4. Any cell whose sign or derivative cannot be certified is refined on a preregistered ladder:
   `16x64`, `32x128`, then `64x256`. Remaining cells are retained as unresolved; they may not be
   dropped or graded by point sampling.
5. The most adverse certified cells for every chart/bank-pair class are replayed with the original
   80-decimal `mpmath.iv` implementation. Disagreement fails the audit.
6. A separate full-matrix verifier and direct frozen-generator probes remain required.

This correction changes computational representation, not physics, candidates, tolerances, or
outcome wording. It is not permission to accept a sampled root, weaken outward bounds, retune after
inspection, or exclude difficult sheets.
