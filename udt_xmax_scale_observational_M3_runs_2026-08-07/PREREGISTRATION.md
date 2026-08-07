# M3 PREREGISTRATION — the real-data runs (V-SNe + V-BAO), frozen before unblinding

Date 2026-08-07 | branch grok | parent MAP: `udt_xmax_scale_observational_MAP_2026-08-07.md`.
**FROZEN CONTRACT — committed BEFORE any real-data fit.** Charles's rulings (2026-08-07): "Go
with your recommendations and go on M3" = the proposed M3 shape ratified: FOUR random files with
split-averaged RR; CPU tree workhorse; GPU spot-check subset; look-elsewhere wired; radial leg
attempt-only; **cap-combine ON with per-tracer shell floor** (the southern ELG/QSO shells
participate). Prior standing rulings travel (ontology rule; CP2/CP4/CP5; no-pin; quarantined
hypotheses).

## 1. What M3 produces (and the only words allowed)

Profile-conditional, measure-tagged RANGES with conditions attached — never "the value of
x_max," never "UDT confirmed/refuted" (F-SCOPE). A null BAO result ("no significant feature at
DR1 thin-shell depth") is a FIRST-CLASS outcome. All results are LEADS until the blind results
verifier passes and Charles rules; external-review bar travels.

## 2. Order of operations (frozen)

1. M3-PREP build additions (§5) + their synthetic gates — no real data.
2. **V-SNe runs** (all modes) — results file written and committed BEFORE any BAO unblinding.
   No SNe choice may be revisited after BAO results exist.
3. **V-BAO run** — per-shell checkpointed background process; then the assembly/analysis.
4. Blind results-verifier pass over both legs; consolidation; Charles.

## 3. V-SNe frozen run spec (data: Pantheon+ on disk; machinery as M2-gated)

- Cuts/columns exactly as the M2 freeze: z > 0.023 on the mode's z column; calibrators excluded
  from shape fits; full STAT+SYS covariance (modes A/B/D).
- Modes run: A (m_b_corr + cov, shape-only, free offset); B (anchored); C (own-Tripp raw-er,
  free alpha/beta, diagonal errors); D (z-column sensitivity: zCMB primary / zHD / zHEL).
- **Anchor frozen (mode B):** M_B = −19.253 ± 0.027 mag (SH0ES local-ladder calibration;
  EXTERNAL-ANCHOR premise: geometric anchors + Cepheid ladder, largely LCDM-independent but its
  own premise chain — travels with every absolute number; F-ANCHOR). The ±0.027 is propagated
  into every absolute interval.
- Reporting per profile (P1/P2/P3) per mode: best-fit (X_eff, shape), Δchi²=1 profile-likelihood
  intervals, chi²/dof; the D1 degeneracy handling as built (one-sided open shape intervals
  reported as such). Whole menu reported including poor fits (F-SHOP).
- **The two headline sensitivity numbers (frozen as deliverables):** |Mode C − Mode A| best-fit
  shift = the quantified BBC-contamination estimate (also the point-of-use note owed on the
  banked 0.91); Mode D shifts = the flow-correction sensitivity.
- Mode-B absolute output: R_w (resp. X) per profile with anchor premise attached; translations
  to O2's measure rows (proper 2R_w/(2−n), optical R_w/(1−n) where finite) labeled per row;
  O3 branch overlays (e.g. "IF spatial=optical THEN n<1 cuts to ...") as REPORTING LABELS only
  (no-pin standing). M_total translation deferred to M4.

## 4. V-BAO frozen run spec (data: on-disk DESI DR1 pre-recon; machinery as M2-gated + §5)

- Shells/bins/weights exactly as the M2 freeze; **cap-combine ON** (NGC+SGC pair counts summed
  per (tracer, shell) before LS; per-tracer ≥5·10⁴ weighted-galaxy floor; union-region
  jackknife, gated per §5.3). WEIGHT_SYS with/without variant both run.
- **Randoms (frozen estimator convention):** all FOUR random files. DR uses the concatenated
  4-file randoms; RR = the MEAN of the four per-file RR counts (no cross-file random pairs) —
  the standard split-randoms convention, adopted openly here for linear cost (~13 CPU-hr).
  Its unbiasedness is gated synthetically in §5.2 before use.
- Backend: CPU tree workhorse; **GPU spot-check (frozen):** 3 designated shells (LRG NGC
  0.60–0.65, BGS NGC 0.21–0.26, QSO NGC 1.10–1.25) get DD/DR recomputed on the GPU backend;
  bin-identical agreement required (the M2 equivalence bound); disagreement = STOP, diagnose.
- Bump machinery as frozen at M2 (cubic-in-ln θ null + Gaussian bump; full-window search, no
  LCDM seeding; 300 null-mock calibration per shell).
- **Look-elsewhere (frozen method):** per-shell LOCAL p from the shell's null-mock max-Δchi²
  distribution; GLOBAL trials-corrected p = P(max over all kept shells of per-shell max-Δchi² ≥
  observed max) under the joint null mocks; the JOINT UDT shape fit (one ell + profile params
  tying all shell centers via θ_b(z) = ell/r(z)) gets its own Δchi² significance calibrated on
  the same null ensemble. All three reported; the word "feature detected" requires global
  trials-corrected p < 0.01 (frozen threshold); below that, per-shell curiosities are reported
  as curiosities. Diagonal-jackknife-covariance caveat attached to every significance (M2
  verifier's condition).
- **Radial leg (attempt-only, frozen criterion):** attempted only in shells whose transverse
  local Δchi² exceeds the 95th null percentile; absence of any such shell retires the radial
  leg for DR1 with the honest note.
- Shape/scale reporting: joint-fit (ell/X_eff) with intervals per profile (shape test, ell
  free); with mode-B's anchor, bounds on R_w/X and ell in physical units (labeled; F-ANCHOR).
  Consistency/tension between SNe-preferred and BAO-preferred profile parameters reported as
  observed, both directions, no reconciliation attempts at M3 (F-STEER).

## 5. M3-PREP build additions (owed BEFORE runs; each synthetically gated; no real data)

1. **Split-averaged RR** implementation; gate: on synthetic catalogs, split-RR(4 files) vs
   full-RR agree within the jackknife noise (bias ≪ statistical error), and LS results
   consistent.
2. **Look-elsewhere module** (per-shell local p; global max-statistic calibration; joint-fit
   significance); gate: false-positive rate at the frozen thresholds on null ensembles; an
   injected multi-shell feature recovers the correct global significance ordering.
3. **Combined-mode jackknife gate** (the M2 verifier's owed item): union-region jackknife
   validated against empirical scatter on synthetic combined-cap mocks (the M2 JK-gate band).
4. **Runners** m3_run_sne.py / m3_run_bao.py: M2_GUARD flip via an explicit M3_AUTHORIZED flag
   citing THIS prereg's commit hash; per-shell checkpointing (staged banking — partial work
   survives); the CPU/GPU spot-check hook; modest CPU-only shell parallelism permitted
   (Category-A conditioning, workers bounded, documented).

## 6. Falsifiers (frozen; primary first)

- **F-IMPORT-LCDM:** as wired (blacklist; no LCDM seeding; no r_d/fiducial/template anywhere).
- **F-SHOP:** everything above is frozen; no post-hoc binning/threshold/menu/cut changes; all
  menu members and all shells reported including nulls and failures.
- **F-STEER:** the owner hypotheses stay quarantined; no reconciliation massaging between legs;
  a null BAO feature or an SNe-BAO tension is reported at equal temperature to a success.
- **F-ANCHOR:** every absolute number visibly carries the M_B premise (and its ±).
- **F-SCOPE:** ranges-with-conditions only; no "the" x_max; no M_total number until M4.
- **F-PEEK is RETIRED at M3** by this prereg (that was its design); the guard flip is legal
  only through the §5.4 mechanism.

## 7. Outcome classes (frozen)

- **M3-RANGES:** fits complete; the X-range table (per profile, per probe, per anchor status)
  delivered — with or without a BAO feature (SNe ranges stand alone if BAO is null).
- **M3-NULL(BAO):** no feature at the frozen threshold — first-class; reported with the
  thin-shell S/N context named at M1.
- **M3-OBSTRUCTED(component/reason):** a leg fails structurally (e.g. jackknife gate fails on
  combined mode); the obstruction is the deliverable for that leg.

## 8. Verification (owed before banking)

Blind results-verifier pass: re-runs the SNe fits from the committed code + data; spot-recomputes
≥2 BAO shells end-to-end (one per backend); audits every reported number against generating
code; checks falsifier discharge; hunts steering in the write-up. Then consolidation + Charles.
Verified-LEAD ceiling stands (same-session verification; external bar travels).
