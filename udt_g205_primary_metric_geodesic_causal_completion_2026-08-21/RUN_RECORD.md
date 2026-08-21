# G205 run record

Date: 2026-08-21

Preregistration commit: `932155c1`

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g205_primary_metric_geodesic_causal_completion_2026-08-21/derive_geodesic_completion.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g205_primary_metric_geodesic_causal_completion_2026-08-21/verify_geodesic_completion_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g205_primary_metric_geodesic_causal_completion_2026-08-21/run_boundary_diagnostics.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  udt_g205_primary_metric_geodesic_causal_completion_2026-08-21/run_catch_proofs.py
```

Observed sequence:

1. the first symbolic run failed closed because SymPy would not infer the sign of an abstract
   positive function;
2. the check was repaired to exact factorization plus the explicit registered `f>0` premise;
3. production passed 112 assertions;
4. independent exact-rational Hamiltonian algebraic-core replay passed 10,000 distinct cases and
   150,007 assertions in the initial package, including seven source-hash assertions;
5. boundary diagnostics passed at 80 digits;
6. hostile catches passed 15/15.

No result family, parameter, or classification was changed after observing the output.

## External-review repair sequence

Fresh external review retained the scientific landing but found that the package replay read live
repository sources, the independent scope was overstated, analytic global proofs were presented as
if mechanized, and finite order checks were presented too close to the universal quantifier. The
repairs were preregistered at commit `012fa064`. Live source hashing was separated from the
self-contained package replay; the independent count therefore becomes 150,000. No mathematical
outcome or parameter family changed.

The repaired evidence contract adds two false-mechanization catches and replaces the external
source-hash catch with a bounded independence-scope catch, for 17/17 hostile catches.

The sealed package-only repair follow-up returned `REPAIRS_VERIFIED__LANDING_RETAINED`. It found no
remaining evidence overclaim and confirmed that the scientific result did not change.

Final repository closure passed the 189-row scientific-premise verifier and the full test suite:
120 passed with one known xfail.
