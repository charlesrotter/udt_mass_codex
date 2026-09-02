# G321 run record

Date: 2026-09-01

## Preregistration ancestry

The five preregistration files were committed and pushed at `863a1e9e` before the production,
independent, catch-proof, package-verification, or outcome artifacts existed.

## Registered commands

```text
python3 -S derive_local_development.py
python3 -S verify_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
```

## Internal outcomes

```text
production assertions             163894
production modes/signs            4 x 2
production periodic points        4096 per mode/sign
maximum production |H|            4.440892098500626e-15
maximum production |M|            1.7763568394002505e-15
raw/completed principal ranks      9 / 10
independent assertions            7
independent modes/signs            3 x 2
independent periodic points        3072 per mode/sign
maximum independent |H|           2.6645352591003757e-15
maximum independent |M|           1.7208456881689926e-15
maximum Ricci-loop anchor error    1.3322676295501878e-15
maximum time-reversal error        0.0
actual package mutations caught   12 / 12
```

The scripts perform no time integration and use only Python standard-library numerical/algebraic
methods. No GPU or long solve was launched.

## Fresh external review and registered repairs

The reviewer authenticated the 35-file sealed intake, replayed all four commands, and reproduced
the five generated artifacts byte-for-byte. It returned
`G321_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED` because the original hostile checks were mostly
toy/circular and the executable theorem audit used unconditional booleans for nonnumerical facts.

The repair:

1. replaces all 12 hostile checks with actual mutations of ephemeral package copies, requiring
   `verify_package.py` to fail with the preregistered reason;
2. replaces the bare theorem booleans with an eight-item typed hypothesis/evidence audit;
3. replaces word-presence report checks with exact ownership/scope/landing stamps and exact status-
   ledger cross-checks;
4. explicitly states that the standard PDE theorem is imported and not machine-proved by G321.

The repaired four-command replay passes.

## Repair-only external follow-up

The reviewer authenticated all 39 payloads, replayed the four registered commands, obtained five
byte-identical generated artifacts, and found the entire 30-file copied package unchanged after
replay. Both repairs were accepted and the scientific landing was unchanged.

Verdict: `G321_REPAIRS_ACCEPTED__CONDITIONAL_LOCAL_MARKED_UNIQUENESS_UPHELD`.
