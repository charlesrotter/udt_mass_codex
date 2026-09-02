# G323 run record

Date: 2026-09-01

## Commands

```text
python3 -S derive_unmarked_quotients.py
python3 -S verify_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

## Production

- samples: 16,384 periodic points per mode/sign;
- modes: 1, 2, 3, 4;
- signs: -1, +1;
- controls: `p=3/2`, `a=1/5`, `J0=100`, `mu=J0/9`;
- assertions: 78;
- maximum pullback error: `8.882e-15`;
- maximum extrinsic error: `9.992e-16`.

## Independent

- samples: 6,144 midpoint points per mode/sign;
- modes: 1, 2, 3, 5;
- controls: `p=7/5`, `a=1/9`, `J0=121`;
- production imported: no;
- production result read: no;
- assertions: 33;
- maximum pullback error: `2.665e-15`;
- maximum extrinsic error: `1.224e-10`.

The initial independent finite-difference Ricci derivative failed closed. The exact repair history is
preserved in `INDEPENDENT_FAILURE_AND_REPAIR.md`.

## Repository gates

- aggregate package verification: pass;
- exact 305-row premise registry and startup guards: repository-side pass; the first sealed intake
  recorded this as an external attestation rather than replayable intake evidence;
- full repository suite: repository-side repair replay `217 passed, 1 xfailed` in `141.43s`; likewise an external
  attestation in the first intake;
- fresh external adversarial review: repairable defects R1--R4, bounded landing retained;
- repair-only external follow-up: pending.
