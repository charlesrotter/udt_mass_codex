# G318 run record

Date: 2026-09-01
Device: CPU
Arithmetic: exact Python `Fraction` for load-bearing identities
Long solve: none
GPU: unused

## Commands

```text
python3 derive_nonconstant_psi_family.py
python3 verify_independent.py
python3 run_catch_proofs.py
```

## Results

- production: 14,043 exact assertions;
- implementation-distinct tensor replay: 4,440 exact assertions;
- independent Weyl instances: 27;
- hostile mutations: 48 of 48 caught after repairing two vacuous hostile-test expressions;
- branch atlas: 16 rows;
- strict-center witnesses: 4.
- current premise/startup verifier: PASS, 301-row registry;
- repository regression: 214 passed and one known xfail;
- all G318 Python sources compile.

The hostile-test repairs changed no scientific formula or landing. The fresh external reviewer
authenticated all 33 payloads, reproduced all five generated artifacts byte-for-byte, independently
rederived the load-bearing result, and returned the accepted G318 verdict without repair.
