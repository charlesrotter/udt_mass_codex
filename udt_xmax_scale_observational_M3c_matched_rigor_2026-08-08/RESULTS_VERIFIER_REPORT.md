# M3c BLIND RESULTS-VERIFIER REPORT

Agent: blind results-verifier (fresh context, no stake), 2026-08-08. Independent
recomputation script: scratchpad `verify_m3c.py` (own rebin operator; GLS chi2 via
whitened lstsq, NOT their projection-matrix route; own profile intervals; independent
600-mock seeds). NOT committed; HOLD for Charles stands.

## 1. Rebinning operator (load-bearing) — VERIFIED
- Identity derived independently: per delete-one JK sample k, w12_k = A w40_k with the
  SAME fixed A ⇒ dev12_k = A dev40_k ⇒ C12 = A C40 Aᵀ EXACTLY. Load-bearing condition:
  A must be one fixed operator across samples. Confirmed in `build_cov.py`: A is built
  once from TOTAL banked RR (not per-region RR) — the identity holds. (Stronger still:
  RR-weighted averaging of fine-bin LS w's with global norms IS algebraically the
  from-scratch coarse-bin LS on summed counts — the "definitional choice" is milder
  than disclosed.)
- Recomputed C12 with my own operator code for 5 shells (DESI driver LRG_1.00_1.05,
  QSO_0.95_1.10_sys, null BGS_0.01_0.06, BOSS CMASS_0.53_0.58, LOWZ_0.20_0.25):
  C12, w12, A all match to 0.0 (exact); PD everywhere; conds 254–4632 match summary;
  cinv_hartlap = 0.7234·inv(C12) confirmed.
- Rank census: all 122 banked cov_jk have rank 40 ⇒ T≥41 everywhere; T=48 confirmed
  from `ls_w_theta_capcombine` (2 caps × 24 regions, leave-one-out over the union).
  N_reg=48 for Hartlap/Percival is correct.
- BGS sys==nosys checkpoints byte-identical (M3-inherited, trivial WEIGHT_SYS for
  BGS); LRG differs — expected, not an M3c defect.

## 2. Refit machinery — VERIFIED (with one attribution finding)
- Independent GLS reproduces every checked number: LRG_1.00_1.05 dchi2 13.56→32.21
  (sys 14.51→31.18); CMASS_0.53_0.58 local p 0.123 under their seed, and 0.12–0.18
  under an INDEPENDENT 600-mock seed — the deflation is seed-stable, not seed luck.
  QSO_0.95_1.10 8.79/local p ~0.01–0.018 reproduces.
- Mock/data consistency: mocks drawn from the SAME C12 used in the fit, evaluated
  under the same W; dchi2 = nᵀ(B_alt−B_null)n is exactly baseline-independent, so
  zero-mean mocks are the correct null; Hartlap scaling cancels in p. Not rigged.
- **FINDING (attribution, owed disclosure):** my decomposition at matched 12 bins:
  BOSS global p under DIAG weighting = 0.107 (nosys) / 0.037 (sys) — ALREADY above
  the 0.01 bar before any off-diagonals enter. The 0.0067/0.000→0.31/0.12 deflation
  is therefore substantially the frozen 40→12 REBINNING (resolution loss on a
  narrow/marginal feature; narrowest scan widths 0.10–0.20 in ln-θ are sub-bin at
  12 bins), with full C deflating further (0.107→0.31, 0.037→0.123). The frozen
  12-bin route is prereg-legal and the downgrade wording "at 12 bins" is scoped, but
  §3(a)'s "correlated noise" framing over-attributes to covariance. AMEND: state the
  binning-vs-covariance decomposition. (Symmetrically: DESI survives at 12 bins under
  both weightings, so no analogous issue there.)

## 3. Tracer split — VERIFIED
- Independent profile code reproduces all four rows exactly: 3.97/3.83/3.87/4.51 σ.
  Δχ²=1 profile (width+amplitude+cubic profiled) is a correct generalized-chi2 center
  error; interval spans any multimodal below-threshold region (conservative); 200-pt
  grid is fine relative to σ_θ; Percival ×0.9867 and Hartlap-through-W both applied.
- Residual caveat (travels, not a failure): LRG–QSO CROSS-covariance is unavailable
  (per-region vectors not banked) — the split σ assumes independent tracers on the
  same sky. Same limitation as M3; direction unknown; worth one line in §6.

## 4. Neutrality (F-STEER/F-RETRO) — CLEAN, one wording nit
- Timeline: prereg commit 4bcd9e09 21:12:20; build_cov.py mtime 21:18:36; results
  21:22–21:24; prereg/methodology-map unmodified since commit. Clean order.
- Equal temperature honored: MIXED headline; BOSS deflation in §0, the table, the
  landing, and downgrade #1 — first-class, not buried.
- Bootstrap skip: prereg §1.1(b) reads "bootstrap ... AND/OR reduce N_bins" — either
  arm satisfies the frozen text; the bootstrap arm's premise (region-blocked counts
  banked) was factually false, so it was infeasible without a recount. ADJUDICATION:
  NOT load-bearing — C12 is an exact linear image of a genuine 48-sample JK (verified
  §1), PD, moderately conditioned; a bootstrap would test the JK estimator itself, a
  fair OWED robustness item but not required by the frozen spec and NOT cheap from
  the bank (impossible without per-region vectors). Keep OWED. Nit: M3C_RESULTS §2
  calls it "the prereg §1.1b cross-check" — the prereg listed it as an alternative,
  not a mandated cross-check; soften. One-line caveat also owed: Hartlap/Percival are
  derived for independent realizations; applying them to JK samples is standard but
  approximate.
- IC skip: EXACT no-op for the bump statistic (constant offset fully degenerate with
  the cubic's constant term) — stronger than the doc's "honest argument"; fine.
  Full-randoms skip: would only reduce RR noise already captured inside the JK C;
  disclosed; non-blocking.
- Threading recomputed independently: 27.1/3 fixed; best-fit 53.04 (22.5/2=11.2 sys),
  51.67 (17.9/2=9.0 nosys) — all reproduce; frozen constants match FROZEN_PREDICTION.md.

## 5. Owed downgrades — CORRECT AS SCOPED
(1) M3b feature→not-detected-under-full-C-at-12-bins: right, correctly held un-edited
for Charles — ADD the §2 binning decomposition so the downgrade names both causes.
(2) 144→9–11: right; verified; the M3b σ_c heuristic under-error is real.
(3) DESI no-downgrade: right (global p < 1/300 both variants; drivers strengthen).

## FINAL VERDICT: **SUSTAINED-AMENDED**
Construction sound; every checked number reproduces under independent code; neutrality
clean. Required amendments before Charles review (wording only, no rerun): (a) add the
binning-vs-covariance decomposition for the BOSS deflation (12-bin diag global p
0.107/0.037) to §3a and downgrade #1; (b) soften "prereg cross-check" for bootstrap;
(c) add the LRG–QSO cross-covariance caveat and the Hartlap-on-JK approximation note
to §6. The M3c-MIXED landing itself stands.
