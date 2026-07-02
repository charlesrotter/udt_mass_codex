# MAP — the minimally-free f(r,θ) finite-mirror cell (Class A, 2-D build)

**Mode:** MAP (no compute). **Author:** Claude (claude.ai session, 2026-07-01), for Charles's
inspection BEFORE anything is built. **Frozen contract:** `discreteness_preregistration.md`
(Class A: closed topological cell modes). **Foundation:** the five derived native-frame docs +
`round_matter_reduction_results.md`. **Purpose:** state the frame WHOLE, put every chose on the
table, and locate — structurally, in advance — where isolation can and cannot come from, so a
scan result (either way) is readable and not over- or under-claimed.

Three NEW analytic observations are flagged **[OBS-1..3]** below. None is banked; each needs a
CAS check in the build. They are frame-level observations, not derivations.

---

## 1. THE FRAME, WHOLE (lay statement)

We have a finite spherical drum. Its skin (the outer seal) is a smooth mirror fold — nothing
leaks, so the drum's public charge is zero by construction. Inside the drum live three things:
the depth field φ(r) (how dilated time is), the size field ρ(r) (how big the angular sphere
actually is at each depth), and a knotted matter field f(r,θ) whose knot count N is a true
integer — the one discreteness the frame already owns. The rigid knot (f=θ) makes the drum
collapse; that is verified and real. The question this build asks is the modest first
pre-registered question: **if the knot is allowed to relax in r and θ, does the drum find any
stable finite size at all — and if so, does it find only certain isolated sizes?**

What would count as an answer either way is already frozen (pre-reg, 9 criteria). What this MAP
adds is the *shape of the question*: the closure conditions form a manifold in the space of
(core data × cell size), and "discreteness" means that manifold has isolated pieces or bands —
not that we forced the counting to be square. We scan the manifold; we do not sculpt it.

## 2. THE EXACT SYSTEM (from the derived frame; nothing new here)

Domain: r ∈ [r_c, r_s], θ ∈ [0, π], static, axisymmetric. Fields φ(r), ρ(r), f(r,θ).
Winding carrier n = (sin f cos Nψ, sin f sin Nψ, cos f), integer N.

Geometry (interior Branch P, round; from `cell_solver_round.py` header, CAS-verified):
    φ'' = 4 e^{−2φ} ρ'² / (Z ρ²) − 2 φ' ρ'/ρ                                  (no direct matter source: matter is φ-BLIND)
    ρ'' = 2 φ' ρ' − (Z/4) ρ e^{2φ} φ'²  +  (e^{2φ}/4)( ξ ρ I_r − κ N² I_4θ / ρ³ )
with the θ-moments of f (from `round_matter_reduction_results.md`, CAS-verified):
    I_r(r) = ½∫ sinθ f_r² dθ,   I_4θ(r) = ½∫ (sin²f/sinθ) f_θ² dθ.

Matter (2-D elliptic PDE, CAS-verified):
    ∂_r(A f_r) + ∂_θ(B f_θ) − (N² sin f cos f / sinθ)(ξ + κ f_r² + κ f_θ²/ρ²) = 0
    A = ξ ρ² sinθ + κN² sin²f/sinθ,   B = ξ sinθ + κN² sin²f/(ρ² sinθ).

Boundary conditions:
    poles:      f(r,0) = 0, f(r,π) = π                       (regularity + degree N)
    outer seal: φ'(r_s) = 0, ρ'(r_s) = 0, f_r(r_s,θ) = 0     (smooth mirror fold, Class A)
    core:       r_c > 0, ρ(r_c) = ρ_c > 0 (finite core — natively motivated: the P source
                diverges as ρ→0), plus the CORE RULE (see ledger — the load-bearing chose).

## 3. PREMISE LEDGER (every fixed thing, tagged)

| # | Premise | chose / derived | Notes |
|---|---------|-----------------|-------|
| P1 | Constrained-two-player metric form (φ longitudinal inside g; h_AB independent) | **CHOSE** (standing Risk 1) | All results scoped to this slice. |
| P2 | Static, diagonal, round h = ρ²Ω | **CHOSE** (slice) | Staged plan un-freezes later (off-round, time-live). |
| P3 | Axisymmetric ansatz: f = f(r,θ), ψ only via Nψ | **CHOSE** | "Minimally free." A null here is a null on this ansatz, not on the winding sector. |
| P4 | Matter = {L2, L4} on the S² carrier | L2 **DERIVED-unique**; L4 **DERIVED-present** (Derrick) + area-form-native; the PAIR is **CHOSE-minimal** | F2 verdict: minimal-but-not-unique. X² and L6 remain admissible extras; V(n) is FORBIDDEN (full SO(3)) absent a symmetry-reduction posit. If free-f still collapses, X²/L6 are the next in-frame freedoms BEFORE any off-frame move. |
| P5 | Matter is φ-blind; radial channel undilated | **DERIVED** (banked, blind-verified) | |
| P6 | Pole BCs f(r,0)=0, f(r,π)=π | **DERIVED** (regularity + degree) | |
| P7 | Outer seal φ'=ρ'=0 | **DERIVED** given Class A (smooth mirror fold); choosing Class A first is **CHOSE** (pre-registered) | |
| P8 | f_r = 0 at the seal | **CHOSE-conditional**: it is the natural variational BC GIVEN no seal matter term | A seal matter/source term would change it (that is Class-B territory). |
| P9 | Finite core ρ_c > 0 | **DERIVED-motivated** (P-source divergence at ρ→0, CAS note in solver header) | The SPECIFIC core rule is a CHOSE — see §4; it is the single most dangerous knob in the build. |
| P10 | Z_φ held fixed (one global value) | **CHOSE** (the open fork; standing Risk 2) | See [OBS-2]: the current Z=8 labeling needs one correction. |
| P11 | ξ = κ = 1 | **CHOSE-units** | κ breaks the vacuum scale symmetry [OBS-1] → κ/ξ sets the absolute length; only RATIOS of cell sizes are unit-free observables (consistent with the ratios-only data-blind rule). |
| P12 | N fixed integer per run | **DERIVED** (topological) | Scan N = 1, 2, 3 as separate runs. |

## 4. [OBS-1] THE COUNTING — where isolation can and cannot come from

This is the lens for reading any result. Shooting data at the core: (φ_c, φ'_c, ρ_c, ρ'_c),
plus the cell size r_s. Outer closure: TWO scalar conditions (φ'(r_s)=0, ρ'(r_s)=0); the f-PDE
with its four BCs is elliptic and generically solvable on any background, so it contributes no
generic scalar condition (but see (b) below).

- Vacuum P has an exact scale symmetry (r,ρ) → λ(r,ρ) [checked by hand from the EOMs; CAS-verify
  in build]. The ξ (quadratic) matter sector RESPECTS it (f_r² scales as 1/λ²); the κ (quartic)
  sector BREAKS it. So with matter on, there is no residual scale gauge: every core number is
  physical.
- Therefore, if the core rule pins only the derivatives (inner mirror φ'_c = ρ'_c = 0), the
  remaining unknowns per fixed r_s are (φ_c, ρ_c): TWO unknowns against TWO conditions →
  **generically a solution exists at EVERY r_s in a range** → a continuum family labeled by
  r_s, even if everything is stable. That would be the honest generic expectation, and it must
  NOT be read as "UDT has no discreteness" — it is the counting of this slice.
- Isolated cell SIZES therefore require one of exactly FOUR structural sources:
  (a) **the core rule pins one more scalar** (e.g. ρ_c fixed by a core model) — then per r_s the
      system is over-determined and closes only at isolated r_s. Legitimate ONLY if the pin is
      pre-registered and never retuned; otherwise it is the new X-kluge.
  (b) **the f-sector fails to be generically solvable/stable**: degree-N solutions of the
      nonlinear PDE may exist or be stable only on special backgrounds (nonlinear-eigenvalue
      behavior). This would be discreteness the GEOMETRY produces — the interesting outcome.
  (c) **stability filtering**: the closure manifold is a continuum of stationary points but only
      isolated points/bands survive the perturbation test (pre-reg criterion 8).
  (d) **ENVIRONMENT PIN (derived candidate — Charles, 2026-07-01).** The cell is not
      self-contained: it sits inside the universe cell, itself a solution of the same equations
      (F5). If the seal-side data must match the AMBIENT state — the universe's Misner-Sharp
      density fixing the φ-level and/or flux environment at the seal — that is one more scalar
      condition SUPPLIED BY THE THEORY, not hand-pinned: count goes over-determined → isolated
      cell sizes generic. This natively reproduces the project's recurring Misner-Sharp
      indication that particle formation may require a specific ambient density or narrow band —
      here as the MECHANISM of isolation, not a side effect. Status: DERIVATION OWED — must
      follow from JC1/JC2 applied to the cell-in-universe configuration (interior P_cell | seal |
      ambient = universe interior, NOT vacuum G): JC1 [√h Z_φ φ']=0 and JC2 π^{AB}-matching
      against the ambient solution's local (φ_amb, ρ_amb, derivatives) at the cell's location.
      "The ambient state pins a scalar at the seal" is the claim to derive; until then it is
      tagged candidate. Scope note: the strictly closed Class-A mirror cell (q=0) is
      environment-blind BY CONSTRUCTION, so this pin lives in a "Class A EMBEDDED" / Class-B
      matching variant — a pre-reg amendment to be made BEFORE any run that uses it.
- **Scan design consequence:** do not force the square system. Map the closure manifold in the
  full (φ_c, ρ_c, r_s) space with derivative-pins at both ends, THEN apply the stability filter,
  THEN observe structure. Discreteness = isolated structure in the (stability-filtered) closure
  manifold. This keeps "solution-space, not imposition" literal.

## 5. [OBS-2] Z_φ labeling correction (small but must not contaminate)

`cell_solver_round.py` sets Z = 8.0, commented "route-B value." Route B is Z_φ = 8 **plus a
forced mixing term** 2e^φ K φ' in the action; the current EOMs contain no mixing term. So the
current system is **Route-A STRUCTURE carrying Route B's number** — a legitimate held-fixed
chose, but it should be ledgered as such, not as "Route B." If Route B is ever claimed, the
mixing term's contribution to the round EOMs must first be derived and included. For the
first question ("any cells at all?") this is tolerable (Z mostly rescales); for ratios it is not.

## 6. [OBS-3] Rigid f = θ is not even stationary for N ≥ 2

Plugging f = θ into the f-EOM leaves a residual ξ(1−N²)cosθ [hand calc; CAS-verify in build].
So the rigid hedgehog is a genuine stationary point only at N = 1; for N ≥ 2 the θ-profile must
deform even before radial structure enters. Consequences: (i) the verified rigid-collapse result
is a statement about an off-shell probe class for N ≥ 2 (still fine as a probe — but the free
solve is MANDATORY there, not optional); (ii) the N ≥ 2 runs should expect θ-deformed profiles
as the baseline, and their I_4θ ≠ 1, which moves the collapse balance before any I_r appears.

## 7. WHAT EXPLORING ALL OF IT WOULD TAKE (whole-before-slice budget)

This build covers ONE cell of a larger grid. The full in-frame space: {rigid | free-f} ×
{L2+L4 | +X² | +L6} × {Class A | Class B seal} × {round | off-round h} × {static | time-live} ×
N ∈ ℤ × the Z_φ fork (Route A / Route B-with-mixing). This build = (free-f, L2+L4, Class A,
round, static, N=1..3, Route-A-structure). Any null propagates ONLY along its own row.

## 8. PROPOSED STEP 0 (analytic, cheap, gated — before the 2-D solver)

A finite-cell virial/Derrick analysis, done symbolically (SymPy), answering: does the reduced
energy on the mirrored domain ADMIT a stationary finite size with free f, and is the
I_r-generating deformation energetically favored near the rigid configuration? Method: (i)
two-parameter scaling family (domain size λ, matter profile scale μ) respecting the mirror BCs
and the core; (ii) stationarity + second-variation conditions as inequalities among the moments
(I_r, I_θ, I_s, I_4r, I_4θ) and the geometry integrals; (iii) special case: second variation of
E in a radial-structure direction δf = ε g(r) h(θ) about f = θ (N=1) — if NEGATIVE, radial
structure is favored, a strong pre-solver signal; if positive-definite, the collapse likely
persists and the scoped negative can be anticipated (still run the solver to confirm).
Deliverable: `f_rtheta_virial_results.md` with the CAS script. This can be done in-session here.

## 9. IMPLEMENTATION CHARTER (for Claude Code, after Charles's sign-off)

Build `cell_solver_f2d.py` + `verify_f2d_reduction.py` + results doc. Constraints binding:

1. **Discretization** (raid the parts bin by METHOD, never assembly):
   - Angular: SH-exact d/dθ (the method inside `spectral_sph_exact.py`) — the winding sin θ
     structure is EXACTLY the known GL-μ-grid mis-differentiation gotcha; do not rediscover it.
   - Radial: Chebyshev collocation (method of `spectral_cheb.py`), Nr ≤ 16 first, 24 max
     (ANTI-HANG). Nθ ≤ 24.
   - Nonlinear solve: Newton with LM damping + line search (method of `newton_solve_p1`), on
     the MONOLITHIC residual [φ-ODE; ρ-ODE; f-PDE; BCs] — do not operator-split (the φ↔ρ↔f
     coupling through e^{2φ} and the moments is stiff by construction).
2. **Continuation:** start from the (N=1) rigid f=θ + vacuum-adjacent background at small
   matter amplitude; continue in r_s BOTH directions; at each r_s record closure residual and
   the solution if closed. For N=2,3 first relax the θ-profile at fixed small r-freedom
   ([OBS-3]), then free r.
3. **Scan = the closure manifold** (§4): grid (φ_c, ρ_c, r_s) with φ'=ρ'=0 pinned at both ends;
   record the closure set UNLABELED; then the perturbation filter (pre-reg criterion 8) by
   time-independent second-variation spectrum of the reduced energy (cheap, same discretization).
4. **Pre-reg tie-in:** fixed Z, ξ, κ per scan; no per-solution retuning; seed-independence
   (criterion 2) via ≥3 distinct initial guesses at representative points; grid-independence
   (criterion 4) via Nr 12→16→24 and a finite-difference cross-check on one closed solution.
5. **CAS verifications owed:** the vacuum-P scale symmetry [OBS-1]; the f=θ residual ξ(1−N²)cosθ
   [OBS-3]; the discretized moments I_r, I_4θ against symbolic values on test profiles.
6. **Op:** single process, unbuffered, no background polling, `python3 -m pytest tests/` before
   any commit; commit scripts WITH the results doc.
7. **Reporting:** WHAT IS THERE, unlabeled. If it collapses everywhere: the scoped negative is
   "round static free-f(r,θ), L2+L4, Class A does not stabilize" — next in-frame freedoms are
   X²/L6 (P4) and Class-B seal, then off-round; the frame verdict is NOT reached.

## 10. STATUS

MAP only. Nothing built, nothing banked. Awaiting Charles: (a) catch/strike premises;
(b) decide the core-rule question in §4(a) — pin or observe-the-manifold (this MAP recommends
observe-the-manifold first, pin never without pre-registration); (c) gate Step 0 (§8) and the
build (§9).
