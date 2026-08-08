# M3b PREREGISTRATION — the freeze + the BOSS out-of-sample test — FROZEN

Date 2026-08-08 | branch grok | Charles's ruling: "write the freeze that way, do the
intermediate work then open BOSS" (2026-08-08). This is THE FREEZE-POINT. It crosses the
CP4a hard no-BOSS-contact line — deliberately, AFTER the freeze commits. Committed before any
BOSS data is touched.

## 0. The structure (Charles's refined design)

DESI (already seen) MEASURES the ruler ℓ; SNe MEASURES the wall R_w; both FREEZE; then BOSS
(virgin, decorrelated) TESTS whether the same frozen ℓ threads it. The data SETS the scale (a
measurement, not a derivation — D3 stands: no native amount); the TEST is whether ONE geometry
+ ONE ℓ threads independent data. Parallel to ΛCDM calibrating its sound horizon and testing
the shape — the contest is consilience, never the scale value.

## 1. Phase 2 — the in-sample measurement (owed BEFORE BOSS; uses ONLY banked DESI + SNe)

- **r(z) frozen from SNe (banked M3 verified lead):** P1, R_w = n·X_eff, n = 1/inv_n with
  inv_n = 0.947 [0.9284, 0.9658], X_eff = 2086.0 [2059.1, 2113.2] Mpc (mode B anchored;
  anchor premise M_B = −19.253 ± 0.027 travels — F-ANCHOR). r(z) = R_w[1 − (1+z)^(−2/n)].
- **ℓ measured from the DESI SKY-ROBUST thread ONLY** (audit-mandated exclusion of the
  SELECTION-SUSPECT shells): PRIMARY set = the 3 SKY-ROBUST graded shells (LRG 0.70–0.75,
  LRG 1.00–1.05 control, QSO 0.95–1.10); VARIANT set = + the 2 INCONCLUSIVE (LRG 0.90–0.95,
  QSO 1.10–1.25); EXCLUDED = the 3 SELECTION-SUSPECT (LRG 0.95–1.00, LRG 1.05–1.10,
  QSO 1.85–2.00) + the B6 fitter artifact (LRG 0.75–0.80). Both weight variants (sys/nosys).
- **Fit:** θ_b(z_shell) vs ℓ/r(z_shell); minimize χ² weighted by the banked per-shell bump-
  center jackknife errors; report ℓ (PRIMARY), its interval, χ²/dof = **the threading quality
  = the certified drift tension quantified** (honest: the audit found the thread drifts
  OPPOSITE the ℓ/r(z) fall — a single ℓ is expected to thread the MAGNITUDE ~70 Mpc but not
  the DIRECTION; the fit REPORTS this, does not hide it), and **ℓ/R_w** = the dimensionless
  target the discreteness program would have to predict (the D3 output).
- IN-SAMPLE, disclosed as such. NO fit to BOSS. This closes the freeze.

## 2. The frozen prediction (committed at end of Phase 2, BEFORE BOSS contact)

The PRIMARY ℓ + UDT r(z) predicts θ_BAO(z) at BOSS DR12's redshift coverage (LOWZ z≈0.15–0.43,
CMASS z≈0.43–0.70). A predicted-θ table per intended BOSS shell, frozen. Plus the matrix's
per-origin BOSS predictions (from the closed D0 matrix): **O-D** (mundane) → NO feature in BOSS
(decorrelated systematics; the cheapest kill); **O-A/O-C/O-E** → a feature threading the frozen
ℓ, tracer-universal (BOSS galaxies share DESI's ℓ), with O-A's drift behavior; a feature at a
DIFFERENT ℓ → ℓ NOT universal (frame-map/viewing-artifact strain). All frozen.

## 3. Phase 3 — the BOSS out-of-sample test (after the freeze commit)

- **Data (M1-graded clean; acquire to scratch disk):** BOSS DR12 LSS catalogs, PRE-
  reconstruction (galaxy_DR12v5_LOWZ + CMASS, North+South, + randoms). Public SDSS SAS.
  Column policy = the SAME blacklist as V-BAO (RA/DEC/Z + completeness/systot/fkp-as-COMP-only
  weights allowed; any fiducial-cosmology/NBAR/comoving column FORBIDDEN — F-IMPORT-LCDM; the
  loader's blacklist extended to BOSS column names, machine-tested; NO reconstruction files).
- **Pipeline = the frozen M3 machinery UNCHANGED:** thin z-shells (Δz matched to BOSS density),
  cap-combined, split-averaged RR, Landy–Szalay w(θ), the frozen bump search (full-window, no
  seeding), 300-null look-elsewhere, GPU spot-check under the amended-v2 criterion. No
  re-tuning of any frozen choice (F-RETRO / F-SHOP).
- **Frozen pass/fail (committed now):**
  - **REPLICATION + SCALE-CONSISTENT (strong PASS):** a feature detected (global trials-corr
    p < 0.01) AND the frozen ℓ predicts the BOSS θ_BAO within jackknife errors across ≥ 2 BOSS
    shells.
  - **REPLICATION + SCALE-INCONSISTENT (PARTIAL):** feature detected but at ℓ' ≠ frozen ℓ
    (beyond errors) → ℓ not universal; report the tension neutrally.
  - **NULL (first-class):** no feature at threshold → O-D lives / BOSS thin-shell S/N context
    named; the DESI thread stands alone.
  - The drift-direction: whether BOSS reproduces DESI's opposite-drift tension → reported
    either way, equal temperature.

## 4. Falsifiers (frozen)

F-RETRO (primary): ℓ + r(z) + all criteria frozen and git-committed BEFORE BOSS contact
(the commit hash is the timestamp); NO re-tuning after BOSS is seen. F-IMPORT-LCDM: BOSS
pre-recon only; blacklist extended + machine-tested; no fiducial/NBAR/comoving/reconstruction.
F-STEER: NULL and PARTIAL reported at equal temperature to PASS; no massaging toward the owner
ontology. F-SHOP: pipeline frozen from M3; BOSS shell binning declared here (Δz per cap by
density, floor 5e4 weighted) — no post-hoc changes. F-ANCHOR / F-SCOPE: as standing. Hard
line: ZERO BOSS file contact — not even listing — until Phase 2's freeze is committed.

## 5. Outcomes

M3b-PASS / M3b-PARTIAL / M3b-NULL / M3b-OBSTRUCTED(acquisition or S/N). Blind results-verifier
owed before banking (re-run the frozen fit; recompute ≥1 BOSS shell; audit F-RETRO timeline
against git). Verified-LEAD ceiling (same-session; external bar travels).

## 6. Process

Phase 2 (in-sample ℓ) = one agent, bounded, banked-data only → commit freeze. Phase 3 (BOSS) =
acquire (bounded; ~few GB) → run frozen pipeline (checkpointed, GPU spot-check) → commit
results. Phase 4 = blind verifier → consolidate → Charles. Anti-hang + chunked-output rules
throughout; NO monitors (synchronous foreground bounded runs).
