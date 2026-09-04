# G339 run record

Date: 2026-09-03
Preregistration commit: `f6394739`
Device: CPU
Arithmetic: exact rational production algebra plus independent IEEE-754 direct-metric reconstruction
GPU: available but not used; no grid or PDE solve is needed

Commands:

```bash
python3 -B -S derive_carry_type_classification.py
python3 -B -S verify_carry_type_independent.py
python3 -B -S run_catch_proofs.py
python3 -B -S verify_package.py
```

Results:

- production: `2182/2182`;
- independent: `16155/16155` over 1,200 cases;
- hostile catches: `12/12`.
- pre-review aggregate: `15/15`;
- external review: `ACCEPT_G339_BOUNDED_CARRY_TYPE_CLASSIFICATION` with no required repair;
- post-review aggregate including return authentication: `17/17`.
