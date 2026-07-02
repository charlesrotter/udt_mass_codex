# cell_solver_f2d — build notes (code construction + CAS cross-check + bounded smoke test)

**Date:** 2026-07-01. **Mode:** CODE CONSTRUCTION (not a physics run). **Author:** Claude Code agent.
**Scope:** built the 2-D finite-mirror cell solver `cell_solver_f2d.py`, its CAS cross-check
`verify_f2d_reduction.py`, and ran the BOUNDED smoke test only. **No cell claimed; no scan run; no
discreteness claim.** Frozen contract = `discreteness_preregistration.md` (Class A FREE, H=0).
Source equations taken verbatim from `f_rtheta_free_field_MAP.md §2`, `f2d_virial_step0_results.md`,
`round_matter_reduction_results.md`; nothing invented.

## What was built

`cell_solver_f2d.py` — coupled solver for φ(r), ρ(r), f(r,θ) on the finite mirrored round cell,
interior Branch P, φ-blind matter, winding degree N. Structured functions: `make_ctx` (grid/operators),
`fields` (shared evaluator: derivatives + θ-moments + all EOM residual densities), `residual`
(monolithic [φ-ODE; ρ-ODE; f-PDE; mirror BCs; H=0]), `H_of_r` (conserved-Hamiltonian diagnostic +
the closure row), `derrick` (Derrick integral-identity diagnostic), `newton_lm_solve`
(Levenberg-Marquardt, Nielsen gain-ratio damping, jacrev Jacobian), `seed`, and a `__main__` that runs
ONLY the bounded smoke test. Z, ξ, κ, N are fixed at the top of `__main__`, each tagged CHOSE/THEORY.

`verify_f2d_reduction.py` — imports the ACTUAL discrete operators and checks them against symbolic /
high-accuracy references (10 checks, all PASS).

## Discretization choices (methods mined from the parts bin; no wrong-frame assembly imported)

1. **Angular = SH-exact d/dθ, m=0 sector** (method of `spectral_sph_exact.py`). For the axisymmetric
   field f the SH-exact operator is the associated-Legendre-order-0 = ordinary-Legendre(μ) operator
   `Dθ = dSθ·inv(S)`, `S[i,j]=P_j(μ_i)`, `dSθ[i,j]=−sinθ_i P_j'(μ_i)`. GL-μ interior nodes never hit
   the poles, so all `1/sinθ` factors are evaluated only interior, and θ-integrals become GL sums:
   `∫g sinθ dθ = Σ w_j g_j`, `∫g/sinθ dθ = Σ w_j g_j/(1−μ_j²)`.
   - **CAUGHT + FIXED via the CAS check:** the second θ-derivative must use the ANALYTIC operator
     `Dθθ` built from `d²P/dθ² = −cosθ P' + sin²θ P''`, **NOT** `Dθ@Dθ`. Composing `Dθ` is inexact
     because `dP/dθ = −sinθ P'` carries an extra `sinθ` and leaves the polynomial-in-μ space (the
     m=0 second-derivative analog of the `spectral_sph_exact` winding gotcha). With `Dθ@Dθ` the f-PDE
     cross-check failed at 1.9e-2; with the analytic `Dθθ` it passes at 1.3e-15.
2. **Matter unknown = the DEVIATION u = f − θ** (f = θ + u). The rigid hedgehog f=θ is then u=0,
   represented EXACTLY; the pole values f(0)=0, f(π)=π and the degree N are carried by the θ-ramp
   background (no pole collocation — the GL-μ grid has no pole nodes; regularity replaces the BC, as
   in `spectral_sph`). The f-PDE divergences are assembled in EXPANDED form (coefficient derivatives
   A_r, B_θ taken ANALYTICALLY; only u_r, u_rr, u_θ, u_θθ come from the operators) — this makes the
   rigid residual **exactly** ξ(1−N²)cosθ at every node (OBS-3 / V1), verified discretely.
3. **Radial = Chebyshev collocation** (method of `spectral_cheb.py`) on a FIXED reference ζ∈[−1,1];
   physical r = r_c + (L/2)(ζ+1) so d/dr = (2/L)D_ζ with the cell length **L a Newton unknown** (the
   free boundary). Cheb `D²=D_ζ@D_ζ` IS exact on the polynomial space (no analog of the θ problem).
   The EOMs are autonomous in r, so r_c is a pure length label and only L is physical (this is exactly
   why H is conserved and H=0 closes the count).
4. **Monolithic residual, LM solve** (method of `newton_solve_p1`): 11-ish coupled rows are NOT
   operator-split; Jacobian by `torch.func.jacrev` (residual is pure torch → jacrev-safe). Damping =
   Nielsen gain-ratio LM (the `glm` control that floored residuals in the p1 solver).
5. **H=0 closure** imposed via the full H(r) expression at the seal node (Step-0 V5). Counting is
   SQUARE: unknowns [φ(Nr), ρ(Nr), u(Nr·Nθ), L] = 2Nr+Nr·Nθ+1; equations [φ-ODE interior + φ'=0 both
   ends] + [ρ-ODE interior + ρ'=0 both ends] + [f-PDE interior×all θ + f_r=0 both ends×all θ] + [H=0]
   = 2Nr+Nr·Nθ+1. Verified equal in the smoke test (81 = 81 at Nr=Nθ=8).

## CAS cross-check results — `verify_f2d_reduction.py`: **10/10 PASS**

- (a) θ-moments: f=θ → (I_r,I_θ,I_s,I_4θ,I_4r)=(0,1,1,1,0) exactly (err 0). Band-limited deformed
  profile: I_r exact (0e0/4e-17; integrand poly in μ → GL exact); I_4θ 4.6e-13 (spectral; carries
  sin²f, non-polynomial → GL quadrature accuracy) and CONVERGES 4.6e-13→2.2e-16 as Nθ 8→16.
- (b) manufactured smooth (φ,ρ,f): φ-ODE discrete==symbolic 3.2e-15; f-PDE discrete(expanded)==
  symbolic(conservative) 1.3e-15; ρ-ODE (with GL-sum moments inside the assembled residual) 1.7e-14.
- (c) rigid f=θ residual == ξ(1−N²)cosθ discretely: N=1 err 2.7e-15 (→0), N=2 9.8e-15, N=3 1.4e-14.

## Smoke-test output (Nr=8, Nθ=8, N=1, Z=8, ξ=κ=1; wall 0.5 s of a 120 s budget)

- **Residual assembles:** len(u)=len(F)=81 (square), max|F|=0.71, all finite.
- **Jacobian finite/non-singular enough to step:** seed cond ≈ 1e17, s_min ≈ 1e-14. This large seed
  cond is a **flat-seed artifact**, not structural: the near-null right singular vector loads 0.99 on
  L, and the starved rows are the φ-ODE/φ'-BC — when φ=ρ=const nothing pins L (the EOMs are ~0 and
  L-flat there). As soon as the fields gain structure the cond drops to **≈5e9** (= the known
  Chebyshev endpoint-amplification conditioning, matching the p1 header's ~1e9–1e11 note). LM
  descends monotonically through both; a Galerkin-basis remedy (as in p1) is available if a
  production scan needs a better-conditioned step.
- **One Newton step decreases the residual:** Φ 4.57 → 1.58 on step 1, then monotone to 3.6e-3 at the
  30-iter cap (still descending, not stalled — this is a bounded step count, NOT a convergence claim).
- **Diagnostics compute:** H(r) conserved (drift max−min ≈ 1.5e-5 on the descended field; the conserved
  quantity holds numerically); Derrick S_a/S_b computed (S_a−S_b ≈ 0.17 off-solution, as expected — it
  is a per-solution identity, not zero off a solution).

## Correctness caveats / places of uncertainty (honest)

1. **Second-θ-derivative operator** was the one real bug — fixed (analytic Dθθ). All other operators
   verified to machine/spectral accuracy.
2. **Non-band-limited fields → spectral, not exact.** A REAL deformed solution f is not band-limited
   in μ (f=θ itself is not); the moments carrying sin²f (I_s, I_4θ, I_4r) and any θ-derivative of the
   true solution are spectrally accurate, not exact, at finite Nθ. The verify shows convergence with
   Nθ. A production scan MUST include the pre-registered grid-independence check (Nθ, Nr refinement)
   — the smoke test does not establish converged accuracy, only correct assembly.
3. **Pole BCs are seed/background-carried, not collocated** (GL-μ interior grid). The degree N and the
   f(0)=0/f(π)=π values ride on the θ-ramp background + the topological sector of the seed; there is no
   explicit pole row. This matches `spectral_sph`'s treatment but means the pole/degree structure is a
   PROVENANCE of the seed, to be watched in a real scan (as the pre-reg already notes for N).
4. **H=0 imposed at the seal only** (one scalar). It is the conserved quantity, so seal-value=0 ⇒
   everywhere on-shell; the H(r) drift is monitored as the discretization-drift diagnostic. Off-shell
   (during Newton) H is not yet flat — that is expected.
5. **Conditioning:** the structural ~5e9 (Chebyshev endpoint) is inherited, not new; it did not block
   the bounded step but would want the Galerkin remedy for a careful scan (flagged, not built here).
6. **Not tested:** convergence to an actual closed cell; multi-seed independence; N≥2 θ-relaxation
   (OBS-3 says N≥2 needs the θ-profile freed first); the full closure-manifold scan. All of these are
   the SEPARATE gated run, deliberately not performed here.

## Op notes
Single clean unbuffered process; no background polling; no nohup; wall 0.5 s. `python3 -m pytest tests/`
= **32 passed, 1 xfailed** (the pre-existing solution-space-gate xfail; unchanged). Nothing committed.
