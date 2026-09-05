# G352 run record

Date: 2026-09-05
Python: system `python3`, standard library only, `-B -S`
GPU: not used; no long solve

## Preregistration chronology

- `f5ee3393`: initial G352 preregistration committed and pushed before outcome work.
- `14afc199`: R1 phase-orientation sign repair committed and pushed before outcome work.
- `b0bc9f24`: authenticated fresh external `REPAIR` verdict and R2 scope repairs committed and
  pushed before repair execution.

## Saved-evidence commands

Run from the G352 package directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -S derive_clock_rate_readout.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_clock_rate_readout_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -B -S run_catch_proofs.py
```

Results:

- repaired production: 103,648/103,648 assertions over 2,400 genuinely distinct generated base
  states;
- repaired implementation-distinct: 73,889/73,889 assertions over 2,700 genuinely distinct
  generated base states;
- repaired semantic mutations: 18/18 caught.

The repaired registered no-write aggregate is run after this record and the aggregate verifier are
present. Its result is 48/48 and belongs in `VERIFICATION_RESULT.json`. A second execution with
`UDT_NO_WRITE=1` reproduced 48/48 without changing package files.

Repository checks from the repository root:

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest tests/
```

The pre-banking exact 334-row premise audit passed. After adding the externally accepted G352 row,
the exact 335-row premise audit also passed. The final full suite returned 137 passed and one
expected documented xfail in 402.00 seconds.

The fresh external reviewer authenticated 36 payloads and replayed the original 36/36 package. It
retained the conditional `R A^-1` algebra but required the continuous/atomic distinction,
nonnegative product measure, explicit factorization conditions, and evidence-count regrading now
implemented under R2.

The sealed R2 repair-only reviewer authenticated all 42 manifest payloads in the exact 44-file
intake and independently replayed the four registered no-write checks: 103,648/103,648 production,
73,889/73,889 implementation-distinct, 18/18 hostile mutations, and 48/48 aggregate gates. Session
`01a07355-b749-7a01-8d4f-226a7faaf11b` returned
`ACCEPT_G352_R2_REPAIR_COMPLETION`. Its exact 13,241-byte response has SHA-256
`f04c7d38567bdb56854c1ee6fc4da80b0307be3aa62286127a61775dcaf3760e`.
After banking the exact response, the aggregate gained one response-integrity gate and passed
49/49 under the same no-write controls.
