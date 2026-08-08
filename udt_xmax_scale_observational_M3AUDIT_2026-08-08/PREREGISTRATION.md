# M3-AUDIT PREREGISTRATION — selection-function forensics on the BAO notables (frozen)

Date 2026-08-08 | branch grok | Charles's go: "Do M4 now, audit right behind it." Charles's
framing (binding, recorded 2026-08-07): investigate what DESI did to NORMALIZE the data — the
survey's own layers (mask, fiber-assignment gaps, selection transitions, imaging weights) — as
the outlier suspects, NOT a physics mechanism. Mismatch → solver applied to a third party's
pipeline. Still LCDM-free (F-IMPORT-LCDM intact; DESI normalization ≠ ΛCDM model assumptions).

## 1. The frozen question

Are the strong-shell features' positions/strengths attributable to survey selection/
normalization structure rather than sky clustering — graded per shell, SYMMETRICALLY across
convenient and inconvenient cells alike?

## 2. Targets (frozen; the SAME battery for every target — F-STEER symmetry)

The thread shells: LRG 0.70–0.75 (2.37°), LRG 0.90–0.95 (2.34°), LRG 1.00–1.05 (2.44°),
QSO 0.95–1.10 (1.39°), QSO 1.10–1.25 (2.05°). The outliers: LRG 0.95–1.00 (8.8°; the named
lead — sits at the LRG selection-edge thinning), LRG 1.05–1.10 (1.17°), QSO 1.85–2.00 (0.71°).
Fitter-level: LRG 0.75–0.80 (nominal 70.7° out-of-window center). Plus the thread
DRIFT-DIRECTION tension (runs opposite the predicted gentle fall, ~1–1.5 bins) as a
cross-target question: can selection gradients tilt bump centers coherently?

## 3. The frozen test battery (forensics only; per target)

- **B1 dN/dz edge structure:** the tracer's selection transitions vs the shell boundaries
  (edge thinning inside/adjacent); quantified slope/curvature at the edges.
- **B2 region stability:** drop-one-jackknife-region θ_b stability (a sky feature is
  region-stable; a mask/footprint artifact tracks specific regions).
- **B3 sub-shell split:** z-halves of the shell — persistence vs edge-tracking of the bump.
- **B4 cap asymmetry:** per-cap (NGC vs SGC separately) w(θ) recompute — imaging-driven
  selection artifacts are typically cap-asymmetric; sky clustering is not.
- **B5 remaining-weight sensitivity:** WEIGHT_ZFAIL on/off (the one weight layer not yet
  varied; WEIGHT_SYS already done at M3).
- **B6 (LRG 0.75–0.80 only):** refit with the bump center constrained in-window; report the
  constrained result and grade the 70.7° center as the edge artifact it appears to be, or not.

## 4. Deliverable + grades (frozen)

Per target: **SELECTION-SUSPECT** (≥2 battery flags consistent with a named selection layer) /
**SKY-ROBUST** (clean across the battery) / **INCONCLUSIVE** — with the evidence per test.
Plus the drift-direction note (B1×thread synthesis). **FORENSICS ONLY — F-FIX (new, this
step): producing any "corrected" measurement, reweighting invention, or revised banked number
FIRES. The audit grades; it never repairs. Banked M3 results stand untouched regardless of
outcome; grades attach as provenance annotations.**

## 5. Falsifiers

F-FIX (above, primary). F-STEER: symmetric battery — the thread shells face the same tests as
the outliers; an audit that only convicts inconvenient cells or only acquits convenient ones
is itself the failure. F-IMPORT-LCDM: intact throughout (no fiducial anything; blacklist
stands). F-SCOPE: grades + evidence only; no physics conclusions, no mechanism language.

## 6. Bounds + process

Targets only (~9 shells), CPU, checkpoint/count reuse where valid (per-cap counts require
recomputation — bounded, the M3 per-shell costs apply); chunked outputs; staged banking. One
audit agent → one blind adversarial review of the audit → consolidation. Outcomes:
AUDIT-GRADES / AUDIT-INCONCLUSIVE(component).
