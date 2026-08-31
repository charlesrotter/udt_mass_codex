# G308 run record

Date: 2026-08-31

## Preregistration

- pushed commit: `aaea5c12`
- parent: `5a199ca6`
- no G308 executable or outcome existed in that commit

## Production

```bash
python3 -S derive_global_chirality_coherence.py
```

PASS: candidate B; 11,526 exact assertions; 36 directed frames; 216 global point cases; both
chiralities; five positive scale/rate controls.

## Independent replay

```bash
python3 -S verify_global_chirality_independent.py
```

PASS: 79,200 implementation-distinct checks over 1,200 random frames; maximum normalized error
`2.020605904817785e-14`; no production import.

## Hostile controls

```bash
python3 -S run_catch_proofs.py
```

PASS: eight direct exact mathematical mutations and fourteen semantic/ownership mutations caught.

## Premise audit

```bash
python3 verify_current_scientific_premises.py
```

PASS: 289 registry rows; registry SHA-256
`10c7b53fc2820a63c7fee40d1a9d06325c7a3cb8c17d58329646eaf191de5ba8`.

## Repository regression

```bash
python3 -m pytest -q
```

PASS: 199 passed and one expected xfail in 136.74 seconds. The xfail is the pre-existing
matter-sector habit-pin gate; G308 introduced no regression.

## Fresh external review

The sealed 41-file intake returned `G308_REPAIRABLE_DEFECTS`. The reviewer found no bounded
scientific defect and accepted the strongest landing. It found one medium sealed-path portability
defect in `verify_package.py` and one low evidence-quality caveat: the first randomized verifier
was non-importing but reconstructed the same outer-product ansatz as production.

## Preregistered repairs

R1--R4 were preregistered and pushed at `d212fb42` before repair implementation.

- R1: unique repository/sealed source resolution; missing and ambiguous layouts rejected.
- R2: 121,600 method-distinct Hodge/group-orbit checks; maximum error
  `1.7763568394002505e-15`.
- R3: the original 79,200 checks regraded as a constructive randomized cross-check.
- R4: explicit portability and rebuilt sealed-intake gates.

All four repairs pass internally. A freshly rebuilt 51-file sealed intake ran all six registered
commands without symlinks or manual staging. Six load-bearing outcome files were byte-identical to
the repository copies. The post-repair premise audit passed, and the full repository regression
returned 199 passed with one expected xfail in 137.46 seconds. Repair-only external follow-up
remains pending.
