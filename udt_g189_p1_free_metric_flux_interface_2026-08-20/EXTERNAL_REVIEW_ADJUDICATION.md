# G189 external-review adjudication

Date: 2026-08-20

## Primary grade

```text
G189_ACCEPTED_WITH_REPAIRS
```

The fresh read-only gpt-5.4 reviewer reran the sealed package and retained all four requested
scientific statements:

1. the metric-to-flux factorization survives conditionally;
2. the regular-center type failure of `R=R0 tanh(phi)` survives;
3. the preregistered numerical negative survives on both SNe catalogs;
4. P1 remains localized to one supplied `phi(R)` or frequency-history role rather than an
   independent screen or reciprocal-kernel ingredient.

The reviewer also found no hidden `X_max`, post-readout angular factor, Lambda-CDM distance call,
shape optimizer, or outcome-based selection of the alternate transfer control.

## Required repairs

### 1. Host-dependent DES source hashing

The original source manifest named the two DES files by absolute `/media/...` paths. Although the
sealed numerical replay used `G189_DES_ROOT="$PWD/external_data"`, the production source-integrity
gate still hashed the host paths when they existed.

Repair implemented:

- both DES manifest rows now use logical `external_data/...` names;
- production and intake-building code resolve those names only through `G189_DES_ROOT`;
- the production artifact now contains no absolute source-hash key.

### 2. Artifact dependence in the implementation-distinct replay

The original second implementation recomputed from raw data but read `PRODUCTION_RESULT.json` and
used agreement with that stored artifact as part of its own `PASS` decision.

Repair implemented:

- `verify_p1_free_flux_independent.py` no longer reads the production artifact;
- it gates only its own raw-data calculation and algebraic controls;
- `verify_package.py` explicitly joins the two independently produced results and checks their
  numerical agreement.

## Post-repair internal result

All repaired live checks pass. Production values are unchanged:

| catalog | production chi-square | independent chi-square | absolute difference |
|---|---:|---:|---:|
| Pantheon+ | 3204.9509632650042 | 3204.9509632650133 | 9.09e-12 |
| DES-SN5YR | 2685.9110340934367 | 2685.9110340934262 | 1.05e-11 |

The preregistered ceilings, zero shape-parameter count, imported transfer status, type failure, and
bounded scientific landing are unchanged.

## Repair-only follow-up

The fresh sealed repair-only review returned:

```text
G189_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED
```

It confirmed that DES sources are intake-relative through the explicitly supplied
`G189_DES_ROOT`, that the second implementation reads no production artifact or implementation,
and that `verify_package.py` owns the cross-comparison. The complete sealed replay passed with
cross-implementation residuals between approximately `1e-11` and `1e-14`.

## Final evidence grade

```text
EXTERNALLY_ACCEPTED_WITH_REPAIRS_CLOSED
__SCIENTIFIC_LANDING_UNCHANGED
```
