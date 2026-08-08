# M3 V-BAO RESULTS — PROVISIONAL / LEAD (prereg 523f4aca; blind results-verifier owed)

Date 2026-08-08. 52 shells × 2 weight variants, cap-combined, 4-file split-RR, CPU tree +
passed GPU audit (amended-v2 criterion — verifier re-adjudication owed on the amendment).
Caveats on every number: diagonal jackknife covariance; nearest-bin center tie approximation;
look-elsewhere p-floor = 1/300 (reported 0.0 means < 0.0033).

## Headline 1 — the frozen detection criterion is MET (both weight variants)
Global trials-corrected max-statistic p < 1/300 vs the frozen threshold 0.01
(`feature_detected: true`, sys AND nosys). Per the frozen language rule the package may say:
**a coherent angular clustering feature exists in the DR1 catalogs beyond noise, after
accounting for the 52-shell search.**

## Headline 2 — the strong-shell cluster is NOT an imaging-weight artifact
The notable shells are stable between the with/without-WEIGHT_SYS variants to ~1% in position
and a few % in strength: LRG 0.70–0.75 (2.37°), 0.90–0.95 (2.34°), 1.00–1.05 (2.44°),
1.05–1.10 (1.17°), QSO 0.95–1.10 (1.39°), 1.10–1.25 (2.05°). The M1-flagged over-correction
hazard did not materialize for these cells. (BGS 0.01–0.06 broad 10.6° hit also
weight-stable — reads as local large-scale structure / selection breadth, not BAO-like.)

## Headline 3 — HONEST LIMIT: single-ruler parametrization is NOT robust at DR1 depth
The joint coherent-structure statistic is enormous for every profile (p < 1/300 all three;
existence again), but its PARAMETERS are variant-unstable despite near-identical per-shell
inputs: best (shape, s=ell/scale) = (1.008, 0.0309) [sys] vs (5.0-at-grid-edge, 0.0091)
[nosys]. Reading: the joint landscape is near-degenerate (many bin-path combos within noise of
each other); the machinery robustly detects coherence but cannot yet pin the ruler curve.
CONSEQUENCE (F-SCOPE honored): **no BAO-alone X-range is banked from this run.** The BAO
deliverables are (a) the detection, (b) the weight-robust per-shell theta_BAO(z) table, and
(c) the consistency observation (below) — the SNe leg carries the scale constraint.

## Consistency observation (stated, not fitted)
The weight-robust strong shells at 2.3–2.4° across z 0.70–1.05 sit near the gentle
theta = ell/r(z) drift predicted by the SNe-fitted P1 wall (R_w ≈ 2.2 Gpc, n ≈ 1.06) with
ell ≈ 70 Mpc-scale; the 1.17° (LRG 1.05–1.10), 8.5–8.8° (LRG 0.95–1.00), and 0.71° (QSO
1.85–2.00) hits do NOT thread the same curve (factors 2–3 off). A single-ruler reading
therefore explains a SUBSET of the coherent structure; the outliers are either secondary
noise-grabs, selection-edge artifacts (the 8.8° shell sits at the LRG selection thinning —
the recorded M3-AUDIT candidate), or genuinely not one ruler. Adjudication belongs to
M3-AUDIT / M3b (BOSS cross-check), not to this run.

## Open items carried
- **Radial leg: TRIGGERED in 9 shells but NOT RUN** — the trigger criterion fired (honest
  records in both jsons) but the radial (Delta-z) correlation estimator was never built at
  M3-PREP (only the D1 projection formulas exist). OWED as a follow-up build+run under its
  own gate; until then the Alcock–Paczynski ratio remains unexploited.
- The LRG 0.75–0.80 nominal 70.7° bump center sits outside the search window — fitter edge
  artifact, flagged to the verifier (its p = 0.05–0.10 is not load-bearing anywhere).
- The amended-v2 GPU-audit criterion (post-unblinding machinery touch) — verifier
  re-adjudication REQUIRED (GPU_SPOTCHECK_DIAGNOSIS.md).

## Files
`bao_results_sys.json`, `bao_results_nosys.json` (full per-shell records, look-elsewhere,
joint fits, audit values), `bao_checkpoints/` (104 shell count sets + audit caches),
`GPU_SPOTCHECK_DIAGNOSIS.md`, `spotcheck_BGS_DR_full.npz`.

**Everything above is PROVISIONAL until the blind results-verifier pass (prereg §8) and
Charles's ruling; external-review bar travels.**

## CONSOLIDATED (2026-08-08, blind results-verifier in): BAO leg SUSTAINED — verified LEAD

`RESULTS_VERIFIER_REPORT.md`: two shells recomputed end-to-end from the raw DESI FITS
(strong LRG 1.00–1.05; null ELG 1.20–1.25) — DD/DR/RR/w(θ)/σ bit-identical; the full 52×2
look-elsewhere assembly reproduces bit-identically including the joint-fit variant
instability; detection headline, weight-robust θ(z) table, and the no-BAO-alone-X-range scope
decision all hold. **GPU-audit amendment: AMENDMENT-SUSTAINED** (independent reproduction of
every diagnosis claim; corr(log cell, log diff) = 0.98 — the accumulation signature; a bias,
lost pair, or binning bug cannot evade all three v2 tests simultaneously). AMENDMENTS APPLIED
(supersede wording above):
- The consistency observation must carry BOTH halves: the 2.3–2.4° thread magnitudes sit near
  the SNe-fitted P1 curve (ell ~ 70 Mpc-scale), **but the observed drift DIRECTION across the
  strong shells runs opposite the predicted gentle fall (~1–1.5 bins)** — "sits near the
  curve" may not be over-read; adjudication belongs to M3-AUDIT/M3b/radial. Worst outlier is
  3.8× off the thread (not "2–3×").
- Radial triggers: 9 shells (sys) / 8 (nosys); the radial estimator remains UNBUILT — OWED.
- The v2 audit numeric bounds (1e-8 / 1e-9) are set 2–4× above measured values (data-chased,
  disclosed); **the load-bearing detector is the absolute small-cell whole-pair census and
  must not be weakened in any future recalibration.**
Status: verified LEAD (same-session verifier; external bar travels); four-check complete.
