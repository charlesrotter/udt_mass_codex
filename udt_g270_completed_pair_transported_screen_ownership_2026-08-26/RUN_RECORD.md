# G270 run record

Date: 2026-08-26
Branch: `grok`
Preregistration commit: `a75d71bf`

## Production

```bash
python3 udt_g270_completed_pair_transported_screen_ownership_2026-08-26/derive_screen_ownership.py
```

Result: `PASS`, 36 exact symbolic checks.

## Independent replay

```bash
python3 udt_g270_completed_pair_transported_screen_ownership_2026-08-26/verify_screen_ownership_independent.py
```

Result: `PASS`, 208,005 exact-rational assertions over 12,000 frames and 1,001 smooth-ribbon axis
cases. The implementation imports no production function and reads no production result.

## Mutation replay

```bash
python3 udt_g270_completed_pair_transported_screen_ownership_2026-08-26/run_catch_proofs.py
```

Result: `PASS`, baseline clean and 11/11 targeted mutations caught.

## Premise gate

```bash
python3 verify_current_scientific_premises.py
```

Result: `PASS`, 250-row current registry and startup guards.

## Repository regression gate

```bash
pytest -q
```

Result: `172 passed, 1 xfailed`; the expected failure is unchanged and unrelated to G270.

No GPU, observational outcome, fit, distance attachment, field equation, source, matter model,
`X_max`, or protected package was used.
