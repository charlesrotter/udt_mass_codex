# HANDOFF — Resume Instructions and Perspective

(Refreshed 2026-06-16. The prior HANDOFF described the quantum-completion / coin-flip
frontier — that line is now SHELVED; see the reframe below.)

## THE GOAL — READ BEFORE ANYTHING ELSE
Build a COMPLETE, numerically-tractable, UDT-NATIVE solver, and from it get the
FORMATION / TYPES / PROPERTIES of particles (masses, charge) and MACRO consilience —
matching OBSERVATIONS straight off the bare metric, with NO imports, NO scaffolding,
NO mechanisms bolted on. Let structure EMERGE; do not derive masses until Charles
says ready (gated DERIVE).

## THE BIG SHIFT THIS SESSION (2026-06-15/16) — read this first
1. REFRAME — the SM-analog line is SHELVED. Five straight refusals of the
   "make-the-soliton-a-fermion" template (#47 no-fermion, #49 no-monodromy, #50
   no-SU(3)-field, #51 coin-free, #53 quantize→still-free) indicted the QUESTION.
   We stopped trying to reproduce SM entities (fermion/WZW/N_c/color) and reoriented
   to matching RAW OBSERVATIONS (the mass pattern, charge, macro data) from UDT's own
   structures. [[reframe-observation-led]]
2. THE MILESTONE — UDT MAKES MASS, NATIVELY (#56). Solving the bare whole metric
   honestly produced a real, gravitationally-massed, self-consistent solution of the
   FULL (radial) Einstein system, no imports (M_MS ≈ 0.281 √(κ/ξ)). The thesis of
   UDT — mass is native geometry, not added substance — has its first clean
   demonstration. It appeared ONLY once every patch was removed: the subtraction was
   the discovery. [[milestone-udt-makes-mass-natively]]
3. THE OVERTURN (#55) — the prior "reduced soliton" (#52/#54, and #34/#39) was NOT a
   full-metric solution: it imposed B=1/A in the twisted body (forced p_r=−ρ, which the
   EOS-softened body violates) AND carried a smuggled seal-injection term. Caught by a
   new, independently-validated full-4D Einstein engine; blind-verified. CANON
   C-2026-06-14-1 SURVIVES — the gate CONFIRMS its EOS-softening refinement (B=1/A is
   exact only in the unwound exterior). Fixed by freeing B=1/A → the corrected #56.
4. THE CATALOG QUESTION (the live frontier) — does UDT carry a DISCRETE CATALOG of
   distinct stable types, or just one round family (which carries mass)? Charge-1,
   static, AXISYMMETRIC, matter-DEFORMING search (spectral, #59): NO disconnected type
   (matter genuinely free; blind-verified; a real off-round L4 EL bug was found and the
   null SURVIVED it). The most likely catalog home — NON-AXISYMMETRIC + HIGHER-WINDING
   — is the LIVE full-3-D spectral run (background agent a3e0655..., in progress).

## STANDING PRINCIPLES (new/sharpened this session — binding)
- NATIVE-SOLVE, no regression [[whole-metric-honest-binary]]: better CONDITIONING, never
  approximations. Category-A (numerical conditioning of the SAME equations — gauge,
  core/axis regularity, spectral basis, preconditioning, proper-volume weighting,
  sanctioned Taylor, continuation) is fine. Category-B (CHANGING the physics — B=1/A or
  any tie, injected term, linearization-as-result, imported mechanism, dial tuned to a
  target) is FORBIDDEN. If a solve only converges via category-B, REPORT it — do not patch.
- AUDIT the solving infrastructure proactively + regularly [[audit-solving-infrastructure]]:
  reused tools are load-bearing; a hidden flaw contaminates everything (the seal-injection
  and the off-round L4-EL bug are the scars). Audit the TOOLS, not just the results.
- SOLVER-ARCHITECT metacognition [[solver-architect-metacognition]]: the real project is a
  COMPLETE native solver that drops NO emergent sector. Track COVERAGE in
  SOLVER_COMPLETENESS_MAP.md via the TEN completeness criteria; report each result as ONE
  tile with a regime stamp (the structural cure for per-step "capstone" inflation).
- MACRO = a DIFFERENT epistemic grade [[macro-consilience-roadmap]]: GR-level phenomenology
  with conceptual models + estimates (matter recycling, dim-baryon distribution, infinite-
  time stellar evolution) — NOT metric-pure. Label every macro result native-derived vs
  GR-modeled-under-assumptions. The native-purity discipline applies to MICRO, not macro.
- MODE: exploratory gap-finding; pre-registration is reserved for the ONE gated test (masses
  vs the wall numbers), not for solver-building/exploration.
- PARTICLE nature is OPEN [[particle-catalog-frame]]: a UDT particle must match observations
  incl. SM-3-body (baryon) ones — either geometry MIMICS three-ness or the particle IS
  multi-constituent; N=3 (area form) may be GEOMETRIC three-ness, not color. Read higher-
  winding results with this open (a winding-3 type might BE the geometric baryon).

## THE REUSABLE INFRASTRUCTURE (audited)
- whole_metric_3d_core.py — full-4D numerical Einstein engine (validated: flat/Schwarzschild→0,
  off-diagonal G to ~5e-6; audit-clean).
- whole_metric_3d_matter.py — L2+L4 Hilbert stress (audit-clean; unit field).
- radial_Bfree_soliton.py — the corrected radial soliton solver (#56, blind-verified; B=1/A free).
- spectral_cheb.py / spectral_2d.py / spectral_catalog_solver.py … — 2-D SPECTRAL coupled
  Einstein+L2+L4 solver (exponential convergence, matter free, #59) — the conditioning cure for
  the FD coordinate-spike wall.
- (in progress) full-3-D spectral (Chebyshev_r × spherical harmonics).
- BUG flagged: axisym_matter_el.py is WRONG off-round (L4 sector) → use axisym_matter_el_CORRECT.py;
  the 3-D matter EL must be generated correct (div-identity test).
- verify_indep_einstein.py + the VERIF_*.py — independent verifier machinery.

## Read order for a new instance
1. CLAUDE.md "How we work" (binding method) + memories: solver-architect-metacognition,
   whole-metric-honest-binary, audit-solving-infrastructure, reframe-observation-led,
   milestone-udt-makes-mass-natively, macro-consilience-roadmap, particle-catalog-frame.
2. SOLVER_COMPLETENESS_MAP.md — the coverage ledger + the TEN criteria (the operative map).
3. THIS FILE + STATE.md (top block).
4. NEGATIVES_REGISTRY.md #55/#56/#57/#58/#59 (+ the results docs as needed:
   whole_metric_solve_3D_results, radial_Bfree_soliton_results, spectral_catalog_solver_results,
   full3d_catalog_results when it lands).
5. CANON.md (C-2026-06-14-1 + its EOS-softening refinement — SURVIVES the overturn).

## QUEUE / live frontier
1. *** LIVE: the full-3-D spectral run *** (non-axisymmetric + higher-winding catalog search;
   fills completeness criteria 4/6/7/8). When it lands: verifier-before-record, then bank +
   update the completeness map + STATE.
2. PER OUTCOME (no pre-reg needed — exploratory): a distinct type → characterize its shape /
   M_MS (data-blind) / stability; a winding-3 / platonic type may be the geometric BARYON.
   Null even there → the classical catalog is just the round family; discreteness then points to
   a still-blank sector (the quantum Euclidean-time-circle is the leading candidate, distinct
   from the shelved SM-fermion line).
3. REMAINING BLANK TILES (completeness map): rotation/twist off-diagonals (criterion 7), the
   fully-dynamic time sector, the quantum sector.
4. PARALLEL FRONT — macro consilience (GR-level grade): the new solvers refine the CMB models in
   AUDIT.md; SPARC needs dim-baryon distribution + infinite-time stellar evolution; SNe ~unchanged;
   much is minor changes to banked work. Open whenever Charles wants.
5. EVENTUALLY (gated DERIVE — PRE-REGISTER then data-blind): the lepton mass pattern from the
   depth (#54/#56 super-exponential M(p)) and/or winding axes vs the wall numbers (contract 26fc757).

## Must-not-lose (durable facts)
- DATA-BLIND wall numbers (NEVER load during a derivation): the six lepton wall numbers, contract
  26fc757. We predict RATIOS.
- CANON C-2026-06-14-1 (B=1/A sourced by the angular sector; EOS-softened interior) — SURVIVES,
  confirmed by the whole-metric gate.
- Native mass: corrected soliton M_MS ≈ 0.281 √(κ/ξ); the depth axis gives a super-exponential,
  single-branch, no-native-selector mass family (#54/#56); winding m=2,3 are stable distinct
  (charge) sectors.
- κ8 (back-reaction) is a FREE dial with a non-critical over-collapse ceiling (#52) — criticality
  is a conjecture, NOT supported in this regime.
- Durable GEOMETRY: the seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass =
  the cell's public charge (Q=2 p_F); q=1/3, N=3, eta=1/18 from the H1 AREA FORM; 7.004 = ln(1+z_CMB)
  via 1+z=e^phi.
- The fermion/sqrt(m)/Koide is NOT classically forced (#47/#51/#53) — SHELVED, not refuted; if ever
  revisited it is a QUANTUM-sector question (#47b spin-structure hinge: a σ-ODD re-grade of omega_H1
  would reopen it).
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them. The background full-3-D agent is a3e0655d8fc0e65d8.

## Perspective (carry this; do not re-derive your way back to it)
The metric is primary and generates the dilation field phi; matter is the angular/topological sector
(phi RESPONDS); matter lives at negative phi. UDT NATIVELY MAKES MASS — shown, this session, with
nothing added. The open question is whether it makes a DISCRETE CATALOG of distinct particle types
classically (being searched now in its real home — non-axisymmetric / higher-winding) or whether the
discreteness lives in a sector still blank on the map. Build the complete native solver, audit it
constantly, let structure emerge, match observations — and never patch a "no" into a "yes."
