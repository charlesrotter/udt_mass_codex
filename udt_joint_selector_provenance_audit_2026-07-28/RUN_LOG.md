# Run log

All computations used CPU only from repository root.

```text
python3 udt_joint_selector_provenance_audit_2026-07-28/discover_sources.py
python3 udt_joint_selector_provenance_audit_2026-07-28/build_audit.py
python3 -m py_compile udt_joint_selector_provenance_audit_2026-07-28/run_algebra.py \
  udt_joint_selector_provenance_audit_2026-07-28/verify_audit.py
python3 udt_joint_selector_provenance_audit_2026-07-28/run_algebra.py
python3 udt_joint_selector_provenance_audit_2026-07-28/verify_audit.py
```

The first independent-verifier run stopped at catch-proof F17 because the proof predicate was
written with a reversed `any` condition. The predicate was corrected to test the preregistered J06
nonselection gate directly. No source, candidate, obligation, algebra, or outcome changed. The
second run passed all 30 catch-proofs.

Production algebra: 13/13 exact checks pass under Python 3.10.12 and SymPy 1.13.1.

Independent replay: 3,044/3,044 source blobs rehashed; 80/80 group rulings reconciled; 16/16
candidate rows checked; 30/30 catch-proofs pass.

GPU processes launched: zero.

P03-B, ODE/PDE, time-live, density, bootstrap-equation, action, source, carrier, boundary, matter,
`Xmax`, prediction, canonization, and repository-reorganization work launched: zero.
