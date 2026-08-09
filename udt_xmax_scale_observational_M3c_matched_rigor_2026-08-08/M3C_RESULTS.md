# M3c RESULTS — matched-rigor full-covariance re-run (DESI + BOSS)

Prereg `PREREGISTRATION.md` (commit 4bcd9e09, FROZEN). Phase-3 build+rerun agent,
2026-08-08, branch grok. mu NOT invoked (data-rigor step). **Verified LEAD:
blind results-verifier returned SUSTAINED-AMENDED (amendments applied in place,
see CONSOLIDATED); nothing banks/amends M3/M3b until Charles reviews.**

## 0. Anti-steering stamp
Every upgrade below was adopted from the FROZEN prereg BEFORE its ruler effect was
seen. The outcome is MIXED and reported at equal temperature: the DESI feature +
tracer split SURVIVE, the BOSS detection DEFLATES. No upgrade was added/dropped
after seeing its effect (F-STEER / F-RETRO honored).

## 1. STEP 1 — banked-counts inventory (what is actually on disk)
M3 (DESI) and M3b (BOSS) checkpoints bank, per (shell,variant): `theta(40)`,
`w(40)`, `sig(40)`, **`cov_jk(40,40)` FULL**, and TOTAL `DD/DR/RR(40)`.
They do **NOT** bank the region-blocked `[T,T,40]` count arrays nor the per-region
leave-one-out `w_jk` vectors. **BUT** the banked `cov_jk` IS the full T=48 region
jackknife covariance at 40 bins (cap-combine → T = 2 caps × 24 regions; verified:
numerical rank = 40, so T>40). **M3 used only its DIAGONAL** (the flagged M2
caveat) — at 40 bins with 48 regions the inverse is near-singular (Hartlap dof
48−40−2 = 6), which is exactly why M3 stayed diagonal.

→ Route taken = FROZEN prereg §1.1(b): reduce N_bins so C is well-conditioned,
**ZERO recount**, binning FROZEN to 12 log bins on [0.3,12] deg.

## 2. STEP 2 — the FULL bin-bin covariance (`build_cov.py` → `cov_out/`)
The banked 40-bin full cov is rebinned to 12 bins with a FIXED linear operator
A(12×40): `w12 = A w40`, `C12 = A C40 Aᵀ`. This is **mathematically identical** to
forming the 12-bin jackknife covariance from the (linearly-rebinned) per-region
vectors, since A(dev_k) = dev of (A·w_jk_k) and cov = c·Σ_k dev_k dev_kᵀ. The only
definitional choice: the coarse-bin estimator is the RR-pair-count-weighted average
of the fine-bin LS w's rather than a from-scratch coarse-bin LS — a legitimate,
data-only estimator (RR = banked random-pair counts; **no theory P(k), no mocks, no
fiducial cosmology**). DISCLOSED.
- **N_reg = 48, N_bins = 12.** Hartlap `(48−12−2)/(48−1) = 0.7234` on C⁻¹;
  Percival `m = 0.9735` (σ ×0.9867) on parameter errors (mild — N_reg≫N_bins).
- **All 122 shell-variants POSITIVE-DEFINITE.** Condition numbers: min 200,
  median 436, max 17509. C is well-invertible at 12 bins.
- Off-diagonal correlation is **strong** (mean |corr| 0.18–0.52, max 0.86–0.89) —
  the diagonal approximation was genuinely inadequate; the upgrade is warranted.
- BOOTSTRAP arm (prereg §1.1b): its premise — that region-blocked counts were
  banked — was **factually false** (inventory §1), so it is INFEASIBLE without a
  recount. Adjudicated NON-LOAD-BEARING (verifier): C12 is an exact image of a
  genuine 48-sample jackknife, not a construction the bootstrap would need to
  validate. Remains OWED (via recount) as post-hold work; the JK C eigenspectrum
  is non-pathological (all positive, condition numbers moderate) in its place.

## 3. STEP 3 — re-fit under proper C. BEFORE/AFTER significance tables
Matched 12-bin binning throughout; BEFORE = diagonal-only weighting (M2/M3
condition), AFTER = full C⁻¹ (Hartlap) + Percival on parameter errors. Frozen scan
= 40 fine log-centers × width grid (0.10,0.20,0.35,0.60) in ln-θ (identical trials
to M3); null recalibrated by drawing y~MVN(0,C12), independent per shell (crc32
seed on BASE 20260807).

### (a) DETECTION — global trials-corrected p
| survey | variant | M3/M3b (diag,40-bin) | M3c (full C,12-bin) | detected <0.01? |
|---|---|---|---|---|
| DESI | nosys | 0.000 (glob 41.7) | **0.000** (glob 32.2) | **YES — survives** |
| DESI | sys   | 0.000 (glob 44.4) | **0.000** (glob 31.2) | **YES — survives** |
| BOSS | nosys | 0.0067 (glob 18.1) | **0.310** (glob 7.5) | **NO — deflates** |
| BOSS | sys   | 0.000 (glob 24.2) | **0.123** (glob 8.7) | **NO — deflates** |

DESI driver shells (nosys) STRENGTHEN under full C (correlated noise makes the
coherent LRG bump more significant): LRG_1.00_1.05 Δχ² 13.6→**32.2**;
LRG_0.95_1.00 6.6→15.7; LRG_0.90_0.95 7.8→13.2 (all local p→0.000).
BOSS strong shell washes out: CMASS_0.53_0.58 local p 0.013→**0.123**.
**BOSS deflation decomposition (verifier amendment, TWO causes):** at MATCHED
12 bins the BOSS global p under DIAGONAL weighting is already **0.107/0.037**
(nosys/sys) — above the 0.01 bar before the full C enters. The deflation is
therefore SUBSTANTIALLY the frozen 40→12 rebinning (a narrow feature diluted by
coarse bins; scan widths sub-bin at 12 bins), with the full covariance deflating
further (0.107→0.31, 0.037→0.12). **Both causes — binning + covariance — travel
with every citation of the BOSS deflation.**

### (b) THE TRACER SPLIT — LRG_1.00_1.05 vs QSO_0.95_1.10 at zc≈1.02 (headline)
| variant | mode | θ_LRG (deg) | θ_QSO (deg) | **split significance** |
|---|---|---|---|---|
| nosys | diag (12-bin) | 2.348 ± 0.218 | 1.347 ± 0.127 | 3.97 σ |
| nosys | **full C**     | 2.348 ± 0.199 | 1.424 ± 0.137 | **3.83 σ** |
| sys   | diag (12-bin) | 2.348 ± 0.194 | 1.450 ± 0.127 | 3.87 σ |
| sys   | **full C**     | 2.348 ± 0.155 | 1.450 ± 0.126 | **4.51 σ** |

(M3 original 40-bin diagonal reference: θ_LRG = 2.44, θ_QSO = 1.39.)
**The split SURVIVES proper covariance** — 3.8–4.5 σ, essentially unchanged from
the diagonal ~3.9 σ. Two tracers genuinely disagree in θ_BAO at one redshift; this
is NOT a covariance/S-N artifact. The C2 caveat is NOT vindicated for the split.

### (c) THREADING — single ruler ℓ=58.34 on DESI PRIMARY SKY-ROBUST set (full-C center errors)
PRIMARY = {LRG_0.70_0.75, LRG_1.00_1.05, QSO_0.95_1.10}. Center errors from the
full-C Δχ²=1 profile (Percival-corrected).
| variant | χ²(ℓ=58.34 fixed)/3 | best-fit ℓ | χ²/dof | (M3b diag 40-bin) |
|---|---|---|---|---|
| sys   | 27.1/3 | 53.04 | 22.5/2 = **11.2** | 288.4/2 = 144.2 |
| nosys | 23.7/3 | 51.67 | 17.9/2 = **9.0**  | 276.2/2 = 138.1 |

A single ruler STILL fails to thread (χ²/dof ≈ 9–11, p ~ 1e-5), BUT the
catastrophic **144 was largely an error-underestimate artifact** of the M3b
σ_c = σ_b/√Δχ² center-error heuristic under diagonal errors. Under proper
covariance the tension shrinks ~13×; the residual failure is driven by the REAL
tracer split (§3b), which mathematically forbids two θ at one z. Magnitudes remain
~50–58 Mpc scale.
BOSS "within frozen-ℓ" test with full-C center errors: **6/9** shells consistent
(vs M3b 0/9), but this is driven by the enlarged proper error bars, not a
detection (BOSS feature deflates, §3a) — weak consistency, honestly flagged.

## 4. STEP 4 — RR shot-noise / IC (resolved by inspection; recount skipped, DISCLOSED)
Anti-hang: a full-random undownsampled recount of a representative shell was NOT
run (heavy; budget/anti-hang). It is resolved by inspection instead:
- **RR shot noise is negligible.** Banked RR pair counts are 1e7–1e10 per bin,
  2–4 orders above DD (1e5–1e7) — RR variance sits far below the jackknife
  variance the covariance is built from. The covariance core is not RR-limited.
- **Integral constraint** is an ~constant additive offset in w(θ), absorbed by the
  free cubic null baseline of the bump search → negligible effect on the localized
  feature. Both are honest arguments, not measurements; a native recount remains
  an OWED confirmation if Charles wants belt-and-suspenders.

## 5. STEP 5 — LANDING: **M3c-MIXED**
- **DESI angular feature — SURVIVES** (global p = 0.000 both variants; driver
  shells strengthen under full C).
- **Same-z tracer split — SURVIVES** (3.8–4.5 σ; the load-bearing C2 re-test holds).
- **BOSS detection — DEFLATES** (global p 0.31/0.12; no longer passes the frozen
  0.01 bar it met in M3b under diagonal 40-bin errors). TWO causes, both named:
  the frozen 40→12 rebinning (diag-at-12-bins already 0.107/0.037) + the full
  covariance (→0.31/0.12).
- **Single-ruler threading — still fails**, but the 144 tension figure was
  covariance-inflated; true χ²/dof ≈ 9–11, residual failure = the real split.

### Point-of-use downgrades OWED (held for Charles; M3/M3b NOT edited here)
1. **M3b BOSS "feature_detected = True"** (global p 0.0067/0.0) → at the frozen
   matched-rigor 12-bin binning NOT detected at the 0.01 bar (diag already
   0.107/0.037; full C 0.31/0.12). The BOSS replication/"feature" claim needs
   downgrade to "does not survive the matched-rigor re-test — **both** the 40→12
   rebinning **and** the full covariance contribute." (The BOSS `M3b-PARTIAL`
   landing weakens toward `M3b-NULL`.)
2. **M3b threading χ²/dof = 144.2** should not be cited as the tension magnitude —
   it is error-underestimate-inflated; proper value ≈ 9–11/dof (still failing).
3. **DESI detection + tracer split** — NO downgrade (survive / strengthen).

## 6. Premises / caveats (all travel)
- Covariance = RR-weighted linear rebin of the banked 48-region JK cov to 12 bins;
  exact at the covariance level, coarse-estimator definitional choice disclosed (§2).
- N_reg = 48 (cap-combine), N_bins = 12, Hartlap 0.7234, Percival m 0.9735.
- Inherits M3/M3b: cap-combine LS, split-averaged RR (DESI 4-file / BOSS 1-file),
  WEIGHT_SYS with/without both run, no reconstruction, no fiducial-cosmology columns.
- Bootstrap arm (via recount) + native full-random recount = OWED gaps, disclosed,
  not silently skipped (bootstrap adjudicated non-load-bearing, §2).
- **LRG–QSO cross-covariance unavailable:** the split σ (§3b) assumes the two
  tracers' θ_b errors are INDEPENDENT; they sample the same sky, so a positive
  cross-covariance would reduce (or negative increase) the split significance.
  Not constructible from the banked per-survey covariances. Travels on the split.
- **Hartlap-on-JK caveat:** the Hartlap factor is derived for independent-sample
  covariances; applied to a jackknife it is an approximation (standard practice,
  mild at N_reg=48 ≫ N_bins=12). Travels on all full-C significances.
- SNe M_B anchor conditions the absolute-Mpc ℓ; ℓ/R_w is anchor-free (unchanged).
- **Verified LEAD — blind verifier SUSTAINED-AMENDED (see CONSOLIDATED below);
  HOLD for Charles.**

Files: `build_cov.py`, `rerun_m3c.py`, `cov_out/*.npz` (122 covariances),
`cov_build_summary.json`, `m3c_refit_results.json`, `run_output.txt`,
`RESULTS_VERIFIER_REPORT.md`, `verify_m3c.py`.

---

## 7. CONSOLIDATED (post-verifier, amendments applied)

**Verifier verdict: SUSTAINED-AMENDED** (blind results-verifier,
`RESULTS_VERIFIER_REPORT.md` + `verify_m3c.py`, 2026-08-08, same-session).
Strengthenings the verifier ADDED: (i) the rebin identity C12 = A·C40·Aᵀ ↔
12-bin jackknife-of-rebinned-vectors **independently proven exactly**; (ii) all
refits and split sigmas **reproduce exactly** via an independent GLS route;
(iii) the BOSS deflation is **seed-stable at 600 mocks**; (iv) F-STEER
neutrality clean, no mock/fiducial leak. Three wording amendments required and
now applied in place: §3a two-cause BOSS decomposition; §2 bootstrap-arm
premise correction; §6 cross-covariance + Hartlap-on-JK caveats.

**Landing restated: M3c-MIXED.**
- DESI angular feature SURVIVES (global p = 0.000 both variants; drivers strengthen).
- The same-z tracer split SURVIVES (3.8–4.5 σ under full C; the C2 load-bearing
  re-test holds — conditional on tracer-independence, §6).
- BOSS detection DEFLATES — **two causes, both named:** the frozen 40→12
  rebinning (diagonal-at-12-bins already p = 0.107/0.037, above the bar) AND the
  full covariance (further to 0.31/0.12).
- Single-ruler threading still fails (χ²/dof ≈ 9–11) but the M3b 144 figure was
  error-underestimate-inflated.

**Owed point-of-use downgrades — VERBATIM, HELD FOR CHARLES (M3/M3b UNEDITED):**
1. **M3b BOSS "feature_detected = True"** (global p 0.0067/0.0) → at the frozen
   matched-rigor 12-bin binning NOT detected at the 0.01 bar (diag already
   0.107/0.037; full C 0.31/0.12). The BOSS replication/"feature" claim needs
   downgrade to "does not survive the matched-rigor re-test — **both** the 40→12
   rebinning **and** the full covariance contribute." (The BOSS `M3b-PARTIAL`
   landing weakens toward `M3b-NULL`.)
2. **M3b threading χ²/dof = 144.2** should not be cited as the tension magnitude —
   it is error-underestimate-inflated; proper value ≈ 9–11/dof (still failing).
3. **DESI detection + tracer split** — NO downgrade (survive / strengthen).

**Four-check line:** pre-registered (4bcd9e09, frozen before ruler effect seen);
bounded (banked-counts route, zero recount; skips disclosed §2/§4);
blind-verified on the load-bearing premise (rebin identity + refit reproduction,
SUSTAINED-AMENDED); forced premises audited (§6 all travel).

**Status: verified LEAD** (same-session verifier; the external bar — independent
replication under native full-resolution covariance — travels with the result).

**OWED (post-hold work, not blocking):** bootstrap covariance arm via a
region-blocked recount; full-randoms (undownsampled) recount + integral-constraint
measurement; PIP bitweights (prereg adopt-if-feasible, deferred).

**HOLD for Charles — nothing banks or amends M3/M3b until his review.**
