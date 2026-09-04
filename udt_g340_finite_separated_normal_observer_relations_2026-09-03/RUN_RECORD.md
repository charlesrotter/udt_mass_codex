# G340 run record

Date: 2026-09-03

## Preregistration

- commit: `d2b68663`
- source hashes: `SOURCE_SCOPE.tsv`
- result alternatives frozen before execution

## Production

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -S derive_finite_pair_relations.py
```

Result: `3868/3868`, alternative A.

Coverage: 108 one-way principal cases, 108 radar cases, six symmetric radar controls, six winding
families, and 400 general nonprincipal null-Hamiltonian/quadrature cases.

## Independent

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -S verify_finite_pair_independent.py
```

Result: `5988/5988`.

Coverage: 360 principal arrival/frequency cases solved by direct metric quadrature and bisection,
180 radar cases, 1,000 general direct-metric null cases, and six winding families. The route uses
Gauss--Legendre integration rather than production Simpson integration and imports no production
code or result.

## Hostile

```text
PYTHONDONTWRITEBYTECODE=1 python3 -B -S run_catch_proofs.py
```

Result: `15/15` hostile mutations caught.

No GPU, network, observation, package download, protected draft, or long solve was used.

## Sealed-replay dress rehearsal

The first local sealed-copy rehearsal exposed a package-relative source lookup. The verifier was
repaired to authenticate the sealed `sources/` tree directly when `.git` is absent. No formula,
result, landing, tolerance, or scientific claim changed. The superseding intake was rebuilt only
after the repaired aggregate passed both repository and sealed layouts.

## Fresh external review

- authorized sealed intake: `/tmp/udt_g340_review_f3dk5b10`;
- authenticated payloads: `35/35` plus manifest and detached seal, `37` total files;
- reviewer replay: production `3868/3868`, independent `5988/5988`, hostile `15/15`, pre-review
  aggregate `17/17`;
- verdict: `ACCEPT_G340_BOUNDED_FINITE_PAIR_RELATION_CLASSIFICATION`;
- findings: none at critical, high, medium, or low severity; no required repair;
- post-review aggregate including return authentication: `19/19`.
