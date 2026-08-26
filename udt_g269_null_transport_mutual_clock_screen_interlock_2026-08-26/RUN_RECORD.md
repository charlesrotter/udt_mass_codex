# G269 run record

Date: 2026-08-26
Branch: `grok`
Preregistration commit: `c79f29e6`

## Production

```bash
python3 udt_g269_null_transport_mutual_clock_screen_interlock_2026-08-26/derive_transport_interlock.py
```

Result: `PASS`, 34 exact symbolic checks.

The first invocation stopped before writing a result on two test-expression transcription errors.
`PREREGISTRATION_EXECUTION_NOTE.md` records the bounded arithmetic/sign repairs.

## Independent replay

```bash
python3 udt_g269_null_transport_mutual_clock_screen_interlock_2026-08-26/verify_transport_independent.py
```

Result: `PASS`, 143,715 exact-rational assertions over 12,000 cases, including 11,613 transverse
cases, 387 planar cases, and 101 distinct `M_PT` values at one fixed `r`.

## Mutation replay

```bash
python3 udt_g269_null_transport_mutual_clock_screen_interlock_2026-08-26/run_catch_proofs.py
```

Result: `PASS`, baseline clean and 10/10 injected mutations caught through the shared validator.

## Repository gates

```bash
python3 verify_current_scientific_premises.py
pytest -q
```

Results: the 250-row premise registry and current startup guards pass; the full repository suite
reports `172 passed, 1 xfailed`.

No GPU, observational outcome, fit, distance attachment, field equation, source, matter model,
`X_max`, or protected package was used.
