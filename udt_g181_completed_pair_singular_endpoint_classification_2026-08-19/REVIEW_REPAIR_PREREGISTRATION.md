# G181 external-review repair preregistration

Date: 2026-08-19

The fresh external review returned `G181_REQUIRES_REPAIR`. It found no scientific counterexample
but rejected two certification claims. Before implementing any repair, the repair scope is frozen
as follows.

## Registered repairs

1. Remove the third-party SymPy dependency from the production replay. Replace it with a
   dependency-free exact implementation that regenerates the same `DERIVATION_RESULT.json` and
   `WITNESS_ATLAS.tsv` and runs under `python3 -I -S` with `UDT_READ_ONLY_REPLAY=1`.
2. Replace the catch suite. Count only executable mutants whose altered calculation is rejected by
   an invariant oracle. Metadata/open-scope checks must be reported separately as semantic guards
   and must not contribute to `catch_count`.
3. Preregister exactly 28 executable mutation families spanning determinant/density algebra,
   completed-coordinate and shift transforms, tape thresholds, depth signs, tape/depth
   independence, endpoint regularity, density-limit nonclassification, primary turns/center/zero
   tangent, removable stalls, cusp differentiability, and oscillatory nonconvergence.
4. Report exactly six semantic scope guards separately: supplied-family ownership, two-sided
   branch carry, null/cut/focal/topology/global exclusion, non-scalar transport exclusion,
   `X_max`/metric-distance exclusion, and dynamics/observation exclusion.
5. Make the independent exponent census genuinely rational, including noninteger rational
   exponents and exact populations on both sides of and at `a+b=-1`. Preserve 20,000 trials and all
   nine cross-classes; do not preserve the old assertion total merely for continuity.
6. Require `verify_package.py` to execute all three replays in isolated read-only subprocesses, not
   merely inspect their banked JSON.

## No scientific changes permitted

The formulas, 19-witness atlas, seven-source set, landing, premise grade, and maximum conclusion
may not change on this repair path. A mathematical change requires a new preregistration.

The follow-up may return `G181_REPAIR_ACCEPTED` only if the corrected sealed intake reproduces all
artifacts without repository access, third-party dependencies, or writes and the original bounded
geometry remains intact.
