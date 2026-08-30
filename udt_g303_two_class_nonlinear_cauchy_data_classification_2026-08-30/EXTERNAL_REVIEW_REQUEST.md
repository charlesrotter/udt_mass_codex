# G303 fresh adversarial review request

## Role and scope

Act as a fresh skeptical mathematical-relativity and hyperbolic-PDE reviewer. Inspect only the
sealed intake. Do not edit evidence files, continue the research, use observations, or propose a
preferred UDT law. Writable ephemeral copies may be used only for bounded replay checks.

## Claimed bounded landing

```text
BOTH_G301_CLASSES_HAVE_THE_SAME_LOCAL_CAUSAL_PRINCIPAL_SYSTEM
__TRACEFREE_DATA_ARE_THE_UNION_OVER_ONE_CONSTANT_SCALAR_DATUM
__WELLPOSEDNESS_DOES_NOT_SELECT
```

This is conditional on the frozen G301 local metric-only residual lane and one connected local
boundary-free Cauchy slab. It does not select a UDT equation or history.

## Required adversarial questions

1. Rederive independently whether `S_ab=0` plus contracted Bianchi is exactly
   `Ric_ab=Lambda g_ab`, `dLambda=0` on connected regions.
2. Rederive all normal projections and verify the signs/factors in
   `H=2Lambda`, `M_i=0` for signature `(-,+,+,+)` and the stated `K` convention.
3. Decide whether trace-free initial data really form a union over one constant datum, or whether
   an additional scalar function, normal derivative, constraint, or compatibility condition was
   hidden or discarded.
4. Distinguish the raw rank-nine trace-free principal symbol from the Bianchi-completed fixed-sector
   rank-ten harmonic metric system. Determine whether this completion is mathematically legitimate
   or circular.
5. Check whether both systems actually meet the same local quasilinear-wave and gauge-constraint
   propagation hypotheses. Flag any overstatement of well-posedness.
6. Determine whether harmonic gauge, Gauss--Codazzi, or the standard local wave theorem imports a
   gravitational field equation rather than serving only as mathematics applied to the frozen
   residuals.
7. Verify that the reciprocal kernel contributes no additional evolution residual.
8. Inspect production, independent replay, hostile catches, source hashes, preregistration ancestry,
   and package verifier for shared-code false independence, vacuous assertions, missed mutations,
   or outcome-driven repair.
9. Preserve the exact ceiling: no boundary/global theorem, field-equation selection, source, mass,
   observation, physical query population, realized history, scale, or `X_max`.

## Required replays

The intake contains `review_runtime/python_deps.tar.gz`, a sealed review-only archive of the exact
SymPy and mpmath versions used by the registered scripts. Extract it into `/work/python_deps`; the
launcher points `PYTHONPATH` there. Do not download or install anything. Then run in a writable
ephemeral copy:

```bash
mkdir -p /work/python_deps
tar -xzf /intake/review_runtime/python_deps.tar.gz -C /work/python_deps
python3 derive_cauchy_classes.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

## Return format

Lead with exactly one verdict token:

- `VERIFIED_BOUNDED_CLASSIFICATION`
- `VERIFIED_WITH_CAVEATS`
- `REFUTED`
- `INTERNAL_CERTIFICATION_FAILURE`

Then state:

- the strongest retained or corrected landing;
- every exact mathematical defect or caveat;
- whether the one-constant data census is valid;
- whether local well-posedness genuinely fails to discriminate;
- any required repair, separated into scientific versus packaging/certification changes.
