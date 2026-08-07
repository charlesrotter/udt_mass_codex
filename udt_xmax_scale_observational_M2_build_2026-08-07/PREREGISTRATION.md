# M2 PREREGISTRATION — the validator BUILD (V-SNe + V-BAO), frozen before anything runs

Date 2026-08-07 | branch grok | parent: `udt_xmax_scale_observational_MAP_2026-08-07.md` (M2 on
Charles's go, 2026-08-07). **FROZEN CONTRACT — committed before any build/fit.** M2 BUILDS and
VALIDATES-ON-SYNTHETIC only; **NO real-data verdicts at M2** (that is M3, separately gated).
Real-data contact at M2 is limited to schema/row-count/column verification and single-shell
I/O feasibility smoke tests that produce NO science numbers.

## 0. Standing rulings this build rides on

- CP1 ("cleaner and slower"): the profile menu comes from the structure lane (O2/O3, now complete
  as verified leads) — frozen in §2 below, no ad hoc members (F-SHOP).
- CP2 (validator/origin split): origin-agnostic by construction; ell is a free nuisance.
- CP4: the candle absolute calibration is the accepted external anchor (premise travels — F-ANCHOR).
- CP5 (+amendment): DESI DR1 on disk; 500 GiB scratch budget if needed (M2 expects ~0 new GiB).
- Ontology rule (binding): BAO = raw observations; zero LCDM imports (F-IMPORT-LCDM primary).
- CP2-pair-lane NO-PIN standing: fits are measure-UNCONDITIONAL; branch-conditional overlays are
  reporting labels only (§5).
- Owner hypotheses X-BAO-ORIGIN / X-CMB-ANISO: quarantined; nothing in this build may depend on
  or encode them (F-STEER).

## 1. What M2 delivers (and what it may not)

- **D1 — native prediction formulas** for each menu profile, derived from the lock realization
  (ds² = −A c²dt² + dr²/A + r²dΩ² under the areal anchor; 1+z = A^{−1/2}; observer normalization
  φ(0)=0 ⇒ A(0)=1 — THEORY tags carried), machine-checked in sympy against the banked O2/O3
  results (e.g. n=1 must reproduce d_L = X·z(z+2) exactly).
- **D2 — V-SNe**: a fresh, small fitter (no archived-code resurrection; F-LEGACY) implementing
  the frozen modes of §3, validated by INJECTION-RECOVERY on synthetic data (known profile +
  noise drawn from the real covariance ⇒ recover the truth within stated tolerance).
- **D3 — V-BAO**: the observable-space matcher of §4, validated by INJECTION-RECOVERY on
  synthetic w(θ) (known bump ⇒ recovered center/width/significance) and by an end-to-end mock
  (synthetic catalog with an injected angular feature ⇒ recovered θ_BAO(z)).
- **D4 — the purity harness**: machine tests wiring the falsifiers (forbidden-column blacklist;
  menu freeze check; no-real-data-verdict guard at M2).
- **MAY NOT:** produce any X value, any real-data chi², any real-data bump significance, or any
  statement about which profile the data prefer. Any such number appearing in M2 outputs =
  **F-PEEK fires** (new falsifier, this step: real-data verdicts before the preregistered M3 run).

## 2. The frozen profile menu (from O2/O3 — F-SHOP; c₀ = 1 by observer normalization, THEORY)

- **P1 (class i):** A = (1 − r/R_w)ⁿ, n > 0 free. r(z) = R_w[1 − (1+z)^(−2/n)];
  d_L(z) = (1+z)² r(z). n=1 (the L member) is one point of the family, not privileged; its
  banked d_L/X = z(z+2) is the machine cross-check.
- **P2 (class ii):** A = e^(−r/X). r(z) = 2X ln(1+z); d_L = (1+z)²·2X ln(1+z).
- **P3 (class ii′):** A = (1 + r/X)^(−α), α > 0 free (the O3-declared regular representative).
  r(z) = X[(1+z)^(2/α) − 1]; d_L = (1+z)² r(z).
- Class (iii) log-corrections: NOT independently fitted — stated reason (completeness, not
  convenience): at SNe/BAO precision the extra log parameter is degenerate with n over the data's
  z range; (iii) enters only as the banked caveat that class-(i) edge verdicts are not
  class-stable. Any future promotion to the fit menu is a new prereg.
- All prediction formulas are exact under the lock + areal anchor (chart tags travel). The scale
  parameter fitted is R_w (resp. X) = the wall's AREAL radius — measure-tagged; translations to
  other rows use O2's exact table (e.g. proper x_max = 2R_w/(2−n) for n<2) and are labeled
  per-measure at reporting.

## 3. V-SNe frozen design

- **Data:** `Data/Pantheon+SH0ES.dat` (1701 rows) + `Data/Pantheon+SH0ES_STAT+SYS.cov`.
  Build-time verification of M1's load-bearing column claims (zHD flow-corrected; m_b_corr
  BBC-bias-corrected; raw zCMB/zHEL/mB/x1/c present) against the shipped README/column docs —
  the M1 single-agent spot-verify owed at M2.
- **Cuts (frozen):** z > 0.023 in the fit redshift (peculiar-velocity floor; CHOSE-convention,
  tagged); SH0ES calibrator rows excluded from shape fits (used only by the anchored mode per
  its own premise); duplicate-SN structure handled per the covariance's row convention.
- **Modes (all built; all reported at M3; none privileged):**
  - **A (primary shape):** m_b_corr + full STAT+SYS covariance; free global offset (shape-only,
    anchor-free). Contamination caveat carried: m_b_corr's BBC layer is LCDM-adjacent (M1 catch).
  - **B (anchored):** mode A + the external M_B calibration ⇒ absolute R_w/X (F-ANCHOR: the
    anchor premise chain travels with every absolute number).
  - **C (raw-er standardization):** own Tripp standardization m = mB + α·x1 − β·c with α, β free
    nuisances, diagonal errors (the official covariance does not apply to this vector — stated),
    NO BBC bias correction. |Mode C − Mode A| best-fit shift = the QUANTIFIED contamination
    estimate for the BBC layer (the M1 catch turned into a number). Also supplies the
    point-of-use note owed on the banked 0.91.
  - **D (redshift sensitivity):** zCMB (primary; kinematic frame convention, tagged) vs zHD
    (flow-model corrected) vs zHEL — same fit, column swapped; shifts reported.
- **Statistic:** Gaussian chi² with the mode's covariance; profile-likelihood intervals
  (Δchi² = 1 for 1-parameter, stated per mode); per-profile reporting of best fit + interval +
  chi²/dof for the WHOLE menu including failures (F-SHOP/F-SCOPE).
- **Synthetic validation gate (M2's pass bar):** inject each menu profile at 3 (R_w, shape)
  truth points into mock data with noise drawn from the real covariance; the fitter must recover
  truth within its own stated intervals in ≥ the nominal coverage sense (spot coverage check),
  and mode C must recover injected α, β.

## 4. V-BAO frozen design (observable space; zero LCDM)

- **Data:** on-disk DESI DR1 pre-recon LSS catalogs (BGS_BRIGHT, LRG, ELG_LOPnotqso, QSO;
  NGC+SGC; dat + randoms). READ-ONLY; no modification/move.
- **Column policy (F-IMPORT-LCDM wired as code):** allowed = RA/DEC/Z, WEIGHT_COMP, WEIGHT_ZFAIL,
  WEIGHT_SYS (with/without variant per M1's over-correction caveat), randoms' Z. **Blacklisted =
  NX, WEIGHT_FKP, anything `_rec`** — a machine test asserts the loader cannot return blacklisted
  columns; weighting uses native completeness weights only (any radial weighting needed is built
  from the catalogs' own dN/dz, never NX).
- **Shells (frozen):** thin redshift shells of width Δz = 0.05 (BGS/LRG/ELG) and Δz = 0.15 (QSO)
  over each tracer's M1-reported range; a shell enters only if it holds ≥ 5·10⁴ weighted
  galaxies (S/N floor, frozen; dropped shells reported — no silent caps).
- **Estimator:** Landy–Szalay w(θ) per shell, per cap, native weights; θ ∈ [0.3°, 12°] in 40
  log-spaced bins (frozen); pair counts via exact tree/grid code on CPU (bounded; per-shell,
  never all-sky at once).
- **Feature detection (model-free; frozen):** null = cubic polynomial in ln θ; alternative =
  null + Gaussian bump (center θ_b, width σ_b, amplitude); Δchi² significance per shell with
  trials (look-elsewhere) accounted over the full θ search window and over shells — the search
  window is the FULL θ range (no LCDM-predicted center may seed or restrict the search).
- **UDT joint shape test (the M3 payload this build enables):** one native length ell (free
  nuisance, P-STATIC-RULER premise tagged) + a menu profile predict ALL shell centers at once via
  θ_BAO(z) = ell / r(z) (transverse proper length = r·θ under the areal anchor — geometry,
  native). Joint fit across shells ⇒ the shape test with ell free; with mode-B's anchor ⇒ bounds
  on R_w/X and incidentally ell in meters (labeled). **Radial leg** Δz_BAO(z): built as
  Δz = ell·(1+z)·dδ/dℓ_p evaluated per profile (exact form derived in D1) but flagged
  ATTEMPT-ONLY at M3 (M1's thin-shell S/N risk, honest).
- **Synthetic validation gate:** (a) bump injection into mock w(θ) with realistic noise ⇒
  recovered center within stated errors, significance calibrated on null mocks (false-positive
  rate at the stated threshold); (b) end-to-end: a synthetic RA/DEC/Z catalog with an injected
  angular-scale feature ⇒ pipeline recovers θ_BAO(z) across ≥ 2 shells.

## 5. Reporting rules (frozen now, for M3's sake)

Ranges are profile-conditional and measure-tagged: "R_w (areal) ∈ [..] under P1 at n ∈ [..]"
with O2-table translations per row, labeled. The O3 branch-conditional overlays (e.g. "IF the
kernel's spatial = optical THEN n < 1 cuts this range to ...") are REPORTING LABELS applied
after the unconditional fit — never fit constraints (no-pin standing). Every absolute number
carries the anchor premise (F-ANCHOR); no single "the value of x_max" (F-SCOPE); M_total
translation deferred to M4.

## 6. Falsifiers (frozen)

- **F-IMPORT-LCDM (primary):** any acoustic/r_d/comoving/fiducial/template/reconstruction/
  blacklisted-column leakage into code or formulas — machine-wired (D4) + review-audited.
- **F-PEEK (new, this step):** any real-data verdict number produced at M2 (fit results, bump
  significances, preferred profiles). Schema checks and I/O smoke tests are legal; numbers that
  could steer M3 are not.
- **F-SHOP:** the §2 menu and §3/§4 frozen choices (cuts, bins, thresholds, windows) are fixed
  here, pre-run; any change = new prereg. All menu members reported at M3 including failures.
- **F-STEER:** origin-agnostic construction; n=1 unprivileged in code paths and defaults; the
  two owner hypotheses appear nowhere in the build.
- **F-ANCHOR / F-SCOPE:** as in §5. **F-LEGACY:** no archived-code resurrection.

## 7. Outcomes (frozen)

- **M2-BUILT:** both validators pass their synthetic gates; purity harness green; ready for M3.
- **M2-PARTIAL(component):** one leg passes, the other obstructed — the passing leg may proceed
  to M3 alone (per-leg gating; honest partial beats a hang).
- **M2-OBSTRUCTED(component/reason):** e.g. the catalogs cannot support the estimator at any
  frozen shell choice; the obstruction is the deliverable.

## 8. Process (bounded; anti-hang + chunked-output rules)

One derivation agent (D1, exact sympy, small) → two build agents (D2, D3; CPU only, bounded
smoke tests, incremental file writes ≤120-line appends, final reports ≤50 lines) → one blind
adversarial verifier pass over the whole build (prereg conformance; purity; synthetic-gate
honesty — does the recovery test actually test what it claims; F-PEEK sweep of all outputs)
before M2 is recorded. M3 (real-data runs) is a SEPARATE gate on Charles's go.
