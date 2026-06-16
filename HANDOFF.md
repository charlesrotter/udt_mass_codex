# HANDOFF — Resume Instructions and Perspective

(Refreshed 2026-06-16. The prior HANDOFF described the quantum-completion / coin-flip
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
4. THE CATALOG QUESTION — does UDT carry a DISCRETE CATALOG of distinct stable types, or
   just one round family (which carries mass)? Charge-1 static axisym matter-free search
   (#59): NO disconnected type (blind-verified; a real off-round L4 EL bug was found + the
   null survived it). The full-3-D spectral run (#60) then BUILT + VALIDATED the full-3-D
   machinery (round soliton recovered in the ψ-live basis, gate PASS, M_MS=0.281) but the
   OFF-ROUND search is SOLVER-LIMITED (the matrix-free Jacobi-PCG iterative solve won't
   converge off-round) ⇒ INCONCLUSIVE, catalog STILL OPEN. Net: every STATIC search to date
   returns a CONTINUUM / one round family / no catalog.
5. *** THE NEW PERSPECTIVE (2026-06-16) — the catalog may be a DYNAMICAL SPECTRUM, not
   static cells *** ([[particle-catalog-frame]] sharpening). Discreteness in nature is
   typically STANDING-WAVE / SPECTRAL (atomic spectra = eigenvalues of a wave equation, not
   a catalog of static lumps). The lepton-relevant axis (DEPTH) is a CONTINUUM with NO STATIC
   selector (#54/#56) — exactly the setup where a standing-wave / EIGENVALUE condition imposes
   discreteness. So the lepton FAMILY may be the discrete EIGENMODES of one continuous depth
   family (DYNAMICAL) — living in an EIGENVALUE / standing-wave solver we have NOT built. The
   static nulls then become EVIDENCE pointing there, not failures. This converges with the
   quantum reframe (#6), the #57 time-periodicity selector (only ever probed via STATIC
   linearized modes — not closed), and RG↔dilation. CAVEAT: the static catalog is NOT closed
   (off-round #60 is solver-LIMITED, not a clean null), so this is a leading hypothesis, not
   established.
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
- full-3-D spectral (Chebyshev_r × Gauss-Legendre_θ × Fourier_ψ): primitives + analytic 3-D Weyl
  Einstein (pole-stable: flat=0, Schwarzschild exp, 2-D-match 1e-14) + CORRECT 3-D matter EL
  (machine-zero on round, div(T) exact) — BUILT, internally VALIDATED (#60; round gate PASS,
  M_MS=0.281). ⚠ NOT independently verified/audited (the #60 run was INCONCLUSIVE and its final
  summary was lost to an API error) — AUDIT/VERIFY THIS before relying on it for a real search.
  REMAINING WALL: the OFF-ROUND coupled SOLVE is solver-limited (matrix-free Jacobi-PCG too weak).
  FIX (category-A conditioning, next session): block-SCF/KEH + continuation-from-round + a real
  elliptic/block preconditioner (or coarse dense spectral grid). See SOLVER_COMPLETENESS_MAP tractability.
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
4. NEGATIVES_REGISTRY.md #55/#56/#57/#58/#59/#60 (+ the results docs as needed:
   whole_metric_solve_3D_results, radial_Bfree_soliton_results, spectral_catalog_solver_results,
   full3d_catalog_results).
5. CANON.md (C-2026-06-14-1 + its EOS-softening refinement — SURVIVES the overturn).

## QUEUE / next-session frontier (the 3-D run LANDED = #60, INCONCLUSIVE / solver-limited)
1. FIX THE OFF-ROUND 3-D STATIC SOLVER (category-A conditioning only) to CLOSE the static-catalog
   question: BLOCK-SCF/KEH (alternate metric-solve / matter-solve, each well-conditioned) +
   CONTINUATION from the already-converged round #56 soliton + a real elliptic/block PRECONDITIONER
   (or a coarse dense spectral grid). Then run the non-axisym + higher-winding search; a winding-3 /
   platonic stable type may be the geometric BARYON (data-blind shape/mass/stability). Verifier-first.
2. *** SCOPE / BUILD THE EIGENVALUE / STANDING-WAVE (DYNAMICAL) SOLVER *** — per the NEW PERSPECTIVE
   (big-shift #5): this may be WHERE THE FAMILIES ACTUALLY LIVE (discrete EIGENMODES on the depth
   continuum), not the static catalog. It's a natural extension of the breathing-mode (ω²) machinery,
   and it's the #57 time-periodicity selector done PROPERLY (full dynamical, not static-linearized).
   Arguably the higher-value build for the mass-pattern observation. (Both 1 and 2 are complementary:
   1 closes the static door cleanly; 2 opens the door the evidence points at.)
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
the complete native solver (now: a static one that works to 2-D/round-3-D, plus a dynamical/eigenvalue
one to build); audit it constantly; let structure emerge; match observations; never patch a "no" into
a "yes"; and report each result as ONE tile with its regime, never "the capstone."
