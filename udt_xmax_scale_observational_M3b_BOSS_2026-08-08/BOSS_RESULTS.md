# M3b Phase-3 — BOSS DR12 out-of-sample test of the FROZEN ruler

Prereg `PREREGISTRATION.md` (commit **af9fa75d**). Freeze **f9c5b436** (F-RETRO
timestamp: ℓ=58.34 Mpc + the BOSS θ(z) prediction table git-committed BEFORE any
BOSS file was touched). Pipeline = the frozen M2/M3 machinery
(`v_bao.py` + `look_elsewhere.py`) run UNCHANGED. **NOTHING frozen was altered in
response to BOSS** (ℓ, r(z), the prediction, bins/shells/thresholds, the bump
search, the null count — all as committed at f9c5b436).

Status: **PROVISIONAL / verified-LEAD ceiling** (same-session). Blind
results-verifier owed before banking (prereg §5). NOT committed.

## 1. Acquisition log (Step 1 — bounded, public SDSS SAS)

Source: `https://data.sdss.org/sas/dr12/boss/lss/` (DR12v5 combined LSS,
PRE-reconstruction). Fetched to `/media/udt-admin/ScratchDisk/Data/boss_dr12/`
(DESI dir untouched). All gzip-verified OK.

| file | bytes | rows |
|---|---|---|
| galaxy_DR12v5_LOWZ_North  | 73,432,436 | 317,780 |
| galaxy_DR12v5_LOWZ_South  | 32,341,613 | 145,264 |
| galaxy_DR12v5_CMASS_North | 138,873,951 | 618,806 |
| galaxy_DR12v5_CMASS_South | 51,580,500 | 230,831 |
| random0_DR12v5_LOWZ_North  | 1,578,615,321 | 15,678,814 |
| random0_DR12v5_LOWZ_South  | 713,300,258 | 7,084,128 |
| random0_DR12v5_CMASS_North | 3,239,878,693 | 32,151,741 |
| random0_DR12v5_CMASS_South | 1,172,229,517 | 11,636,252 |

**One random file per cap (`random0`)** used (prereg-authorized: split-RR over a
single file reduces exactly to the single-RR estimator at these densities;
F=1 declared). Shipped randoms are ~50x the data.

## 2. Loader + blacklist (Step 2 — F-IMPORT-LCDM, machine-tested)

`boss_loader.py` maps BOSS DR12v5 column names onto the frozen `v_bao.Catalog`.
Completeness weight (standard, Reid et al. 2016):
**w = WEIGHT_SYSTOT · (WEIGHT_CP + WEIGHT_NOZ − 1)** — a completeness weight
(fiber-collision + z-failure + imaging-systematics), NOT a fiducial weight.
`use_sys=False` (nosys variant) drops WEIGHT_SYSTOT. **Randoms carry weight = 1**
(no completeness columns; they ARE the selection function).

BLACKLIST (physically unreturnable, tested in `test_boss_blacklist.py`, 7/7 PASS):
`NZ`, `NBAR` (n(z), fiducial cosmology), `WEIGHT_FKP` (fiducial P0·n(z)), `COMP`,
any `COMOVING`/`DISTANCE`/`DC` column, any `_rec` reconstruction path. The loader
raises `BossBlacklistViolation` BEFORE any I/O for any blacklisted/non-whitelist
column or `_rec` file.

## 3. Kept-shell census (Step 3 — DZ=0.05, frozen 5e4 weighted-galaxy floor)

Δz=0.05 by density; LOWZ [0.15,0.43), CMASS [0.43,0.70); a shell is kept iff its
cap-combined weighted count ≥ 5e4 (frozen floor). **9 shells kept, 3 dropped.**

| sample | shell | Σw | kept |
|---|---|---|---|
| LOWZ | [0.15,0.20) | 43,866 | dropped (<5e4) |
| LOWZ | [0.20,0.25) | 52,360 | KEPT |
| LOWZ | [0.25,0.30) | 61,205 | KEPT |
| LOWZ | [0.30,0.35) | 87,925 | KEPT |
| LOWZ | [0.35,0.40) | 85,942 | KEPT |
| LOWZ | [0.40,0.43) | 39,393 | dropped (thin, <5e4) |
| CMASS | [0.43,0.48) | 131,457 | KEPT |
| CMASS | [0.48,0.53) | 232,440 | KEPT |
| CMASS | [0.53,0.58) | 215,108 | KEPT |
| CMASS | [0.58,0.63) | 151,050 | KEPT |
| CMASS | [0.63,0.68) | 82,753 | KEPT |
| CMASS | [0.68,0.70) | 18,888 | dropped (thin, <5e4) |

## 4. Per-shell bump table (frozen bump search; full window [0.3,12]°, no seeding)

θ_obs = fitted bump center (deg); σ_c = DERIVED center error σ_b/√Δχ² (the freeze
method); θ_pred = ℓ_frozen/r(z_c) with the FROZEN r(z); ℓ' = radians(θ_obs)·r(z_c).

**variant sys** (global trials-corr p = 0.0000; joint p = 0.0000):

| shell | z_c | θ_obs | σ_c | θ_pred | ℓ' (Mpc) | local p | within? |
|---|---|---|---|---|---|---|---|
| LOWZ 0.20–0.25 | 0.225 | 2.111 | 0.070 | 4.755 | 25.9 | 0.290 | no |
| LOWZ 0.25–0.30 | 0.275 | 10.961 | 0.162 | 4.115 | 155.4 | 0.697 | no |
| LOWZ 0.30–0.35 | 0.325 | 0.251 | 0.023 | 3.673 | 4.0 | 0.983 | no |
| LOWZ 0.35–0.40 | 0.375 | 6.734 | 0.107 | 3.350 | 117.3 | 0.730 | no |
| CMASS 0.43–0.48 | 0.455 | 4.647 | 0.163 | 2.984 | 90.8 | 0.047 | no |
| CMASS 0.48–0.53 | 0.505 | 10.249 | 0.033 | 2.816 | 212.4 | 0.040 | no |
| CMASS 0.53–0.58 | 0.555 | 4.043 | 0.079 | 2.678 | 88.1 | **0.000** | no |
| CMASS 0.58–0.63 | 0.605 | 2.950 | 0.124 | 2.564 | 67.1 | 0.877 | no |
| CMASS 0.63–0.68 | 0.655 | 7.128 | 0.073 | 2.468 | 168.5 | 0.070 | no |

**variant nosys** (global p = 0.0067; joint p = 0.0067): θ_obs / ℓ' track sys to
~1–2% on every shell (weight-variant stable **centers**); the only material
variant differences are in significance of the two weakest CMASS shells. Full
table in `boss_prediction_test.json`.

## 5. Look-elsewhere (300-null, frozen)

- **Feature detected (both variants):** global trials-corrected p = **0.0000**
  (sys) / **0.0067** (nosys), below the frozen 0.01 bar. The mundane O-D
  (no-feature, the cheapest kill) is therefore **NOT** the outcome — there is
  angular power beyond the 9-shell + full-window look-elsewhere noise. Driven by
  CMASS 0.53–0.58 (Δχ²=24.8, local p=0.000) and CMASS 0.48–0.53 / 0.43–0.48.
- Radial-leg triggers (Δχ² > null 95th): 3 shells (sys) / 2 (nosys), all CMASS.
  Radial estimator not built (honest gap, as in M3).

## 6. Frozen-prediction test (Step 4 — prereg §3, frozen pass/fail)

**(a) Feature at threshold? YES** (spares O-D). **(b) Does the frozen ℓ=58.34 Mpc
predict the BOSS θ_BAO? NO — 0/9 shells** have θ_obs within the DERIVED center
error of θ_pred, in EITHER variant. The observed bump centers scatter across the
whole window (0.25°–11°); per-shell ℓ' scatters **4–212 Mpc**, nowhere coherently
near 58 Mpc. The frozen prediction that θ FALLS monotonically 4.8°→2.5° is not
reproduced. **(c)** The detected power does not form a clean drift either way; the
significant shells (CMASS 4.0°, 10.2°, 4.6°) do not thread a single ruler.

The frozen look-elsewhere's floated joint (profile, s, shape) fit — which is
allowed to re-fit the scale freely — does reach p<0.01, but lands at
**ℓ_joint ≈ 169 Mpc (sys, profile P3, shape 0.55) vs ≈ 224 Mpc (nosys, P3,
shape 1.23)**: ~3–4× the frozen 58.34 Mpc, profile P3 (frozen was P1), and
**variant-UNSTABLE by 33%** — i.e. no stable BOSS ruler at the frozen scale, and
the floated ruler is not robust. (Same instability class as the M3 in-sample
joint fit.)

### LANDING (equal temperature, F-STEER): **M3b-PARTIAL**
A feature IS detected at threshold, but at ℓ' ≠ the frozen ℓ (0/9 shells thread
58.34 Mpc; floated joint ruler ~169–224 Mpc, variant-unstable, wrong profile).
**The frozen single-universal-ruler out-of-sample SCALE prediction FAILS.** This
CORROBORATES the in-sample freeze finding (χ²/dof=144, anti-drift, 1.75× same-z
tracer split): **ℓ is a magnitude (~tens of Mpc), not a threaded universal
ruler.** Reported straight; unfavorable to the single-ruler reading.

**BOSS ℓ' and ℓ'/R_w (reported regardless):** per-shell ℓ' = 4–212 Mpc (no single
value); floated joint ℓ' ≈ 169 Mpc (sys) → ℓ'/R_w ≈ 0.077, ≈ 224 Mpc (nosys) →
0.102 — vs the frozen 58.34 Mpc / 0.0265. Variant-unstable; do NOT bank a BOSS ℓ'.

## 7. GPU spot-check (amended-v2 criterion, Category-A)

CPU-vs-GPU bin-identity on 2 designated BOSS shells × {DD, DR} — **all 4 PASS**:
CMASS 0.53–0.58: DD max rel 2.85e-12, DR 1.43e-10; LOWZ 0.30–0.35: both 0.0.
All: small-cell whole-pair census = 0; total rel ≤ 1.05e-12. (Criterion:
per-cell rel≤1e-8 AND small-cell whole-pair==0 AND total rel≤1e-9.) The GPU
workhorse is validated bin-identical to the CPU tree.

## 8. Premises / caveats (all travel)

- **F-RETRO honored:** ℓ, r(z), the θ(z) prediction, DZ=0.05, the 5e4 floor,
  θ-window [0.3,12]°/40 bins, 24-region jackknife, the bump search, the 300-null
  count, and the 0.01 threshold are all as frozen at f9c5b436; none was changed
  after seeing BOSS.
- **Category-A conditioning (declared on THROUGHPUT, before any assembly/verdict):**
  (i) GPU workhorse backend — the shipped BOSS random density makes the CPU tree
  exceed the anti-hang budget; the GPU counter is bin-identical (M2 equivalence
  test + the §7 spot-check). (ii) Uniform random downsample to 10× the data
  (RAN_FACTOR=10; initially 20, reduced after a single-shell timing test showed
  20× exceeds budget on CMASS) — the LS estimator is unbiased in random count;
  10× RR/DR shot noise sits below the 24-region jackknife variance; the angular
  selection function is preserved.
- **Inherited:** diagonal jackknife covariance (M2 condition) on every
  significance — bin-bin correlated broadband residuals are NOT modelled, so
  per-shell Δχ² significances are plausibly INFLATED; the "feature" may be
  residual smooth power the cubic null under-absorbs rather than a BAO peak. This
  caveat strengthens, not weakens, the PARTIAL landing.
- **F-ANCHOR:** θ_pred/ℓ in Mpc ride M_B=−19.253±0.027 (SNe ladder); ℓ/R_w and
  the θ-shape test are anchor-free.
- Files: `boss_loader.py`, `test_boss_blacklist.py`, `run_boss.py`,
  `compare_prediction.py`, `boss_checkpoints/` (18 shell npz+json),
  `boss_results_{sys,nosys}.json`, `boss_prediction_test.json`, `boss_run_log.txt`.

## 9. CONSOLIDATED (blind results-verifier — SUSTAINED, 2026-08-08)

**Verdict: SUSTAINED** (`RESULTS_VERIFIER_REPORT.md`). Both variant legs reproduce
incl. a raw-catalog recompute of CMASS 0.53–0.58 to machine precision; no LCDM
leakage found. **F-RETRO timeline clean:** prereg af9fa75d (18:59) → freeze
f9c5b436 (19:05:30) → earliest BOSS file contact (19:09:13) — the freeze preceded
any BOSS contact by 3.7 min (hash = timestamp).

**Landing restated — M3b-PARTIAL (equal temperature):** a feature is REPLICATED in
both weight variants (global trials-corr p = 0.000 / 0.007 < 0.01; O-D does NOT
survive), but the frozen single-universal ruler **ℓ = 58.34 Mpc FAILS
out-of-sample: 0/9 shells thread it** (robust to a fair center error), and there is
**no stable BOSS ruler** — the floated joint ℓ_joint ≈ 169 / 224 Mpc (profile P3,
variant-unstable ~33%), ~3–4× the frozen scale. Per-shell ℓ′ scatters 4–212 Mpc.

**Caveats carried:** the diagonal-jackknife covariance (no bin-bin correlation)
travels on the detection — per-shell Δχ² plausibly inflated (the feature may be
broadband residual the cubic null under-absorbs), which strengthens PARTIAL.
**Category-A flagged:** GPU workhorse backend + RAN_FACTOR 20→10 downsample —
declared on throughput before any verdict; LS unbiased in random count; GPU
bin-identity spot-checked (§7).

**Four-check:** preregistered (af9fa75d) ✓ · full-space run / bounded slice
justified (9-shell census + Cat-A conditioning stated) ✓ · blind-verified
(SUSTAINED) ✓ · every forced premise audited (F-RETRO timeline, F-IMPORT-LCDM
machine-test, F-ANCHOR) ✓. **Status: verified LEAD** (same-session; the external
bar travels).

**Ruler-free reading (methodological catch — the forward lead):** the phenomenon
is REAL and now CROSS-SURVEY replicated (DESI + BOSS both show angular power beyond
noise), but it is **NOT a single geometric ruler** — it does not thread one ℓ, and
the same-z tracer-split (in-sample, 1.75×) is corroborated by BOSS's incoherent,
tracer/redshift-dependent centers. This points AWAY from a static comoving ruler
and TOWARD a φ-matter coupling (tracer- and depth-dependent), the forward lead.
