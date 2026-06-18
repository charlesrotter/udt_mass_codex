# HANDOFF — Resume Instructions and Perspective

## *** 2026-06-17 UPDATE (read FIRST; supersedes the queue below) ***
Overnight automode run executed the whole "fix-static then characterize-catalog" arc. READ
STATE.md top block + winding_platonic_phase3b_results.md (with its grid-convergence CORRECTION)
+ off_round_solver_results.md + winding_catalog_verified_results.md + infrastructure_audit_3d_2026-06-16.md.
- PHASE 1: INFRA-AUDIT #2 — #60 machinery clean; 3 premise corrections (off-round wall = solver not
  physics; "round gate machine-zero" was ~1%; div(T) gate broken→fixed divT_excised.py).
- PHASE 2: OFF-ROUND WALL BROKEN — full3d_newton.py (explicit-Jacobian Newton, category-A, value-equiv
  1.4e-14, B=1/A free). Plus sh_theta_operator.py + full3d_grid_shexact.py (SH-exact θ for m≠0).
- PHASE 3/3b: winding catalog of SECTORS exists; m=1 round STABLE grid-stable minimum (M~0.29-0.30);
  m>=2 round UNSTABLE → lower non-axisym states (m=2 toroidal=Skyrme B2; m=3 axial, NOT tetrahedral),
  coupled-stable along steepest modes. *** BUT m>=2 ground-state MASS NOT grid-converged (M_MS(2)
  ranged 9.8-38.5; residual-Newton finds different critical points per grid) — masses/shapes UNSETTLED. ***
- METHOD: fixed-metric matter Hessian over-counts instabilities for gravitating solitons; use coupled
  re-solve [[gravitating-soliton-stability-test]]. SH power-spectrum symmetry ID self-test PASSED.
- ENERGY MINIMIZER (energy_minimizer.py, BUILT 2026-06-17): global-min search now WORKS at a fixed grid.
  basin_hop confirms the m=2 ground state = the OBLATE basin, M~12.2-12.4 @18x8x8 (multistart 12.16 +
  basin_hop 12.37 agree). [Gate 1 caught a sign bug in the original gradient-descent inner loop; pivoted
  local_min->Newton + basin_hop, justified because phase3b_descend showed the states are already MINIMA.]
  Warm-start CONTINUATION was tried+FAILED (cross_grid_branch.py; don't repeat).
- MASS GRID-CONVERGENCE = a ROBUST NEGATIVE (2026-06-17, winding_platonic_phase3b_results.md final
  section). Built large_grid_solver.py: jacrev Jacobian build dominates (38-133s/iter); dense works but
  cost-limited; matrix-free 2-grid Newton-Krylov STALLS (CG step not a descent direction, cheap+geometric
  coarse both); deep-floored warm-start continuation DRIFTS (m=1 0.29->0.32 with growing psivar -- interp
  injects non-axisym structure into steep solitons; m=2 oblate 16.9->41->94 diverges). FRESH per-grid m=1
  IS grid-stable. NET: catalog STRUCTURE solid + m=1 mass pinned (~0.29-0.30), but m>=2 ABSOLUTE MASSES
  are NOT grid-convergeable with current machinery. Banked m=2 = at-grid only (oblate ~12.2-12.4 @18x8x8).
- CROSS-SESSION RECON (cross_session_recon_2026-06-17.md): mined the parallel branch
  origin/session-2026-06-17 (quantization-emergence fork, NOT merged; we keep main). KEY USABLE FINDING
  that REDIRECTS fork B: a SINGLE-CELL FLUCTUATION/"vibration-notes" eigenvalue solver is BOX-CONTROLLED
  (4x blind-verified there) -- it will NOT give lepton ratios; only the box's integer ladder is intrinsic.
  Escape (convergent both sessions): discreteness is TOPOLOGICAL (winding) or in the CLOSED-TIME/non-
  stationary sector. Lepton GENERATIONS (same charge) are NOT the winding catalog (=charge) NOR the
  box-controlled breathing tower => most likely the CLOSED-TIME selector (#57 done properly). Reusable:
  their exact deep-phi fluctuation operator + mpmath log-grid dps>=50 recipe (float64 garbage in deep-phi).
  TENSION to reconcile: they identify the single-cell soliton as a global-monopole TEXTURE (Barriola-
  Vilenkin, Hopf=0), NOT a Skyrmion -- hold our "Skyrme B=2 torus" reading loosely.
- THE FORK (Charles's call): (A) RESEARCH-GRADE solver upgrade to pin m>=2 masses (fix/replace the
  matrix-free solver -- debug why the CG step isn't a descent direction; or a refinement that doesn't
  inject non-axisym structure; or Shamanskii/chord Jacobian-reuse to amortize the dense build); OR
  (B-REDIRECTED) the quantum/spectrum route -- but NOT the box-controlled single-cell fluctuation
  spectrum; target the CLOSED-TIME/non-stationary selector (#57 done properly) or the topological/winding
  ("spectrum") solver — Charles's hunch is it may BUILD ITSELF as the natural modes of these classical
  objects ([[no-presumed-quantum-sector]], the angular sector = QCD/QED reverse-engineering clue-source).
  Both are gated on Charles's go. m=4 + finer-grid (Nps>=12) m=3 tetrahedral check are smaller open items.
- FOUR-CLUSTER BRANCH AUDIT (cross_session_recon_2026-06-17.md, all to OUR standards): box-control
  CONFIRMED (free-BC test + independent re-run); #51 (non-unit carrier) is REAL but QUARANTINED to the
  shelved single-cell-V line -- our soliton/catalog/canon use the UNIT S^3 carrier and are UNAFFECTED (we
  do NOT need to close #51 for main); phi-angular dynamical-resonance "dead" is only PROVISIONAL/one-channel
  (founding suspect NOT retired); pilot-wave/Schrodinger = HOSTING not emergence (generic-relativity + parked
  hbar); native Born measure e^{phi} HOLDS. 3 provisional cross-session negatives imported to NEGATIVES_REGISTRY.
- THE "i" FINDING -> AN SM-ASSUMPTION DERIVED [[udt-derives-sm-assumptions]] (Charles reframe 2026-06-17):
  the quantum "i" (complex structure) is a POSTULATE in QM/SM; the branch found (structural part native +
  audit-unrefuted) that i = the S^2 AREA FORM = the topological charge (N=3,q=1/3). => UDT may DERIVE the
  "why is QM complex" assumption (the GOOD kind of win: derive an SM ASSUMPTION, never reproduce an SM
  ENTITY). Caveat: ponder/MAP-grade identification; the i-FLOW (dynamics) is the parked clock/hbar gap.
  LEDGER (derive vs share): i=candidate DERIVE; fermion=SHARED postulate (Berry phase 0); Born=partial.
- GAP UNIFICATION (the sharp result): the flowing-i, the de Broglie carrier, the rest-energy clock, and
  hbar are ALL THE SAME ONE missing input -> candidate source = the CLOSED-TIME / seal sector. THREE
  independent threads -- lepton mass FAMILY (generations), the native WAVE, and the quantum i -- ALL
  converge on the closed-time selector.

*** RECOMMENDED NEXT PUSH (driver, 2026-06-17): the CLOSED-TIME / non-stationary selector (#57 done
PROPERLY -- full dynamical, not static-linearized). It is now the single high-value, de-risked target:
(a) three threads converge on it; (b) the box-control dead-end is ruled out (don't build a single-cell
fluctuation spectrum); (c) #51 shown not to threaten main; (d) the SM-assumption lens says a win here
= deriving "why QM is complex" + the dynamics (foundational, not hosting). MAP it first (premise ledger,
lay PONDER with Charles) -- it is a new dynamical sector, gated DERIVE discipline applies. The fork's
option (A) (research-grade solver to pin m>=2 absolute masses) remains valid but lower-value than (B);
absolute masses may also be moot if generations live in the closed-time spectrum (ratios, grid-robust).

(Refreshed 2026-06-16/17. The prior HANDOFF described the quantum-completion / coin-flip
frontier — that line is now SHELVED; see the reframe below.)

## THE GOAL — READ BEFORE ANYTHING ELSE
Build a COMPLETE, numerically-tractable, UDT-NATIVE solver, and from it get the
FORMATION / TYPES / PROPERTIES of particles (masses, charge) and MACRO consilience —
matching OBSERVATIONS straight off the bare metric, with NO imports, NO scaffolding,
NO mechanisms bolted on. Let structure EMERGE; do not derive masses until Charles
says ready (gated DERIVE).

## THE BIG SHIFT (2026-06-15/16 session) — read this first
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
4. THE CATALOG QUESTION — RESOLVED this session (see the 2026-06-17 top block): the off-round wall was
   BROKEN (Phase 2) and the catalog characterized (Phase 3/3b) — a discrete winding catalog of SECTORS
   exists (m=1 round STABLE, mass grid-pinned ~0.29-0.30; m>=2 break to non-axisym oblate/toroidal,
   coupled-stable); m>=2 ABSOLUTE masses are NOT grid-convergeable = a tooling negative. (The 2026-06-16
   "#60 INCONCLUSIVE / solver-limited / catalog STILL OPEN" framing is RETIRED — HANDOFF_ARCHIVE.md.)
5. DISCRETENESS-IS-DYNAMICAL ([[particle-catalog-frame]]) SURVIVES but is REDIRECTED: discreteness is
   NOT a static catalog AND NOT a single-cell eigenvalue/standing-wave tower (the cross-session box-control
   audit showed the latter is box-controlled — [[single-cell-spectrum-box-controlled]]). The lepton FAMILY
   (generations) is the CLOSED-TIME / non-stationary selector (#57 done properly) — the live target (top
   block). (The 2026-06-16 "build an eigenvalue solver of one depth family" plan is retracted —
   HANDOFF_ARCHIVE.md.)
6. THE QUANTUM REFRAMING ([[no-presumed-quantum-sector]]): do NOT presume a separate quantum
   SECTOR. Quantum-APPEARING observations (discreteness, spin, exclusion) are TARGETS the
   GEOMETRY may resolve (standing waves / eigenvalue / topology). The UDT/QCD–QED overlap is
   with their GEOMETRIC/CLASSICAL face (gauge = connection; Skyrmion = classical soliton;
   large-N QCD is classical) — coherent with no quantum layer. The #51/#53 fermion results
   used RETIRED SM-imports, so the native fermion verdict is UNWRITTEN. For the precision tier
   (g−2, Lamb shift, …): REVERSE-ENGINEER the needed solver from quantum math (stochastic
   quantization / Madelung / ℏ-loop / effective action / RG↔DILATION first) — extract the
   TARGET + computational TYPE, NEVER import the mechanism. Hardest eventual test = Bell
   nonlocality, where UDT's global coupling may have the resources locality forbids.

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
  winding results with this open (a winding-3 type might BE the geometric baryon). NEW (2026-06-16):
  the catalog itself may be a DYNAMICAL SPECTRUM (standing-wave eigenmodes on the depth continuum),
  not static cells — see big-shift #5.
- NO PRESUMED QUANTUM SECTOR [[no-presumed-quantum-sector]]: don't reify "the quantum sector" as a
  place things live. Quantum-appearing observations are geometric TARGETS (standing-wave / eigenvalue
  / topology); the QCD/QED overlap is with their classical face; the fermion native-verdict is
  UNWRITTEN (the #51/#53 "no" used retired imports). Reverse-engineer the precision solver from
  quantum math (RG↔dilation first) — extract target+type, never import the mechanism.

## THE REUSABLE INFRASTRUCTURE (audit status per item — do NOT assume "audited" blanket)
- whole_metric_3d_core.py — full-4D numerical Einstein engine (validated: flat/Schwarzschild→0,
  off-diagonal G to ~5e-6). INFRA-AUDIT #1 CLEAN (08fd4ef).
- whole_metric_3d_matter.py — L2+L4 Hilbert stress (unit field). INFRA-AUDIT #1 CLEAN.
- radial_Bfree_soliton.py — corrected radial soliton solver (#56, blind-verified; B=1/A free).
  INFRA-AUDIT #1 CLEAN.
- spectral_cheb.py / spectral_2d.py / spectral_catalog_solver.py … — 2-D SPECTRAL coupled
  Einstein+L2+L4 solver (exponential convergence, matter free, #59) — the conditioning cure for
  the FD coordinate-spike wall. VERIFIER-CHECKED via #59 (the off-round EL bug was caught there);
  NOT yet through a standalone infra-audit.
- full-3-D spectral (Chebyshev_r × Gauss-Legendre_θ × Fourier_ψ): analytic 3-D Weyl Einstein
  (pole-stable) + CORRECT 3-D matter EL. INFRA-AUDIT #2 CLEAN (2026-06-17,
  infrastructure_audit_3d_2026-06-16.md; it corrected #60's overstated "machine-zero gate / div(T) exact"
  — round recovery was ~1%, the div(T) gate was broken → fixed by divT_excised.py). The OFF-ROUND wall
  is BROKEN by full3d_newton.py (Phase 2, category-A, value-equiv 1.4e-14, B=1/A free).
- NEW this session (2026-06-17): full3d_newton.py (explicit-Jacobian Newton solver) · full3d_grid_shexact.py
  (SH-exact θ for m≠0 winding; round bit-identical) · divT_excised.py (fixed conservation gate) ·
  winding_catalog_map.py (winding seeds + diagnostics) · energy_minimizer.py (global-min basin-hop, WORKS
  at a fixed grid) · cross_grid_branch.py (interp_state — but warm-start CONTINUATION DRIFTS, don't reuse).
  ⚠ large_grid_solver.py (matrix-free 2-grid Newton-Krylov) STALLS — do NOT rely on it; m>=2 absolute-mass
  grid-convergence is the open tooling negative.
- BUG (fixed): axisym_matter_el.py was WRONG off-round (L4 sector) → axisym_matter_el_CORRECT.py;
  the 3-D EL (matter_el_3d_gen.py) is generated correct (div-identity test). Deprecate the buggy one.
- verify_indep_einstein.py + the VERIF_*.py — independent verifier machinery.

## Read order for a new instance
1. CLAUDE.md "How we work" (binding method) + memories: solver-architect-metacognition,
   whole-metric-honest-binary, audit-solving-infrastructure, reframe-observation-led,
   milestone-udt-makes-mass-natively, no-presumed-quantum-sector, particle-catalog-frame
   (esp. the 2026-06-16b "catalog = dynamical spectrum" sharpening), macro-consilience-roadmap.
2. SOLVER_COMPLETENESS_MAP.md — the coverage ledger + the TEN criteria (the operative map).
3. THIS FILE + STATE.md (top block).
4. NEGATIVES_REGISTRY.md (#55-#60 + the 3 cross-session imports) + this session's results docs:
   off_round_solver_results, winding_catalog_verified_results, winding_platonic_phase3b_results
   (with its grid-convergence CORRECTION + the energy-minimizer + the mass-grid-convergence NEGATIVE),
   infrastructure_audit_3d_2026-06-16, cross_session_recon_2026-06-17. Older: whole_metric_solve_3D_results,
   radial_Bfree_soliton_results.
5. CANON.md (C-2026-06-14-1 + its EOS-softening refinement — SURVIVES the overturn).

## QUEUE / forward items (the LIVE next push is the top-block RECOMMENDED NEXT PUSH = the CLOSED-TIME selector)

NOTE (2026-06-17): the 2026-06-16 "fix-static THEN build the single-cell eigenvalue solver" order is
DONE / REDIRECTED and ARCHIVED in HANDOFF_ARCHIVE.md. Item 1 (fix the off-round static solver) = DONE
(Phase 2, full3d_newton). Item 2 (single-cell eigenvalue/standing-wave solver) = REDIRECTED — the
cross-session box-control audit retired it (a single-cell fluctuation spectrum is box-controlled). The
live frontier is the CLOSED-TIME selector (see the top-block RECOMMENDED NEXT PUSH). Remaining forward items:

3. THREE-TIER ROADMAP (the tractability split — different builds, NOT one regime): STRUCTURE
   (mass/charge/static catalog) → the static solver (have it); SPECTRA (discreteness / the mass
   family) → the eigenvalue/standing-wave solver (item 2); PRECISION (g−2, Lamb shift, running
   coupling) → a DYNAMICAL/response solver, REVERSE-ENGINEERED from quantum math (RG↔dilation first).
4. REMAINING BLANK TILES (completeness map): rotation/twist off-diagonals (criterion 7); the
   fully-dynamic time sector; the quantum-APPEARING observations (tile H — reframed as geometric
   targets, no separate sector presumed).
5. PARALLEL FRONT — macro consilience (GR-level grade, label native-derived vs GR-modeled): the new
   solvers refine the CMB models in AUDIT.md; SPARC needs dim-baryon distribution + infinite-time
   stellar evolution; SNe ~unchanged; much is minor changes to banked work. Open whenever Charles wants.
6. EVENTUALLY (gated DERIVE — PRE-REGISTER then data-blind): the lepton mass pattern from the depth
   (#54/#56 super-exponential M(p)) and/or the eigenvalue spectrum (item 2) vs the wall numbers
   (contract 26fc757).

## Must-not-lose (durable facts)
- DATA-BLIND wall numbers (NEVER load during a derivation): the six lepton wall numbers, contract
  26fc757. We predict RATIOS.
- CANON C-2026-06-14-1 (B=1/A sourced by the angular sector; EOS-softened interior) — SURVIVES,
  confirmed by the whole-metric gate.
- Native mass: radial #56 soliton M_MS ≈ 0.281 √(κ/ξ) (radial-grid value); the full-3-D round m=1 mass
  is grid-pinned ~0.29-0.30 (Phase 1/3b). The depth axis gives a super-exponential, single-branch,
  no-native-selector mass family (#54/#56). Winding m=2,3 are distinct charge sectors that break to
  NON-axisym (oblate/toroidal) coupled-stable ground states; their ABSOLUTE masses are NOT yet
  grid-convergeable (tooling negative).
- κ8 (back-reaction) is a FREE dial with a non-critical over-collapse ceiling (#52) — criticality
  is a conjecture, NOT supported in this regime.
- Durable GEOMETRY: the seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass =
  the cell's public charge (Q=2 p_F); q=1/3, N=3, eta=1/18 from the H1 AREA FORM; 7.004 = ln(1+z_CMB)
  via 1+z=e^phi.
- The fermion/sqrt(m)/Koide is NOT classically forced (#47/#51/#53) — SHELVED, not refuted; if ever
  revisited it is a QUANTUM-sector question (#47b spin-structure hinge: a σ-ODD re-grade of omega_H1
  would reopen it).
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.

## Perspective (carry this; do not re-derive your way back to it)
The metric is primary and generates the dilation field phi; matter is the angular/topological sector
(phi RESPONDS); matter lives at negative phi. UDT NATIVELY MAKES MASS — shown, with nothing added
(the first clean "mass from bare geometry," in Wheeler's "mass without mass" lineage but stable where
his geons were not). The emerging story, coherent across the whole arc: MASS is geometric and STATIC;
DISCRETENESS may be its SPECTRUM — dynamical, standing-wave eigenmodes on the continuous depth family,
NOT a catalog of static cells (the static searches keep returning continua, which may be the geometry
telling us we were looking for the wrong KIND of object). And there may be NO separate quantum sector
at all: what we call "quantum" (discreteness, spin, the QCD/QED structures) may be the geometry's
standing-wave / eigenvalue / topological behavior seen through the quantum calculational layer. Build
the complete native solver (now: a static one that works to 2-D/round/off-round-3-D incl. the winding
catalog, plus a CLOSED-TIME / non-stationary one to build — NOT a single-cell eigenvalue tower, which is
box-controlled); audit it constantly; let structure emerge; match observations; never patch a "no" into
a "yes"; and report each result as ONE tile with its regime, never "the capstone."
