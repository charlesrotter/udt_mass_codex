# COMPLETION PROGRAM — finish every thread before the next level

**Directive (Charles 2026-06-21):** finish ALL F-items (even the substantially-done ones — no hanging
threads), THEN audit the solvers + previous results top-to-bottom. Goal (next few days): a CLEAN,
PHYSICS-CORRECT SOLVER for doing work later. Finish everything before moving to the next level.
Discipline: [[infrastructure-first-not-exciting-stuff]] — check/double/triple-check; verifier-before-record
on every closure; hunt imports / frozen items / improper assumptions. Status-of-record = the SCOREBOARD in
FOUNDATIONAL_ASSUMPTIONS_LEDGER.md. This doc = the actionable checklist.

## PHASE A — finish F1–F8 (close every residual to a clean state)

- [x] **F1 — gravity curvature action.** CLOSED (F1F3_closure_results.md, verified CLEAN). DERIVED (vacuum!=GR). FINISH: confirm the derivation is airtight;
  formally close the superseded gravity-side residuals (N4 C1-uniqueness scope, N6 asymptotic-flatness-vs-
  no-infinity tension, N8 local-Lorentz-at-extremes); document the FREE X dial (kinetic/curvature ratio) as
  the one principle-unfixed parameter, with the no-ghost+Cassini window. Deliverable: F1 closure record.
- [x] **F2 — matter action L2+L4.** CLOSED (F2_closure_results.md, verified CLEAN). RESOLVED = minimal-but-not-unique. FINISH: document the {X^2,L6} admissible
  extras as a bounded value-open ambiguity (mass-only, not EOS); CHECK the load-bearing full-SO(3) target
  assumption (if reduced, V re-enters). Deliverable: F2 closure record.
- [x] **F3 — a(phi) coupling.** CLOSED (folded into F1F3_closure_results.md, verified CLEAN). DERIVED a=e^{+phi} (entangled w/ F1). FINISH: tie off with F1; confirm the
  physical-coupling re-grade is airtight; close "a=-1 silently used in P1-P5d" (the P1-P5 re-audit covers the
  downstream). Deliverable: folded into F1+F3 closure.
- [ ] **F4 — finite-cell / seal / boundary.** Seal-as-QUANTIZER question CLOSED (verified). FINISH the STRUCTURE:
  is the container DERIVED or POSITED — A1 (no spatial infinity), D2 (I×S^2 doubling vs S^2×S^1 Chern competitor),
  D3 (inner-core r=0 removal), and WHICH involution (t->-t vs P×T); resolve the time-surface/radial-crease fork
  held DERIVED-conditional. Deliverable: F4 structure closure (derived-vs-posited, each tagged).
- [x] **F5 — critical-universe frame.** CLOSED (F5_critical_universe_closure_results.md, verified CLEAN) = ADMITTED WORKING FRAME with a derived self-consistency mechanism (c²=2GM/R); pinning dimensional-only; does NOT bear on must-quantize. PARTIAL (bootstrap = critical universe w/ a why, c^2=2GM/R). FINISH:
  is "matter at ONE critical amount" DERIVABLE or an admitted FRAME? is the pinning derivable or dimensional-
  only? Deliverable: F5 closure (derived vs admitted-frame, explicit).
- [ ] **F6 — postulate-A boundary.** OPEN (admitted). FINISH the clean ledger: what is truly POSTULATED
  {hbar, spin-1/2, statistics} vs FREE-with-the-imported-metaplectic-framework vs NATIVE (i=area-form,
  cell-independence); is quantization the right framework vs later geometric emergence (the door-open clause)?
  This is an ADMISSION/decision item, not a derivation — make the boundary crisp + Charles-signed. Deliverable:
  F6 postulated-vs-free-vs-native ledger.
- [x] **F7 — scale bridge / ~10^40 autonomy gap.** CLOSED-TO-CLEAN-STATE (F7_scale_bridge_native_results.md, verified CLEAN): imported-Hubble REMOVED (M/R=c²/2G native; absolute size = unpinned dilatation modulus, H0 order-correct as OUTPUT, number pinning-deferred to the coupled solve); cosmic->particle half = the IRREDUCIBLE known-open gap, stated cleanly (M doesn't bridge; depth ~115x short; particle size must come from the cell's own cavity/angular structure). OPEN (known-hard). FINISH to a clean state: do the
  imported-Hubble NATIVE redo (anchor A=7.004, H0/rho_crit as DERIVED outputs); then either close the cosmic->
  particle bridge or formally characterize it as the IRREDUCIBLE open gap (what's needed, why it's hard).
  Deliverable: native cosmic-scale redo + bridge status record.
- [x] **F8 — embedded metric-form choices.** CLOSED (F8_metric_choices_results.md, verified CLEAN; one named residual = non-spherical on the derived operator, value/solve-open). PARTIAL. FINISH: characterize each embedded choice (static /
  spherical / diagonal / areal-r / P8 slot-id) as DERIVED-from-the-principle vs CHOSEN (free solution-space DOF),
  explicitly. Deliverable: F8 choice-provenance record.

## PHASE B — audit solvers + previous results, top to bottom

- [ ] **B0 — verify the P1-P5 re-audit's COMPLETENESS** (P1P5_reaudit_vs_derived_operator_results.md) — did it
  miss any silently-"survives" result that was never re-run? (triple-check)
- [ ] **B1 — close the loud gap: re-grade P5c (family/landscape)** on the derived operator (vacuum!=GR + a=e^phi)
  — the "no family / one soft object" answer (Charles's family question), un-re-graded.
- [ ] **B2 — secondary P-gaps:** P1 static spatial-shear on the EXACT operator; the P5a'/P5b solution-manifold.
- [ ] **B3 — standing imports:** M12 (Theta=m*pi winding BC -> native sector-distinctness mechanism, or formally
  scope it); M10/M11 (S^2-vs-S^3 identity + cos-theta texture — re-settle or confirm).
- [ ] **B4 — SOLVER INFRASTRUCTURE audit** ([[audit-solving-infrastructure]]): engines/solvers/stress for hidden
  patches/imports/approximations/frozen-DOF; the pole-stable HYBRID (approx) now superseded by the exact operator
  — confirm nothing still rides the hybrid; B=1/A over-imposition; seal-injection; etc.
- [ ] **B5 — PREVIOUS RESULTS audit, top to bottom:** re-grade the banked corpus against the corrected foundation;
  NEGATIVES_REGISTRY re-grade pass; flag every result still scoped to the old operator.
- [ ] **B6 — wide-range NUMERICS upgrade:** make the box-control gate statistically airtight (spectral/multidomain/
  KEH-SCF/pseudo-arclength/JFNK+spectral-PC; Nt>=5; strong coupling; A2 true-Einstein), per the recorded plan.

## GOAL
A CLEAN, PHYSICS-CORRECT SOLVER (correct + complete; imports/frozen/approximations removed or explicitly scoped;
every prior result re-graded on the corrected foundation) — ready for later work. THEN the next level (quantize, etc.).

## LOG (append as items close; each verifier-passed before checking the box)
- (2026-06-21) Program opened. F1-F4 substantially done (scoreboard); finishing residuals + F5-F8 + Phase B.
