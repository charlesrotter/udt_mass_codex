# G320 run record

Date: 2026-09-01
Device: CPU
Arithmetic: exact rational identities plus IEEE-754 binary64 periodic controls
Long solve: none

## Commands

```text
python3 derive_physical_quotient.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

## Production

```text
PASS_PENDING_EXTERNAL_REVIEW
290 assertions
modes 1,2,3,4; signs -1,+1; 16,384 periodic points per control
maximum metric seed-rewrite error 3.552713678800501e-15
maximum physical-A seed-rewrite error 1.6653345369377348e-16
```

## Independent

```text
PASS
59 assertions
modes 1,3,5; signs -1,+1; 3,072 periodic points per control
direct Christoffel-Ricci index loops
maximum metric seed-rewrite error 1.7763568394002505e-15
maximum physical-A seed-rewrite error 3.885780586188048e-16
```

## Hostile checks

```text
PASS
26/26 mutations caught
```

## Aggregate and repository gates

```text
G320 package verification PASS_PENDING_EXTERNAL_REVIEW
current exact premise registry PASS
pytest -q: 215 passed, 1 known documented xfail in 140.50 s
```

## External review

```text
sealed payloads authenticated: 32/32
registered commands replayed: 4/4
generated artifacts byte-identical: 5/5
verdict: G320_ACCEPTED__GENUINE_INITIAL_GEOMETRY_FREEDOM_UPHELD
```
