# G270 run record

Date: 2026-08-26
Branch: `grok`
Preregistration commit: `a75d71bf`

## Production

```bash
python3 udt_g270_completed_pair_transported_screen_ownership_2026-08-26/derive_screen_ownership.py
```

Original result: `PASS`, 36 exact symbolic checks.

After preregistered external-review repair R2: `PASS`, 39 exact symbolic checks, including the full
off-axis determinant and an exact positivity decomposition for `lambda>=0`, all real `tau`.

## Independent replay

```bash
python3 udt_g270_completed_pair_transported_screen_ownership_2026-08-26/verify_screen_ownership_independent.py
```

Original result: `PASS`, 208,005 exact-rational assertions over 12,000 frames and 1,001
smooth-ribbon axis cases.

After preregistered external-review repair R2: `PASS`, 368,165 exact-rational assertions over
12,000 frames, 1,001 axis cases, and 40,040 nonzero-`tau` samples. The implementation imports no
production function and reads no production result.

## Mutation replay

```bash
python3 udt_g270_completed_pair_transported_screen_ownership_2026-08-26/run_catch_proofs.py
```

Original result: `PASS`, baseline claim dictionary clean and 11/11 targeted claim mutations caught.
The fresh reviewer correctly classified this as consistency evidence rather than implementation-
level mutation assurance.

After preregistered external-review repair R1: `PASS`, the production implementation baseline is
clean, 8/8 formula-level mutations of that implementation are caught, and 5/5 separately labelled
typed-ledger mutations are caught.

## Fresh external review and repairs

The sealed intake `/tmp/udt_g270_review_mhgdqfco` returned `ACCEPT_WITH_REPAIRS`. The reviewer
accepted the bounded scientific landing and requested only the two evidence repairs registered at
commit `6bd94cff`:

1. exercise formula implementations in the mutation gate and label ledger checks separately;
2. automate off-axis ribbon regularity rather than relying only on the axis and continuity text.

Both repairs pass internally without changing the scientific landing. A repair-only external
follow-up remains required before the final external grade.

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
