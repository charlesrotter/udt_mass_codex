# G209 run record

Date: 2026-08-21

## Environment

- working tree: `/home/udt-admin/udt_mass_codex`
- branch: `grok`
- preregistration commit: `b5c40cc2`
- computation: CPU, exact SymPy/Fraction plus 120-digit `mpmath`
- GPU: not used

## Commands

```bash
python3 udt_g209_g205_timespace_shift_robustness_2026-08-21/derive_timespace_shift.py
python3 udt_g209_g205_timespace_shift_robustness_2026-08-21/verify_timespace_shift_independent.py
python3 udt_g209_g205_timespace_shift_robustness_2026-08-21/run_boundary_diagnostics.py
python3 udt_g209_g205_timespace_shift_robustness_2026-08-21/run_catch_proofs.py
```

## Results

- production assertions: 21
- independent cases: 10,000
- independent assertions: 100,001
- high-precision profiles: 4 at 120 digits
- hostile catches: 25
- all completed finite gates: PASS

The first production attempt encountered a SymPy inequality-solver limitation. Before any result
was obtained, the brittle solver invocation was replaced by the exact factorization and its two
roots. A second on-shell substitution check was likewise expressed by solving the constraint for
`L^2`. Neither change altered the preregistered mathematical test or target bound.

## Fresh external review

- intake: `/tmp/udt_g209_review_52plr6v9`
- scope SHA-256: `2699a11aa5368ae0f36df2ab1936db819181a627bf093c3ea27776a9138123d5`
- sealed tree SHA-256: `797462ac0b853c2e8e94f0b478ca7497df21c4217ea97b636ab0860eaf089566`
- reviewer: external Codex `gpt-5.4`, high reasoning, web disabled, approval disabled, read-only
- process exit: zero
- verdict: `VERIFIED_WITH_CAVEATS`
- payload hashes: 33/33 passed
- registered no-write replay: passed
- repairs: explicit compact-slab extension statement and one TeX typo; landing unchanged

## Repair-only external follow-up

- intake: `/tmp/udt_g209_repair_followup_ke4dvplh`
- scope SHA-256: `731ac771b193cdcf074fa04d4d9418eda45d76b31037b60797b7914d796454c3`
- sealed tree SHA-256: `cf362fab780df23542f327bffda7c0f1edfce18a0de4167d2691d3eea2e23765`
- reviewer: external Codex `gpt-5.4`, high reasoning, web disabled, approval disabled, read-only
- process exit: zero
- verdict: `G209_REPAIR_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED`
- payload hashes: 37/37 passed
- registered no-write replay: passed
