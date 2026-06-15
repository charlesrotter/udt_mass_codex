# MAP — The WHOLE-METRIC Solve (unreduced; premise ledger for Charles's eye)

Authored 2026-06-15, BEFORE any solve. This is the cheap catch-surface: every
metric degree of freedom, every choice, tagged — so a smuggled freezing is caught
HERE, not after a build. Charles steers at the assumption stage.

## Why this exists (the catch)
Charles (2026-06-15): the "complete-metric sweep" (#52/#54) was the complete
ACTION on a REDUCED metric — static, diagonal, spherically symmetric, areal ρ=r,
the angular field a radial profile Θ(r). "Complete action" ≠ "complete metric." A
depth-SELECTOR (and shaped types, and discreteness) may live in the metric DOF we
froze. We have NEVER solved the metric unreduced. THIS DOES IT — and Charles's
standing note: getting it right may OVERTURN a lot of prior results (see §9).

## 1. Geometry, coordinates, and the ONE flagged symmetry
- Cell = a FINITE domain (finite-cell canon; no spatial infinity). Coordinates
  (t, r, θ, ψ), ψ = azimuth about the winding axis.
- SYMMETRY (the one spatial reduction, made VISIBLE — chose, justified): the winding
  field selects an axis; we take AXISYMMETRY about ψ (fields depend on (t,r,θ)).
  This is the natural symmetry of a winding soliton, NOT the old slicing. FLAG: it
  IS still a reduction from full (t,r,θ,ψ); non-axisymmetric (multi-lobe) configs
  are a named FURTHER step, and the solution must be tested for spontaneous
  ψ-breaking before axisymmetry is trusted as the ground state.
- This is the minimal, honest reduction. EVERYTHING ELSE stays live.

## 2. THE UNKNOWNS — all metric DOF LIVE (the anti-freezing list)
General axisymmetric metric on (t,r,θ), 10 components, NOTHING pre-set to zero:
- DIAGONAL warps: g_tt, g_rr, g_θθ, g_ψψ. [derived unknowns]
- "ELECTRIC" off-diagonals (the time-row / shear — the #38 medium-edge, frozen in
  every prior soliton solve): g_tr, g_tθ, g_rθ. [derived unknowns — KEY new DOF]
- "MAGNETIC" off-diagonals (rotation / frame-dragging / twist): g_tψ, g_rψ, g_θψ.
  [derived unknowns — g_tψ = angular momentum, also never in a soliton solve]
MATTER: the unit 3-vector n (target S², 2 functions — profile Θ and internal phase
χ), full (t,r,θ) dependence, winding m about ψ. [derived]
φ: NOT an independent field — read from g_tt via the tie φ=−(1/2)ln(−g_tt). NOT
slaved, NOT imposed. [derived/definitional]
=> 10 metric + 2 matter functions of (t,r,θ), minus gauge (§6). The prior radial
sweeps were the special case g_tr=g_tθ=g_rθ=g_tψ=g_rψ=g_θψ=0, g_θθ=ρ², ρ=r,
∂_t=0, χ=χ(r) — TWO-THIRDS of the metric set to zero. We unfreeze ALL of it.

## 3. THE EQUATIONS — one coupled system, solved simultaneously
- EINSTEIN: G_μν = κ₈ T_μν[n,g], 10 coupled equations, T from the settled action
  L2+L4 (every T_μν component, incl. the off-diagonal momentum/shear pieces the
  reduced T never had). NO term added, NO sector slaved.
- MATTER: the Euler-Lagrange equation for n from L2+L4 on the FULL metric (not the
  hedgehog-reduced profile equation).
- ∇_μ T^μν = 0 (Bianchi) — automatically consistent; a check, not an extra input.
- STRUCTURE (3+1 / ADM split — the GR corpus hands us this, charter principle 4):
  the 10 Einstein eqs = 4 CONSTRAINT (elliptic: Hamiltonian + 3 momentum) + 6
  EVOLUTION (hyperbolic in t). Two realizations of the ONE whole-metric problem,
  both with EVERYTHING live (this is build-up of solver CAPABILITY, not reduction
  of physics):
  (A) STATIONARY soliton (∂_t=0 in the adapted gauge): the whole system collapses
      to a coupled ELLIPTIC 2-D system in (r,θ) for ALL potentials incl. g_tψ
      (rotation) and g_tθ/g_rθ (time-row/shear). This is the full whole-metric
      static soliton — one simultaneous solve. (Standard for rotating star /
      spinning boson-star codes — mine it.)
  (B) TIME-PERIODIC config (the SELECTOR hunt): harmonic/breather time dependence
      => the SAME (r,θ) system becomes an ELLIPTIC EIGENVALUE problem; only special
      configs close up periodically => a DISCRETE spectrum. This is where a native
      discrete-DEPTH selector would appear — as an eigencondition on the whole
      metric, in the same simultaneous solve, NOT a staged afterthought.

## 4. THE SEAL & THE TIME-TOPOLOGY HINGE (the decisive open question)
- Seal: the same-minus MIRROR FOLD = time reversal at the interface D=0 (w6/#42),
  imposed as a boundary condition on the FULL metric (incl. how it acts on the
  off-diagonal/time-row components — this is new; the seal's action on g_tθ/g_tψ
  was never computed).
- Regularity on the winding axis + at the center; finite-cell outer condition.
- THE HINGE: does the finite-cell canon CLOSE TIME into a circle? (HANDOFF open
  hinge, never resolved.) If YES => time-periodicity is FORCED => realization (B)'s
  eigencondition is mandatory => discreteness is native. If NO => time is an
  interval => (B) is optional. This single topological fact may be the whole
  selector. The whole-metric solve must DETERMINE it, not assume it.

## 5. (folded into §3/§4)

## 6. THE GAUGE — the one unavoidable CHOICE (flagged, not smuggled)
A general metric carries 4 coordinate freedoms; a chart MUST be fixed to solve.
- CHOSE: a generic canonical form (Lewis–Papapetrou / quasi-isotropic class) that
  fixes the gauge while keeping ALL physical DOF free.
- TRIPWIRE: do NOT pick a DIAGONAL gauge (re-freezes the off-diagonals = the exact
  slice we're escaping). Do NOT impose ρ=r as a gauge (it was a THEOREM only for
  the reduced class; under the whole metric it must be a RESULT or a flagged
  choice, never silently re-imposed).
- DISCIPLINE: prove the chosen gauge is non-restrictive (counts physical DOF;
  recovers the reduced solutions as a special case) BEFORE trusting any result.

## 7. PREMISE LEDGER (consolidated — chose or derived?)
| Item | tag |
|---|---|
| Action L2+L4+seal, two-way φ | DERIVED (this arc) |
| Target S² (real n) | DERIVED (#50) |
| Axisymmetry about the winding axis | CHOSE (justified; non-axisym = flagged further step; test for spontaneous breaking) |
| ALL 10 metric components live | DERIVED-unknowns (the un-freezing) |
| φ read from g_tt (tie), not slaved | DERIVED/definitional |
| κ₈ (back-reaction) value | OPEN (#52: free dial w/ over-collapse ceiling; criticality a conjecture — TEST BOTH still) |
| Gauge (canonical, non-diagonal) | CHOSE (flagged; proven non-restrictive) |
| ρ=r | NOT imposed — let it be a result |
| Seal = time-reversal fold BC on full metric | DERIVED (w6/#42); its action on off-diagonals = NEW, to compute |
| Time closed to a circle? | OPEN HINGE — to be DETERMINED, the likely selector |
| Stationary first, then time-periodic eigencondition | CHOSE (solver capability build-up, both with all DOF live — NOT physics reduction) |

## 8. READ-OUTS (DATA-BLIND — in √(κ/ξ) units; no wall numbers, no comparison)
Existence + COUNT of distinct stable whole-metric solutions; shapes (now the
metric can be shaped, not just the field); bifurcations; M_MS; charge (Q=2p_F, q);
angular momentum (g_tψ); and — the headline — whether the UNREDUCED metric (off-
diagonal + time-periodicity) produces DISCRETE structure / a depth-SELECTOR / shaped
types that every reduced solve could not. Both outcomes first-class.

## 9. THE OVERTURN LIST (Charles: "may overturn a lot")
These banked results are SCOPED to reduced metrics; if the whole-metric solve shows
structure, each is CONDITIONS-CHANGED (loses blocking authority until re-graded):
- #34 / #39 (whole-metric bulk = one round continuum) — diagonal, reduced angular,
  NO off-diagonal/time.
- #52 (complete-action sweep = one round charge-1 continuum) — static, diagonal,
  spherical, ρ=r.
- #54 (micro mass-shape: depth a continuum, NO native selector) — same scope; "no
  selector" is EXACTLY what realization (B)/the time-row revisits.
- Single-cell discreteness "exhausted" (#40 cohomological, #41 dynamic, #44
  breathing-tower) — reduced/diagonal/single-sector.
- #47b spin-structure HINGE — if the off-diagonal/time-row sector re-grades omega_H1
  σ-ODD, the global-spinor/fermion route REOPENS (CONDITIONS-CHANGED trigger). The
  whole-metric solve directly touches this.
- (Watch) the fermion negatives #51/#53 rest partly on the reduced classical content;
  if the whole metric carries new structure (rotation g_tψ, time-row), re-examine.
NOTHING here is deleted — it is FLAGGED pending re-grade under the unreduced solve.

## 10. EXECUTION (the solve, after Charles signs the MAP)
1. ASSEMBLE the exact unreduced system symbolically (the full T_μν[L2+L4] in all
   components; G_μν in the canonical gauge; the n EL) — VERIFIED (independent
   re-derivation) before any numerics. Recover the reduced sweep as a special case
   (gauge/DOF sanity check).
2. SOLVE realization (A): the full STATIONARY whole-metric soliton (coupled 2-D
   elliptic, all DOF live) on the V100. Map the solution space; compare to the
   reduced #52 result (does freeing the off-diagonals/angular metric change "one
   round knot"?).
3. SOLVE realization (B): the time-periodic eigencondition; DETERMINE the time-
   topology hinge; hunt the native depth-selector.
4. Verifier-before-record at each stage; re-grade the §9 overturn list per results.

## Discipline
DATA-BLIND; OBSERVE not target; verifier-before-record (independent machinery);
GPU V100 torch float64 (CLAUDE.md pitfalls); principle 1 (no imported mechanism —
the GR corpus is transformed, not imported as new physics); principle 2 (sanctioned
Taylor OK, no linearization-as-result); NOTHING canonical without Charles. GET IT
RIGHT: the gauge proven non-restrictive, the reduced limit recovered, every DOF
accounted, before any result is trusted.

## Genuine difficulties (honest — where this can go wrong)
- The off-diagonal components (g_tθ, g_rθ, g_tψ...) are routinely GAUGED AWAY in
  standard codes; keeping them physical requires care that the gauge fix doesn't
  silently kill them. This is the #1 place to get it wrong.
- Mixed elliptic (constraint) + hyperbolic/eigen (time) character — the constraints
  must be satisfied, not just the evolution.
- The seal's action on the full component set is uncomputed; a wrong seal BC on the
  off-diagonals would fake or kill structure.
- Convergence of a coupled 2-D nonlinear elliptic system needs a good initial guess
  (continue from the reduced solution) and the independent-solver cross-check.
