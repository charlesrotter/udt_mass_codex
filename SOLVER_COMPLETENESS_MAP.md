# SOLVER COMPLETENESS MAP — the UDT-native solver coverage ledger

Living document (started 2026-06-16). The metacognitive "solver-architect" view
(Charles 2026-06-16): the real project is a COMPLETE, numerically-tractable,
UDT-NATIVE solver that drops NO potentially-emergent sector/effect/operator and is
honest about its regime of validity. Every result is ONE TILE here, with a regime
stamp, next to the still-blank sectors. Update at every push. Append-style; correct
statuses as coverage changes.

LEGEND: [V]=solved native + blind-verified · [v]=solved/validated (lighter) ·
[R]=solved but REDUCED (scoped) · [E]=examined separately · [ ]=untested ·
[!]=known blind-spot/open.

---

## *** 2026-06-19 POST-POSTULATE RE-CAST — THIS MAP IS NOW THE INSTRUMENT FOR THE EVERYTHING-ON SOLVER ***

Reframe (Charles, 2026-06-19): the microphysics space is UNENTERED, not walled. The status TILES in
sections A-H below were graded in the pre-postulate / contaminated-solver / catalog-hunt frame; they are
**RETIRED AS VERDICTS** (do not cite as blocking; NEGATIVES_REGISTRY wholesale-retirement banner) but
**RETAINED AS TOOL-STATE / COVERAGE info** — what code touched what, and how cleanly. The TEN COMPLETENESS
CRITERIA and the STANDING QUESTIONS (below) are the timeless bones and are unchanged. The CURRENT HEADLINE
and FRONTIER POINTER sections at the bottom are SUPERSEDED (marked there).

The map's job now: make the SOLVER-FIRST discipline operable. Before trusting any result we must SEE which
DOF/term/coupling is on/off/frozen/never-built — so a mismatch-with-observation indicts the solver's
COMPLETENESS first (Charles's four questions: left-out term? numerics? frozen/forgotten DOF? unexplored
solution space with everything on?), never a missing mechanism.

### THE EVERYTHING-ON STANDARD vs CURRENT TOOL STATE (from the 2026-06-19 solver-source recon)

Postulates are INCORPORATED STRUCTURE (not targets): i = the S^2 area form (native); spin-1/2 = the
area-form Maslov index; hbar-quantization acts on the CONTINUOUS solution family; statistics. No SM import.

| Component | EVERYTHING-ON target | Current state | Cleanest providing code | Gap to close |
|---|---|---|---|---|
| Einstein kernel | general 4x4, off-diag + time live | CLEAN, general, validated 2.7e-15; time slot present but ZEROED by choice | `whole_metric_3d_core.py` | turn on the d_t g row |
| **Residual wiring** | field eqns use the GENERAL Einstein | **P1 DONE (verified, main 443abc9): wired via pole-stable HYBRID G_full=G_weyl+[einstein_mixed(full)-einstein_mixed(diag)]; off-diagonals genuinely reach + back-react on the field equations. CAVEAT: hybrid has a FINITE regime — err~0.5*A off-diag, ~A^2 diagonal; trustworthy for small shear A<~0.1, strong shear needs P5's true general Einstein** | p1_residual_general_einstein.py | (small-shear OK; P5 for strong shear) |
| Matter stress | general 4x4 L2+L4 | CLEAN, general, exact (4.2e-17) | `whole_metric_3d_matter.py` | wire a(phi) weight (below); S^2 carrier |
| Carrier | S^2 area-form (pi_2), Theta FREE | symbolic derivation CLEAN; node-core EL CLEAN but only 1-D RADIAL | `coupled_tl_s2_derive.py`, `coupled_tl_stage1a.py` | generalize Theta-free node EL to 3-D (r,th,ps) |
| Theta core BC | native regularity node, value free | CLEAN (the ONLY no-Skyrme code) | `coupled_tl_stage1a.py` | port to 3-D spectral field |
| **Matter coupling a(phi)** | a(phi) a FUNCTION (=-1 where tested, departs at extremes) | **CONTAMINATED EVERYWHERE: silently a=-1 (GR) in every solver; a(phi) lives only in symbolic side-scripts (`a_function_both_extremes.py` etc.), never wired in** | (none in-solver) | **insert e^{(a+1)phi} weight into action measure + stress** |
| Metric warps A,B | A,B independent (NOT B=1/A injected) | CLEAN — B=1/A genuinely FREE across the modern stack (#55 scar ABSENT) | full3d / radial_Bfree / coupled_tl | — |
| Off-diagonals (spatial) e_rt,e_rp,e_tp | live (shear) | P1 DONE: live unknowns, validated (round recovers to floor, off-diag stay ~0). OBSERVED: static native matter sources e_rp,e_tp~0; e_rt~1.3e-2 NOT yet shown to be a grid artifact (verifier: flat vs Nth for resolved l=2 = possible genuine geometric response) — do NOT bank "round has zero physical off-diagonal content" until higher-Nth re-solve. SCOPED: matter EL still blind to off-diagonals (P2) | p1_residual_general_einstein.py | P2 (matter EL sees full metric) + higher-Nth re-solve |
| Off-diagonals (rotation) g_tps | live (frame-drag / angular momentum) | time-row off-diagonals NOT yet wired (P4); #63 (bare vacuum carries none) does not apply with matter | whole_metric_3d_core (capable) | P4 (time live) |
| Time | live (open-time, harmonic balance / evolution) | only a ROUND breathing-mode proxy (coupled_tl_timelive) + a fixed-bg eigensolve; no non-round time-live coupled solve | (none full) | build on the kernel's time slot |
| Non-round spatial (l>=2) | live with everything else | off-round COUPLED solve does NOT converge at production grid (#60 conditioning wall) | full3d_newton (anchor only) | research-grade preconditioned/Newton-Krylov upgrade |
| Seal / finite cell | reflecting time-live boundary | DESIGNED only (time_live_bare_solve_DESIGN.md), not implemented | — | build |
| Deep core | honest (phi->-inf, not a 0.05 cutoff) | FD 1/r^2 strain; body+bulk trustworthy, core excised | — | log/geometric grid or analytic core |
| Driver | scales to off-round coupled at clean floor | dense-Newton clean + proven ~1e-13 SMALL grid; does NOT scale off-round | `full3d_newton.py` (correctness ANCHOR) | preconditioned/Newton-Krylov or sparse-direct upgrade |
| Discretization/observables | spectral + divT gate + M_MS | CLEAN | full3d_spectral, divT_excised, M_MS | — |

BOTTOM LINE (recon): tooling is ~half-way. Clean general primitives exist; THREE things are
contaminated/missing everywhere — a(phi) frozen to -1, off-diagonals built-but-unwired, native Theta-free
EL only 1-D — plus the off-round driver needs a research-grade upgrade (dense-Newton is the anchor, not the
engine). Build order is in POST_POSTULATE_PROGRAM.md.

---

## A. METRIC DEGREES OF FREEDOM (the 10 components)   [tiles below = TOOL-STATE/coverage, RETIRED as verdicts]
- [V] g_tt, g_rr diagonal warps, B=1/A FREE (independent) — radial #56 (blind-verified);
      2-D axisym spectral #59.
- [v] g_θθ, g_ψψ angular metric — carried in 2-D spectral #59 (axisym).
- [E] time-row / shear off-diagonals g_tr, g_tθ, g_rθ — #57 found them LINEARLY
      DECOUPLED on the round background; NOT solved nonlinearly with structure. [!] partial.
- [ ] rotation / twist off-diagonals g_tψ, g_rψ, g_θψ (angular momentum) — UNTESTED. [!]

## B. COORDINATES / DIMENSIONS (t, r, θ, ψ)
- [V] r (radial) — #56.
- [v] θ (polar) — 2-D spectral #59.
- [v] ψ (azimuth) — OPENED (#60, full3d_catalog_results.md): Fourier-ψ spectral
      basis machine-exact; the ROUND #56 soliton recovered in the full-3-D (ψ-live)
      basis (M_MS=0.281, gate PASS). Criterion-4 ψ-DOMAIN now covered for the round
      solution. (OFF-ROUND ψ-shaped solve = solver-limited, see F / 8.)
- [E] t (time) — STATIC solved; time-periodicity SELECTOR examined #57 (seal = interval,
      not a circle; ω₁ depth-flat ⇒ no classical selector). Fully-dynamic evolution [ ].

## C. MATTER (winding field n, charge m, depth p)
- [V] Θ(r) radial profile — #56.
- [v] Θ(r,θ) angular shape, matter FREE — 2-D spectral #59 (charge-1, axisym; corrected EL).
- [v] winding m=1 — ground state, round (spherical).
- [R] winding m=2,3 — found grid-stable (#52d/#57d); 3-D EL now carries winding m
      (matter_el_3d_gen.py, correct), seeds built (#60) but shapes/masses NOT mapped
      — OFF-ROUND solve solver-limited (#60). Still [R].
- [ ] winding m≥4 — seed built (#60) but solver-limited; UNMAPPED.
- [V] depth p (dilation) — continuous family, super-exponential M(p), NO native selector
      (#54/#56; the lepton-relevant same-charge axis).

## D. ACTION TERMS
- [V] L2 (two-derivative) — settled, audited clean.
- [V] L4 (Skyrme stabilizer) — settled; radial EL correct (#56). [!] the 2-D off-round L4
      EL had a BUG (axisym_matter_el.py, found by verifier 7cf94053) — corrected
      (axisym_matter_el_CORRECT.py); the 3-D EL must be generated correct (div-identity test).
- [V] seal / boundary (same-minus = time-reversal) — radial/2-D.
- [V] κ8 back-reaction coupling — FREE dial; over-collapse existence ceiling κ8*(p),
      NON-critical (Path 2, #52); criticality conjecture NOT supported in this regime.

## E. DYNAMICAL REGIME
- [V] static (∂_t=0).
- [ ] stationary rotating/twist (g_tψ etc.) — UNTESTED. [!]
- [E] time-periodic — examined #57 (no classical selector; closed-time hinge underived).
- [ ] fully dynamic (NR-grade evolution) — NOT attempted. [!]

## F. SYMMETRY SECTOR
- [V] spherical (charge-1 ground state).
- [v] axisymmetric (r,θ) — 2-D spectral #59.
- [R] NON-axisymmetric (ψ-dependent; platonic types) — OPENED (Phase 3/3b, 2026-06-16/17):
      the off-round solver (full3d_newton, category-A) + SH-exact θ grid (full3d_grid_shexact)
      make non-axisym solves converge; m>=2 round is UNSTABLE and lower non-axisym (toroidal/
      axial) critical points exist (m=2 toroidal l=2,4 = Skyrme B=2; m=3 axial, NOT tetrahedral),
      coupled-stable along steepest tested modes. BUT grid convergence (Phase 3b) shows the m>=2
      GROUND-STATE MASS is NOT converged (M_MS(2) ranges 9.8-38.5; residual-Newton lands on
      different critical points per grid) ⇒ m>=2 masses/shapes UNSETTLED, not banked. Catalog of
      SECTORS exists; the m>=2 ground STATES need an energy MINIMIZER + continuation to pin.
      Residual: that minimizer; full off-diagonal METRIC; full S³ matter map; higher m.

## G. SCALE REGIME
- [V] shallow ↔ deep φ — radial to p≈6 (#56); bulk swept to p≈-40 pre-L4 (#39).
- [V] weak ↔ strong κ8 — to the over-collapse ceiling (#52).

## H. QUANTUM-APPEARING OBSERVATIONS (no separate quantum SECTOR presumed — Charles 2026-06-16)
NOTE: do NOT reify "the quantum sector" as a place things live — that reifies the quantum
framework (an import). Treat quantum-APPEARING observations as TARGETS the geometry may resolve
(standing waves / eigenvalue / topology). Discreteness is NOT inherently quantum (a vibrating
string, any bound-state eigenvalue problem, is classically discrete; cf. Couder-Fort droplets).
The UDT/QCD-QED overlap is with their GEOMETRIC/CLASSICAL face (gauge=connection; Skyrmion=classical
soliton; large-N QCD is classical) — coherent with no quantum layer. [[no-presumed-quantum-sector]]
- [E] fermion/spin-½ statistics — #51/#53 (classically not forced) used RETIRED SM-imports (Skyrme/
      FR/WZW), so they do NOT count as a native test; native verdict UNWRITTEN. A geometric realization
      (topology / standing-wave) is the open target, not "a quantum sector".
- [ ] discrete spectra (atomic/hadronic) — a STANDING-WAVE/eigenvalue extension of the solver (we
      already compute mode ω²); the cleanest test of geometric discreteness. UNTESTED at scale.
- [!] PRECISION-loop physics (g−2, Lamb shift, DIS, running coupling) — the hard BILL; needs a
      DYNAMICAL/response solver (not the static one) + the reverse-engineer-from-quantum-math strategy
      (stochastic quantization / Madelung / ℏ-loop / effective action / RG↔DILATION first). UNTESTED.
- [!] entanglement / Bell nonlocality — the deepest test of "all geometry"; UDT's global coupling
      may have the resources Bell's locality assumption forbids. UNTESTED.

## TRACTABILITY MAP (what the numerics reach)
- TRACTABLE NOW: 1-D radial coupled Einstein+L2+L4 (#56); 2-D axisym SPECTRAL coupled solve
      (Cheb_r × Legendre_θ), exponential convergence, matter free (#59). Continuation (depth).
- OFF-ROUND WALL BROKEN (Phase-2, 2026-06-16, off_round_solver_results.md): the OFF-ROUND
      coupled SOLVE now CONVERGES via an explicit-Jacobian Newton/LM (full3d_newton.py) —
      value-equivalent to the committed residual to 1.4e-14 (category-A), round floor 3.8e-13
      with the ANGULAR Einstein eqns satisfied (~1e-8), B=1/A FREE (maxB1A=0.14), continuation
      working. The #60 "solver-limited / INCONCLUSIVE" gate is REMOVED. CAVEATS: a perturb-and-
      relax off-round probe RELAXED BACK to axisym (NOT a catalog member — expected null, not a
      verdict); M_MS≈0.289 at gate grid (the prior "0.281" partly conflated radial-grid res);
      INFRA-AUDIT #2 corrected #60's "machine-zero round gate PASS / div(T) exact" — round
      recovery was ~1% (radial slice never imposed θθ) and the committed div(T) gate was broken
      (now fixed: divT_excised.py). SH-exact θ op (sh_theta_operator.py) built for m≠0 winding,
      NOT yet wired into a coupled solve. The non-axisym / higher-winding catalog SEARCH itself
      (criteria 6/8/9) is now TRACTABLE but UNRUN — Phase 3.
- PRIOR #60 framing (superseded by Phase-2 + INFRA-AUDIT #2): "full-3-D round gate PASS at
      machine zero, div(T) ν=r exact, M_MS=0.281" — corrected above; the round solution is real
      (M_MS≈0.289 grid-dependent) but the machine-zero/div(T) claims were overstated.
- NOT YET BUILT: fully-dynamic (time-evolution) NR-grade solver; the quantum-sector machinery.
- TOOLING CORPUS being mined (category-A, NR): spectral elliptic methods, self-consistent-
      field (KEH/Hachisu), gravitating-Skyrmion/boson-star solvers, pseudo-arclength continuation.

## THE TEN COMPLETENESS CRITERIA (the mathematically-complete governing set;
## refined 2026-06-16 from Charles's "sectors/effects/operators" — his words map as
## operators→2; sectors→4,6,7; effects→8,9). A variational field theory's FULL solution
## space is exhausted iff all ten are covered. Each push declares its status on each.
## LAYER 1 — what you're solving:
##  1. FIELDS (every varying DOF: 10 g_μν + matter + φ).
##  2. ACTION TERMS (every term: L2,L4,gravity,seal/boundary) — the "operators".
##  3. FULL EQUATIONS (every variation of every field — NEVER a subset; the #55 scar).
##  4. DOMAIN & COORDINATES (r,θ,ψ,t live unless a STATED symmetry; the 2-D-in-4-D scar).
##  5. BOUNDARY & REGULARITY (seal, center/axis, finite cell — they SELECT solutions).
## LAYER 2 — which world:
##  6. TOPOLOGICAL SECTOR (winding/charge m — each a disconnected world).
##  7. DYNAMICAL CHARACTER (sit=static / spin=stationary / ring=time-periodic / evolve=dynamic;
##     elliptic vs eigenvalue vs hyperbolic; the time-selector lives in "ring").
## LAYER 3 — what emerges:
##  8. BRANCH / BIFURCATION STRUCTURE (are there OTHER disconnected solutions? = the CATALOG).
##  9. STABILITY SPECTRUM (which solutions persist; a "particle" = a STABLE solution).
## 10. REGIME OF VALIDITY (scale/coupling range; where the math changes character).

## STANDING COMPLETENESS QUESTIONS (run every push)
1. For EACH of the ten criteria: what does this push cover, and what does it DROP (explicitly)?
2. Could any DROPPED criterion host emergent structure? If yes ⇒ flagged blind-spot, not a closure.
3. State the REGIME OF VALIDITY (criterion 10) of the result.
4. Is every technique category-A (conditioning) — not category-B (physics simplification)?
5. What tooling/tractability step covers the dropped criteria next?
6. (anti-inflation) This is ONE tile — how much of the ten-criteria space is still blank?

## CURRENT HEADLINE  [SUPERSEDED 2026-06-19 — the winding-catalog frame is RETIRED/unentered; see the POST-POSTULATE RE-CAST banner near the top + POST_POSTULATE_PROGRAM.md. Text below is history.] (updated 2026-06-17 — Phase 3 + 3b, honest after grid convergence)
UDT carries a discrete catalog of topologically-protected winding (charge) SECTORS (m=1,2,3 all
converge — winding_catalog_verified_results.md, winding_platonic_phase3b_results.md). m=1 = round
STABLE hedgehog, grid-stable M_MS~0.29-0.30 (matter Hessian n_neg=0; coupled-stable). For m>=2 the
round state is UNSTABLE and lower NON-axisymmetric (toroidal/axial) critical points exist and are
coupled-stable along the steepest tested modes AT A GIVEN GRID. m=2 reads toroidal (l=2,4 = Skyrme
B=2 analog), m=3 axial (NOT tetrahedral). KEY CAVEAT (Phase 3b grid convergence): the m>=2 GROUND-
STATE MASS is NOT converged — M_MS(m=2) ranges 9.8-38.5 across grids and residual-Newton lands on
DIFFERENT critical points per grid, so masses/shapes for m>=2 are UNSETTLED (the "M~13.4" was grid-
specific). The angular sector overlapping Skyrme/QCD (toroidal m=2) is suggestive, not numerically
banked. METHOD lesson [[gravitating-soliton-stability-test]]: fixed-metric matter Hessian over-counts
instabilities (off-constraint); use coupled re-solve. TOOL GAP: residual-Newton finds arbitrary
critical points; pinning m>=2 stable ground states (= the particles, global minima) needs an ENERGY
MINIMIZER + continuation. Only m=1 is a clean, grid-stable, confirmed ground state.

PRIOR milestone (stands): UDT NATIVELY PRODUCES MASS (#56): a self-consistent full-(radial)-Einstein
soliton, no imports. NO classical discrete catalog YET found in the genuinely-searched
CHARGE-1 STATIC AXISYMMETRIC matter-deforming tile (#59). The full-3-D spectral build
(#60) now has the CORRECT, POLE-STABLE 3-D MACHINERY (analytic Einstein, correct off-round
matter EL, Fourier-ψ) and RECONFIRMS the round soliton in the 3-D ψ-live basis (gate PASS,
M_MS=0.281) — but the NON-AXISYMMETRIC + HIGHER-WINDING catalog SEARCH is SOLVER-LIMITED
(off-round coupled-solve convergence gap; the axisym control #59 relaxes does not relax
cleanly here), so that catalog home is still OPEN (NOT banked, not a negative). The gap is
now isolated to OFF-ROUND 3-D SOLVE TRACTABILITY (the next build), not the physics content.
Time-dynamic, rotation/twist, full-off-diagonal-metric, full-S³-matter, and quantum
sectors remain open.

## STANDING-QUESTION ANSWERS — push #60 (full-3-D spectral)
1. COVERS: criteria 1-5 for the diagonal-Weyl/single-Θ 3-D class incl. ψ (criterion-4
   OPENED, round gate). DROPS (explicit): spatial off-diagonal metric g_rθ/g_rψ/g_θψ;
   full S³ matter map (F,G,H) [single-Θ is restricted non-axisym]; twist (crit-7);
   off-round CONVERGENCE for crit-6/8/9.
2. Could a dropped criterion host structure? YES — the non-axisym catalog (crit-8) and
   winding shapes (crit-6) are exactly what could not be searched ⇒ flagged blind-spot,
   NOT a closure. The off-diagonal metric + full S³ map are the most likely missing DOF.
3. REGIME: validated machinery + round gate basis-robust at (p=0.4, kap8=0.05, 14L). The
   off-round search has NO established regime (did not converge).
4. Category-A? YES — every technique conditioning, proven (flat/Schwarzschild/round/2-D-
   match/machine-zero EL/div-identity). NO category-B. The honest limit is SOLVER speed.
5. Tooling next: a faster off-round 3-D solver (dense-LM on a moderate grid / Newton-
   Krylov with an elliptic preconditioner / metric-matter block SCF) to drive off-round
   to a clean floor (Phi~1e-9 with the axisym control round-recovered), THEN re-run the
   non-axisym + winding search.
6. ONE tile: the 3-D non-axisym/winding CATALOG verdict is still BLANK; what is newly
   filled is the 3-D ROUND recovery + the correct 3-D physics machinery.

## FRONTIER POINTER  [SUPERSEDED 2026-06-19 — closed-time selector was a catalog-mechanism target, now RETIRED; the frontier is the everything-on clean solve, see the top banner + POST_POSTULATE_PROGRAM.md. History below.] (2026-06-17 LATER) — the CLOSED-TIME selector (criterion 7, "ring")
Cross-session recon + audit (cross_session_recon_2026-06-17.md) sharpened the next target. The STATIC
sectors are now well-covered/closed: criteria 1-6,8,9 for the winding catalog (m=1 stable; m>=2 non-axisym
coupled-stable; absolute masses NOT grid-convergeable = a tooling negative); criterion-8/9 single-cell
fluctuation SPECTRUM = BOX-CONTROLLED (audited) -> NOT the lepton family. THE OPEN HIGH-VALUE TILE is
criterion 7 DYNAMICAL CHARACTER = "ring" (time-periodic / CLOSED-TIME / non-stationary), done PROPERLY
(full dynamical, not static-linearized #57). THREE threads converge there: lepton mass FAMILY
(generations), the native de Broglie WAVE, and the quantum "i" (all = ONE missing input: the rest
clock/hbar/flowing-phase). SM-assumption lens [[udt-derives-sm-assumptions]]: a win there derives "why QM
is complex" (the i = S^2 area form) + the dynamics. Tile H (quantum-appearing observations) is downstream
of this. Reusable for any deep-phi spectral work: the branch's exact fluctuation operator + mpmath
log-grid dps>=50 (float64 garbage in deep-phi).
