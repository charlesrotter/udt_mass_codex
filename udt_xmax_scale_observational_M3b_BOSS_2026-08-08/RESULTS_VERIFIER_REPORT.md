# M3b BOSS — BLIND RESULTS-VERIFIER REPORT

Verifier: blind, fresh-context, no stake. Date 2026-08-08. Branch grok.
Package `udt_xmax_scale_observational_M3b_BOSS_2026-08-08/`. Brief: hunt reasons the
M3b-PARTIAL landing must NOT be recorded. Not committed.

## 1. F-RETRO TIMELINE (primary) — CLEAN, does NOT fire

Git + filesystem ordering (all 2026-08-08, times -0400):
- Prereg `af9fa75d` committed **18:59:21** (contract frozen; no data touched).
- Freeze `f9c5b436` committed **19:05:30** — this commit carries ℓ=58.34 Mpc,
  r(z) (inv_n=0.947, X_eff=2086.0 → R_w=2202.7), and the frozen θ(z) BOSS
  prediction table. This is the F-RETRO timestamp.
- BOSS galaxy catalogs mtime **19:09:13 – 19:09:27** (all AFTER the freeze).
- BOSS random catalogs mtime **19:13:00 – 19:22:01** (all AFTER the freeze).

The earliest BOSS file contact (19:09:13) is ~3.7 min AFTER the freeze commit
(19:05:30) and ~10 min after the prereg. FREEZE PRECEDES ALL BOSS DATA CONTACT.
The frozen ℓ=58.34 is hardcoded verbatim in `compare_prediction.py` (ELL=58.34,
INV_N=0.947, XEFF=2086.0) and matches FROZEN_PREDICTION.md; `run_boss.py`/
`boss_loader.py` do not alter ℓ, r(z), bins, window, thresholds, or null count.
No evidence any frozen quantity was changed after BOSS was seen.
**F-RETRO: not fired. Timeline clean.**

## 2. F-IMPORT-LCDM — CLEAN

- `test_boss_blacklist.py` re-run independently: **7/7 PASS**.
- Independent load attempts of NBAR, WEIGHT_FKP, COMOVING, NZ via `boss_loader`
  all raise `BossBlacklistViolation` before any I/O. Confirmed unreturnable.
- Grep of the package for fiducial/comoving/r_d/reconstruction/Planck/Omega_m/
  astropy.cosmology leakage: **none** (only blacklist-machinery mentions).
- Weight formula is completeness-only: `w = WEIGHT_SYSTOT·(WEIGHT_CP+WEIGHT_NOZ−1)`
  (Reid et al. 2016), nosys drops SYSTOT; randoms weight=1. NOT fiducial. Confirmed.

## 3. SPOT-RECOMPUTE (driver shell CMASS 0.53–0.58 sys)

- **Analysis stage** (bump fit + local-p from saved w(θ), committed pipeline +
  seed): RECOMPUTED dchi2=24.7516, θ_b=4.0431, σ_b=0.3914, local_p=0.0000,
  seed=20261462 — **bit-identical** to the checkpoint.
- **Raw end-to-end** (LS w(θ) from raw catalogs via frozen pipeline, GPU, t=385s):
  vs checkpoint — max|Δw|=9.9e-16, max|Δσ|=5.2e-16, DD rel=1.3e-16, DR rel=0.0,
  N_data=[147120,53162], N_ran=[1479536,531849]. **Machine-precision match.**
- Independent θ_pred(z) recompute (ℓ/r(z)): z=0.20→5.197°, z=0.55→2.691°,
  z=0.225→4.755°, z=0.555→2.678°, z=0.65→2.477° — matches FROZEN_PREDICTION.md
  and BOSS_RESULTS.md exactly.
- `compare_prediction.py` re-run: 0/9 shells thread in BOTH variants; per-shell
  ℓ' = 4.0–212.4 Mpc. **Threading-FAILS verdict reproduces; not a bug.**

## 4. IS THE PARTIAL HONEST IN BOTH DIRECTIONS? — YES

(a) **Diagonal-jackknife caveat travels WITH the detection.** BOSS_RESULTS §8
states the diagonal jackknife plausibly INFLATES per-shell Δχ² and the "feature"
may be broadband residual the cubic null under-absorbs — and explicitly notes
this "strengthens, not weakens, the PARTIAL landing." The caveat hedges the
detection, not the fail. Honest.

(b) **Fair-error test — the fail is NOT manufactured by a too-tight error.**
Replacing the DERIVED center error (σ_b/√Δχ², tight) with the FULL bump width
σ_b (generous): still **0/9** thread. The closest shell (CMASS 0.58–0.63, 1.87σ_b
off) is a non-significant bump (local_p=0.877); the significant shells are 3.1–68σ_b
off θ_pred. θ_obs scatter 0.25°–11° vs θ_pred 2.5°–4.8° monotone. The fail is robust.

(c) **"No stable BOSS ruler" is the right read.** Floated joint fit lands at
profile **P3** (frozen was P1); shape = 0.55 (sys) vs 1.23 (nosys) and s_rad
0.081 vs 0.108 — variant-unstable (~33%). BOSS_RESULTS correctly says "do NOT
bank a BOSS ℓ'." Confirmed against boss_results_{sys,nosys}.json.

## 5. PREREG CONFORMANCE — CONFORMS

- Pipeline frozen from M2/M3 (v_bao + look_elsewhere) unchanged; bins/window
  [0.3,12]°/40 log, 24-region jackknife, 300-null, 0.01 threshold all as frozen.
- Category-A declarations (GPU backend; RAN_FACTOR=10, reduced from 20 on a timing
  test) are genuinely throughput-only, declared in committed code/docstrings, and
  do NOT touch ℓ/criteria/bins/thresholds. GPU spot-check 4/4 PASS (re-read from
  log: mrel≤1.4e-10, census 0, total≤1.05e-12). Ordering: shells → spot-check →
  assembly/global_p (verdict last). Legitimate.
- Global feature: global_p sys=0.0000, nosys=0.0067, both <0.01 → feature detected.
  Reproduces via compare_prediction.py.

## 6. AMENDMENTS OWED (minor, non-blocking)

- **boss_census.json ABSENT.** The brief and BOSS_RESULTS §8 file list reference
  it, but the artifact is not on disk. The census (9 kept / 3 dropped) is
  documented in BOSS_RESULTS §3 and regenerable via `run_boss.py --census`. No
  scientific impact; a documentation/artifact gap — either generate+commit it or
  drop the reference.
- The Category-A RAN_FACTOR 20→10 reduction is honestly disclosed as a throughput
  decision; it is legitimate but should stay flagged as a post-prereg (Category-A)
  choice in the consolidated record (it already is).

## FINAL VERDICT: SUSTAINED (with one minor artifact amendment)

The M3b-PARTIAL landing is sound. F-RETRO timeline is clean (freeze precedes all
BOSS contact). No LCDM leakage; blacklist enforced. The feature detection AND the
single-ruler threading-fail (0/9, robust to a fair error) both reproduce. The
diagonal-jackknife caveat travels honestly with the detection; the floated joint
ruler is genuinely variant-unstable (P3, 33%). No frozen number failed to
reproduce. Only owed item: the missing boss_census.json artifact (cosmetic).
