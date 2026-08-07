# V-SNe validator — D2 build notes (M2)

Date 2026-08-07 | D2 build agent | binding: PREREGISTRATION.md §1/§3/§6, D1_FORMULAS.md
("FOR THE BUILDERS" forms implemented exactly, incl. the (X_eff, 1/n)/(X_eff, 1/α)
sampling coordinates). NOT committed (per dispatch). Files: `v_sne.py` (fitter module),
`synth_sne.py` (injection-recovery gate), `test_v_sne.py` (pytest gate),
`v_sne_synth_results.txt` + `v_sne_test_output.txt` (captured outputs).

## 1. Column verification (the M1 spot-verify owed at M2) — ALL CLAIMS HOLD

Read from the actual `Data/Pantheon+SH0ES.dat` header (47 columns, 1701 data rows):

- PRESENT: `zHD/zHDERR`, `zCMB/zCMBERR`, `zHEL/zHELERR`, `m_b_corr`, `m_b_corr_err_DIAG`,
  `mB/mBERR`, `x1/x1ERR`, `c/cERR`, `IS_CALIBRATOR` (the calibrator flag; 77 rows = 1),
  plus SALT2 cross-covariances `COV_x1_c/COV_x1_x0/COV_c_x0` and bias-correction columns
  (`biasCor_m_b` etc.). No M1 claim failed.
- Duplicate-SN convention: 1701 rows, 1543 unique CIDs — duplicate observations of the
  same SN are SEPARATE ROWS (e.g. 2011fe under IDSURVEY 51 and 56); the covariance is
  row-ordered over all 1701, so rows are kept as-is and never collapsed.
- Cov file format VERIFIED: first line `1701`, then exactly 1701² = 2,893,401
  whitespace-separated values, row-major in the .dat row order. Symmetric to ~3e-8
  (text round-off; symmetrized on load). Cholesky succeeds ⇒ positive-definite.
- FLAG (recorded, not acted on): diag(STAT+SYS cov) ≠ `m_b_corr_err_DIAG`² (median rel.
  diff 28% even after the z>0.023 cut) — the DIAG column is a separate quick-look vector
  (incl. peculiar-velocity mapping); modes A/B/D use the shipped cov ONLY, never the
  DIAG column (it is not even whitelisted for A/B/D).
- After the frozen cuts (z_fit > 0.023, IS_CALIBRATOR == 0): N = 1367 rows on zCMB.

## 2. What was built (frozen choices restated)

- `v_sne.py`: loader with per-mode column WHITELIST (`MODE_COLUMNS`; `ModeData.col`
  refuses anything else — machine test); frozen cuts z > 0.023 on the mode's fit-z
  column [CHOSE-convention, prereg §3] + calibrator exclusion from all fit vectors
  (mode B anchors via the EXTERNAL M_B premise, not calibrator rows); cov subset by the
  same row mask. Menu P1/P2/P3 via D1's log1p/expm1-safe forms; sampling coordinates
  (X_eff, 1/n)/(X_eff, 1/α) [D1 §2 item 4, Category-A conditioning]; the n,α→∞ (P2)
  limit is the interior point inv→0.
- Statistic: Gaussian chi² with the full cov via Cholesky (`cho_factor`/`cho_solve`;
  never an explicit inverse); the additive offset B = 5log10(X_eff)+25+M_B is profiled
  ANALYTICALLY (X_eff enters magnitudes only through B ⇒ X_eff is STRUCTURALLY
  unidentified in anchor-free modes; stated in every mode-A output).
- Modes: **A** m_b_corr + full STAT+SYS cov + free offset (BBC/LCDM-adjacent caveat
  carried in the output premise string); **B** = A's chi² surface + external M_B input
  (premise tag emitted in the result header; interval translated monotonically,
  M_B_err in quadrature; P1's R_w = n·X_eff reported at-best-n only with the F-SCOPE
  pair-reporting note); **C** own Tripp m = mB + α·x1 − β·c, α/β free, DIAGONAL errors
  σ² = mBERR² + α²·x1ERR² + β²·cERR² (STATED; the official cov does not apply to this
  vector), no BBC; σ(α,β)-frozen fixed-point iteration (deterministic; converged in 2
  iterations on all gate mocks); **D** = A with the fit-z column swapped
  (zCMB primary / zHD / zHEL via `load_mode_data(zcol=…)`, mode-D-only by loader rule).
- Intervals: Δchi²=1 profile likelihood; deterministic outward bracketing + bisection;
  open ends flagged (one-sided posteriors toward the P2 limit expected, D1 §2).
- Optimization: scipy Nelder-Mead from FROZEN start grids only (no randomness);
  SHAPE_STARTS = (0.25, 0.75, 1.5, 3.0) — excludes n=1 and α=2 (F-STEER).
- **M2_GUARD = True** (module level): every fit function raises RuntimeError on any
  DataVector not tagged `synthetic` — real magnitudes CANNOT be fitted at M2. M3 flips
  it deliberately under its own prereg. `--synthetic`-only posture is thereby hard, not
  advisory; `DataVector.from_real` exists for M3 but is guard-blocked today.

## 3. Synthetic gate results (v_sne_synth_results.txt; deterministic, frozen seeds)

Truth points (frozen, stated in synth_sne.py; spread across the degeneracy range incl.
near-P2 boundary; none at n=1/α=2): P1 (2600,0.08)(2200,0.6)(1800,1.8);
P2 (1500)(2200)(3000); P3 (1800,0.12)(2200,0.7)(2600,1.6). Mock noise = Cholesky of the
REAL STAT+SYS cov on the REAL z distribution after cuts (N=1367). M_B_SYNTH = −19.0
(arbitrary frozen constant). Tripp truths α=0.14, β=3.0.

- **A-analog (+B translation): 9/9 rows PASS or PASS-3sig** (shape, offset B, and X_eff
  all recovered; chi²/ndof 0.94–1.05). **C-analog: 9/9 rows PASS or PASS-3sig**; α and β
  recovered in every row. **Coverage spot-check: 12/20** realizations cover the inv_n
  truth (expect ~13.6/20 for 68%; PASS window [9,19]). **GATE VERDICT: PASS.**
- Build catch (recorded): the first gate run FAILED (7/20 coverage) — the Δchi²=1
  crossing used linear interpolation over a possibly-far-overshooting first bracket
  step, collapsing intervals ~5× for a locally-quadratic chi². Fixed by bisection
  refinement (Category-A numeric fix; no physics change); gate then passed. This is the
  gate doing its job.
- **Degeneracy behavior — as D1 predicted**: (a) a P2-truth mock fitted with P1 or P3
  drives inv-shape to the bound with the LOW end OPEN (one-sided toward the P2 limit,
  D1 §2 item 2); (b) low-z-only (z<0.15) fits widen the shape interval ~5× (±0.095 vs
  ±0.017 full-z) at unchanged X_eff-combination precision (D1 §2 item 1); (c) X_eff ⊥
  offset exact degeneracy in anchor-free modes is structural (profiled analytically,
  reported in every result).

## 4. Purity statement

- **F-PEEK — every real-data quantity touched, and why each is legal (prereg §1/§6):**
  (1) the .dat header + row/CID/calibrator counts — schema verification (expressly
  legal); (2) the cov file's N, value count, symmetry, positive-definiteness — format
  verification; (3) the real redshift columns after cuts — the mock z distribution
  (dispatch-authorized); (4) the real STAT+SYS covariance and its Cholesky — synthetic
  noise (expressly legal); (5) the real mBERR/x1ERR/cERR columns — mode-C mock noise
  scales (uncertainty/covariance-class extraction); (6) diag(cov) vs err_DIAG
  comparison — schema sanity, no model involved. **Never touched by any fit or mock:**
  the real m_b_corr, mB, x1, c VALUES. No chi² against real magnitudes exists anywhere
  in M2 outputs; no best-fit on real data; no preferred-profile statement. The pytest
  gate proves the guard blocks the real path.
- **F-IMPORT-LCDM:** not applicable to the SNe leg except the carried m_b_corr BBC
  caveat (M1 catch) — emitted verbatim in every mode-A/B result; mode C exists to
  quantify it at M3 (|C−A| shift). No fiducial cosmology, template, or r_d enters.
- **F-STEER:** n=1 and α=2 appear in no default, start grid, or truth point; n=1 exists
  only as the banked machine cross-check d_L = R_w·z(z+2) (test passes to 1e-12).
- **F-SHOP:** menu, cuts, modes, starts, seeds, truth points, PASS rules all frozen
  in-file before the gate ran; the one post-run change (bisection) is interval-accuracy
  conditioning, disclosed above.
- **F-LEGACY:** all code fresh; no archived solver resurrected.
- **A2 applied (verifier amendment, 2026-08-07):** the "Degeneracy observations" section
  of `v_sne_synth_results.txt` now has in-package generating code —
  `synth_sne.py::run_degeneracy_obs` (frozen seeds 4100/4200, synthetic-only; run by
  `main()` and standalone via `--degeneracy-only`); regenerated output matched the
  results-file section EXACTLY (diff-clean), so no numbers were replaced. M2_GUARD and
  the F-PEEK posture untouched.

## 5. Status

V-SNe leg: **built + synthetic gate PASS** (M2-BUILT posture for this leg, pending the
blind verifier pass per prereg §8). Ready for M3 wiring: flip M2_GUARD under the M3
prereg, feed `DataVector.from_real`, report all modes/profiles incl. failures.
