# G276 run record

Date: 2026-08-26

## Production

```text
python3 derive_proper_clock_scale.py
status: PASS
exact checks: 22
```

## Independent verification

```text
python3 verify_proper_clock_scale_independent.py
status: PASS
cases: 20,000
exact assertions: 320,003
production imported: false
production output read: false
```

The repaired unit-relabelling control holds dimensionless `C_bar` fixed, transforms `tau_star` and
`c_E` with independent positive rational time/length unit factors, and recovers the corresponding
length-unit transformation of `ell` in every case.

## Hostile controls

```text
python3 run_catch_proofs.py
status: PASS
implementation mutations caught: 6
typed-scope catches passed: 2
```

No GPU, observation, fit, ODE/PDE, history solve, or protected package was used.
