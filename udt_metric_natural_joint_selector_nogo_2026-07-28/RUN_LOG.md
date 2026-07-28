# Run log

All work was CPU-only from repository root.

```text
python3 udt_metric_natural_joint_selector_nogo_2026-07-28/freeze_sources.py
python3 -m py_compile udt_metric_natural_joint_selector_nogo_2026-07-28/derive_nogo.py
python3 udt_metric_natural_joint_selector_nogo_2026-07-28/derive_nogo.py
python3 -m py_compile udt_metric_natural_joint_selector_nogo_2026-07-28/verify_nogo.py
python3 udt_metric_natural_joint_selector_nogo_2026-07-28/verify_nogo.py
```

Two implementation errors were caught before any result was banked:

1. the production reduction-rank helper attempted to extend a list with scalar SymPy expressions;
   it was corrected to append the already flattened constraint list;
2. the explicit reduced-family validation referred to the loop variable before assignment; it was
   corrected to use each named family.

Neither correction changed an equation, premise, candidate, or conclusion. The successful
production run and independent rational implementation agree on all ranks and strata.

Final production algebra:

- Lorentz bracket span rank: 6;
- real-character dimension: 0;
- fixed vector/covector dimensions: 0/0;
- full endomorphism commutant dimension: 1;
- observer/pair/ruler reduced-family dimensions: 1/1/1;
- holonomy centralizer dimensions: 1/3/3/1;
- non-collinear angular commutator: nonzero.

Independent verification: 13/13 source blobs, all ranks, all category and escape-route guards, and
32/32 catch-proofs pass.

GPU, ODE/PDE, time-live, action, source, carrier, density, boundary, matter, `Xmax`, prediction,
canonization, and repository-reorganization work launched: zero.
