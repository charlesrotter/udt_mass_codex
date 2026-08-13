# R1 ingestion and random-null outcome

Date: 2026-08-12
Grade: `VERIFIED-WITH-CAVEATS`

## Result

The complete registered R1 BOSS scope passed its ingestion and deterministic random-only numerical
controls:

```text
OBSERVED__R1_RANDOM_NULL_CONTROLS_PASS
```

- 110/110 fine-shell/sample/cap cells were sampled;
- 220 random-only Landy--Szalay curves were produced, two disjoint replicas per cell;
- 26,180 angular-bin rows were retained;
- all 330 registered per-replica and replicate-difference guards passed;
- 12 compact actual-random-catalog pair-count anchors matched an independent brute-force count in
  every bin;
- a separate verifier recomputed every normalized count, every Landy--Szalay value, every summary,
  and every guard from the saved raw counts;
- no galaxy angular pair count was computed.

The largest absolute normalized diagnostic was `4.7754163996979173` in CMASS South shell 35,
replicate 0. The largest diagnostic RMS was `1.2340262789069887` for the LOWZ North shell 19
replicate difference. Both are below the preregistered guards of 12 and 3, respectively. These are
numerical contamination proxies, not physical significances or calibrated p-values.

## Input populations in the registered redshift scope

| Sample | Cap | Galaxy count | Official-random count |
|---|---:|---:|---:|
| CMASS | North | 568,776 | 29,588,847 |
| CMASS | South | 208,426 | 10,507,945 |
| LOWZ | North | 248,237 | 12,276,023 |
| LOWZ | South | 113,525 | 5,549,994 |

The smallest shell-wise available-random/galaxy ratio was approximately `48.13`, exceeding the
12x population required by the two disjoint 1x/5x partitions.

## Resource observation

- wall time: `5458.909442892298 s` (about 91 minutes);
- peak RSS: `1.6273994445800781 GiB`;
- engine: Python 3.10.12, NumPy 2.2.6, SciPy 1.15.3;
- device: CPU only.

## What was learned

`OBSERVED`: the frozen BOSS inputs are internally usable over the complete registered fine-shell
space, and the exact estimator/mask machinery passes its preregistered random-only contamination
test. This removes a concrete numerical and survey-mask blocker before the galaxy pattern is opened.

It does **not** show that a galaxy oscillation exists, certify a physical covariance, identify an
origin, import an acoustic interpretation, validate UDT, or constrain `X_max`. The Poisson-like
proxy used here is deliberately only a diagnostic. R2 remains the first galaxy-pattern calculation.

## Four evidence gates

1. **Preregistered:** `YES`. The implementation, partitions, thresholds, outputs, resource stops,
   and conclusion ceiling were frozen and pushed at commit `901019ec` before execution.
2. **Full space or bounded scope justified:** `YES_FOR_R1`. All 110 registered fine-shell cells and
   both random replicas were completed. This is the bounded BOSS R1 random-only scope, not R2/R3.
3. **Independently verified on the load-bearing premise:** `YES_WITH_STATED_SCOPE`. A separate
   implementation recomputed the complete estimator algebra from saved raw counts, while brute
   force reproduced 12 compact actual-catalog tree-count anchors. A second full large-tree census
   was not repeated.
4. **Every premise audited:** `YES_FOR_R1`. No galaxy pattern, cosmology, UDT response, distance
   conversion, feature target, or physical uncertainty entered the outcome.

The caveat in the grade is the deliberately limited meaning of the null proxy and the compact—not
full-scale—independent pair-count replay. Neither caveat blocks the registered R2 central-pattern
calculation.
