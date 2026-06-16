# RESULTS — THE FULL-3-D SPECTRAL COUPLED EINSTEIN+L2+L4 SOLVER
## (criterion-4 psi · criterion-6 winding · criterion-8 branch/catalog)

Research record (append-never-edit). Driver: Claude (Opus 4.8, 1M). 2026-06-16.
OBSERVE mode (report WHAT IS THERE; add NO mechanism; report whichever way it
falls). DATA-BLIND throughout (units L = sqrt(kappa/xi) = 1; NEVER compared to
wall numbers / nature). Coverage push, NOT a capstone.

This push builds the FULL-3-D SPECTRAL solver (no spatial symmetry imposed: r, θ,
ψ all live; full 4×4 metric available; matter FREE over (r,θ,ψ); winding m) to
open the BLANK tiles the 2-D axisymmetric spectral solver (#59) could not reach:
the NON-AXISYMMETRIC (ψ-dependent) sector and the HIGHER-WINDING sector — the most
likely home of a Skyrme-type distinct-shape catalog.

---

## 0. EXECUTIVE SUMMARY (the honest binary read)

- **INFRASTRUCTURE VALIDATED (the durable deliverable).** Three independent,
  category-A-audited engines were built and validated to the floor:
  (A) the **analytic 3-D mixed Einstein tensor** for the diagonal Weyl metric with
  ψ LIVE — flat space → 0 EXACTLY (machine zero, all resolutions), Schwarzschild →
  0 EXPONENTIALLY (2.0e-3 @Nr16 → 4.2e-7 @Nr48), and it MATCHES the validated 2-D
  analytic engine to **1.2e-14** in the axisymmetric limit (incl. the off-diagonal
  G^r_θ channel). (B) the **correct full-3-D matter Euler-Lagrange** by DIRECT
  variation of the action (the proven 2-D-CORRECT method, extended to ψ + winding
  m) — **machine-zero on the round soliton (3e-12 to 6e-11)** across resolutions,
  and its symbolic stress-consistency identity div_μ T^μ_r = −EL·∂_rΘ holds
  EXACTLY (sympy = 0). (C) the **exact-chain-rule field gradient** — the matter
  stress matches the validated 1-D radial stress (ρ, p_r, p_T) to **1e-13**.
  NONE of these can carry the L4 codegen bug the #59 verifier found (the EL is the
  literal variation of the same action that builds the stress).

- **VALIDATION GATE: PASS.** The corrected #56 round soliton is recovered in the
  full-3-D basis: **M_MS = 0.2808** (#56: 0.2811–0.2812) across Nr=40/48, Nps=8/12;
  the mass-weighted gauge-invariant angular shape DECREASES with resolution toward
  round (tvar 8.5e-3 @Nth8 → 3.1e-3 @Nth10; psivar 8.0e-3 → 2.2e-3), ψ-structure
  machine-clean where the soliton has mass; weighted residual Phi → 3e-4. The 3-D
  basis is non-restrictive; round is a fixed point.

- **NON-AXISYMMETRIC + HIGHER-WINDING CATALOG SEARCH: SOLVER-LIMITED / INCONCLUSIVE
  — NO verdict drawn (honest).** The off-round relaxation could NOT be driven to a
  clean residual floor with a trustworthy round-recovery. The DECISIVE diagnostic:
  the AXISYMMETRIC CONTROL (an axisym l=2 perturbation) — which the validated 2-D
  spectral solver (#59) relaxes back to round at the floor (tvar 0.94 → 1e-3, Phi
  → 1e-10) — in the present full-3-D solver reaches Phi ~ 4e-5 but its mass-weighted
  shape STALLS at tvar ≈ 0.086 (it does NOT collapse to the round floor). Because the
  axisym control (a KNOWN relax-to-round) does not converge cleanly here, the
  non-axisym / higher-winding results CANNOT be read as "disconnected type" vs
  "unconverged." The matrix-free Levenberg–Marquardt (Jacobi-preconditioned CG)
  converges too slowly on the off-round angular sector at feasible iteration counts;
  the small grid (32³-class) the cost permits has an angular-diagnostic floor ~0.05,
  not 1e-3. Per the charter ("if you cannot converge without a category-B
  simplification, STOP and REPORT honestly"), the catalog binary is left OPEN in the
  3-D sector — this is a SOLVER capability gap, NOT a physics negative.

- **VERDICT.** UDT's classical NON-AXISYMMETRIC and HIGHER-WINDING catalog question
  remains **OPEN** — now with the correct physics machinery built and validated (the
  Einstein engine, the matter EL, the round gate), and the remaining gap isolated to
  the OFF-ROUND coupled-solve CONVERGENCE (a tractability problem, the next build).
  What is newly SOLID: the round soliton is reconfirmed as a full-3-D-basis solution
  (M_MS = 0.281), and the tools that any future non-axisym search needs are now
  native, pole-stable, and correct off-round.

- **NO CATEGORY-B SIMPLIFICATION USED.** B=1/A FREE (a,b independent; recovered in
  the exterior as a RESULT on the gate); matter FREE over (r,θ,ψ); no seal/source
  injection; no linearization kept as a result; no dropped term; no imported
  mechanism; no dial tuned to a target. The analytic-G substitution is the SAME
  native Einstein content (proven flat/Schwarzschild/round, matches 2-D to 1e-14).

---

## 1. THE BUILD — per-technique CATEGORY-A audit

### 1.1 Spectral discretization (Cheb_r × Gauss-Legendre_θ × Fourier_ψ)
`spectral_cheb.py` (radial, reused), `spectral_sph.py` (NEW: θ via Gauss-Legendre
in μ=cosθ — poles EXCLUDED, the standard spectral cure; ψ via UNIFORM periodic
nodes + the FOURIER spectral differentiation matrix — genuinely periodic, no edge).
CATEGORY-A: Fourier d/dψ MACHINE-EXACT on band-limited modes (err 2e-16); ψ
quadrature exact (err 0 on 1+cos²ψ); θ operator exponentially convergent (P_3 err
1e-15); full-sphere quadrature exact (∫dΩ = 4π, err 0). A discretization only — no
tie/source/linearization/drop. This is the criterion-4 (ψ) blind-spot opener.

### 1.2 The analytic pole-stable 3-D Einstein engine
`gen_einstein_3d_weyl.py` → `einstein_3d_weyl_gen.py` → `einstein_3d_eval.py`.
WHY: a purely-NUMERICAL NR engine (whole_metric_3d_core) differentiating the raw
spherical metric does NOT numerically cancel the coordinate-pole cot/(1/sin²)
structure — its flat-space residual GROWS with resolution (25 @Nth6 → 367 @Nth16)
and it fails to converge to the analytic engine even at mid-θ (~0.1, non-decreasing)
because the Christoffel-then-differentiate pipeline is a DOUBLE spectral
differentiation that amplifies aliasing. CURE (the validated 2-D approach, extended
to ψ): derive G^μ_ν ANALYTICALLY (sympy cancels cot/1/sin symbolically into finite
expressions), evaluate ONLY the SMOOTH warp derivatives a,b,c,d spectrally.
CATEGORY-A PROOF: (i) flat → 0 EXACTLY (machine zero, all (Nr,Nth,Nps)); (ii)
Schwarzschild → 0 EXPONENTIALLY (2.0e-3 → 4.2e-7 across Nr=16..48); (iii) MATCHES
the validated 2-D analytic engine to 1.2e-14 in the axisym limit (diagonal AND
off-diagonal G^r_θ). Same native Einstein content (charter principle 4), made
pole-stable. SCOPE: covers the DIAGONAL Weyl metric (a,b,c,d, ψ-live); the spatial
off-diagonal metric components g_rθ,g_rψ,g_θψ are NOT in this analytic engine (the
genuine non-axisymmetry it can express enters through ψ-dependence of a,b,c,d AND
the free matter; full off-diagonal metric is flagged residual — see §5).

### 1.3 The correct full-3-D matter Euler-Lagrange (direct variation)
`gen_matter_el_3d.py` → `matter_el_3d_gen.py`, via
EL = [∂_r(∂lag/∂Θ_r) + ∂_θ(∂lag/∂Θ_t) + ∂_ψ(∂lag/∂Θ_p) − ∂lag/∂Θ]/√g,
lag = √(−g)(L2+L4). This is the SAME proven-correct method that produced the
verified `axisym_matter_el_CORRECT.py` (the #59 verifier's fix), extended to ψ +
winding m. STRUCTURALLY immune to the L4 codegen bug: it is the literal variation
of the SAME action that builds the Hilbert stress.
CATEGORY-A PROOF: (i) MACHINE-ZERO on the round soliton (3e-12..6e-11) across
Nr=48/64, Nth=8, Nps=8/12; (ii) SYMBOLIC stress-consistency: div_μ T^μ_r = −EL·∂_rΘ
holds EXACTLY (sympy = 0) — the off-round correctness gate the prompt required, in
the load-bearing radial component; (iii) for m=1 the c-sector terms reduce to the
verified 2-D-CORRECT form.
NOTE (honest, on the single-Θ family): the field is the unit-S³ hedgehog with ONE
free profile Θ(r,θ,ψ) and the angular embedding (G=θ, H=mψ) FIXED — the same
hedgehog reduction the validated 1-D and 2-D searches used. The div(T) identity
holds EXACTLY for ν=r but carries a nonzero ν=θ,ψ remainder (the θ,ψ momentum
conservation a single field DOF cannot separately satisfy) — i.e. the single-Θ
family is a RESTRICTED non-axisymmetric search (ψ-dependence via Θ; lobed energy
distributions and all windings m). The FULL S³ map (three free profiles F,G,H) is
the complete non-axisym field and is flagged residual (§5).

### 1.4 The exact-chain-rule field gradient
`full3d_spectral.field_dn`: spectral differentiation does NOT obey the chain rule
pointwise (it is global), so differentiating each nonlinear hedgehog component
directly gave G_rr = 2Θ'² (wrong). CURE: take the SPECTRAL derivatives of the
SMOOTH profile Θ only, combine with the ANALYTIC ∂n/∂Θ and the exact angular
partials. CATEGORY-A PROOF: G_rr = Θ'² exactly; the matter stress (ρ, p_r, p_T)
matches the validated 1-D radial stress to 1e-13.

### 1.5 Diagonal Weyl gauge (B=1/A FREE); core/axis regularity; proper-volume weight
Diagonal Weyl (a,b,c,d independent of r,θ,ψ) — B=1/A NOT tied; recovered on the
gate. GL-in-μ nodes never touch the axis (θ=0,π); ψ periodic (Fourier, no edge);
the innermost/outermost 3 Cheb radial rows are regularity-excised from the
objective (O(N²) edge amplification on the steep core/seal — a coordinate-edge
artifact, the deep body converges); winding BC Θ(core)=mπ, Θ(seal)=0; seal gauge
a(seal)=0; depth dial b(core)=−p; c,d regular. Proper-volume weight W=√(√g·dV)
conditions the descent without changing the zero set. All category-A.

### 1.6 Solver (matrix-free Jacobi-preconditioned-CG Levenberg–Marquardt)
`full3d_solver.py`: minimize Phi = ||√W (G−κ8 T, matter-EL, BC)||² by damped LM,
strict monotone acceptance; the Gauss-Newton normal-equation action (J^TJ+λI) by
autograd JVP/VJP + Jacobi-preconditioned CG (matrix-free — the ~1e4 unknowns make a
dense Jacobian per-iteration affordable only on the smallest grids; a dense-LM path
is provided for those). CATEGORY-A: Gauss-Newton's local linear step is the SOLVER
(as the #56 / #59 solvers used), not a physics linearization. **LIMITATION (the
honest core finding): this solver converges the ROUND gate but does NOT drive
OFF-ROUND angular configurations to a clean floor in feasible iteration counts — see
§3.** This is a tractability gap, not a category-B move.

*** THE NATIVE LINE (held precisely): every technique is conditioning of the SAME
native Einstein+L2+L4 equations. B=1/A FREE. NO seal/source injection, NO
linearization-as-result, NO dropped term, NO imported mechanism, NO dial tuned to a
target. The analytic-G substitution and the direct-variation EL are the SAME native
content, proven on flat/Schwarzschild/round and machine-zero on round. ***

---

## 2. VALIDATION GATE — round #56 recovered in the 3-D basis (PASS)

`full3d_final_run.py gate`, Cheb_r × GL_θ × Fourier_ψ, p=0.4, kap8=0.05, cell 14L.

| Nr | Nth | Nps | seed Phi | solved Phi | M_MS | (#56) | tvar(GI,massW) | psivar | EL |
|----|-----|-----|----------|-----------|------|-------|----------------|--------|-----|
| 40 | 8  | 8  | 2.0e3 | 3.3e-4 | 0.28077 | 0.28122 | 8.5e-3 | 8.0e-3 | 2.0e-3 |
| 48 | 10 | 8  | 1.5e3 | 3.0e-4 | 0.28085 | 0.28106 | 3.1e-3 | 2.2e-3 | 2.6e-3 |
| 40 | 8  | 12 | 2.9e3 | 5.1e-4 | 0.28087 | 0.28122 | 9.0e-3 | 7.4e-3 | 4.1e-3 |

M_MS matches #56 to 3–4 dp; the mass-weighted gauge-invariant angular shape
(tvar/psivar) DECREASES with resolution toward round (the soliton is round where it
carries mass; far-tail rho≈0 is excluded by the mass weighting). The round soliton
is a CLEAN FIXED POINT of the full-3-D system; the basis is non-restrictive.
**GATE: PASS.** (The remaining Phi ~ 3e-4 is the core/seal Cheb-edge amplification,
the documented coordinate artifact; the deep-body residuals are O(1e-4..1e-3).)

---

## 3. OFF-ROUND SEARCH ATTEMPT — SOLVER-LIMITED (honest, no verdict)

`full3d_final_run.py robust`, grid 32×6×6, amp 0.25, 6 relax blocks each.

| seed | seed (Phi, psivar, tvar) | final (t) Phi | psivar | tvar | M_MS |
|------|--------------------------|---------------|--------|------|------|
| axi_l2 (CONTROL) | 1.6e3, 0.00, 0.08 | (140s) 4.2e-5 | 5.9e-2 | 8.6e-2 | 0.27901 |
| psi1 (ψ m=1 lobe) | 1.6e3, 0.09, 0.10 | (138s) 3.8e-4 | 1.2e-1 | 1.3e-1 | 0.28897 |
| psi2 (ψ m=2 bar)  | 1.6e3, 0.07, 0.09 | (139s) 4.4e-5 | 5.4e-2 | 6.4e-2 | 0.28062 |

**THE DECISIVE READ (the axisym CONTROL):** an axisymmetric l=2 perturbation —
which the validated 2-D spectral solver (#59) relaxes back to round at the floor
(tvar 0.94 → 1e-3, Phi → 1e-10) — in the present full-3-D solver reaches Phi ~ 4e-5
but its mass-weighted shape STALLS at tvar ≈ 0.086 and even develops spurious
psivar ≈ 0.059 (the axisym input has psivar = 0). Because a KNOWN-relax-to-round
case does NOT converge cleanly here, NO conclusion can be drawn from psi1/psi2:
their residual psivar/tvar (0.05–0.13) is indistinguishable from the solver's own
unconverged floor on this coarse grid. (A longer matrix-free run on psi1 confirmed:
Phi decreases monotonically 0.9 → 0.29 over 250 s but psivar does NOT collapse —
the solver is too slow, not arresting at a type.)

**CONCLUSION (per the charter STOP-and-REPORT rule):** the non-axisymmetric and
higher-winding catalog search is INCONCLUSIVE — gated by OFF-ROUND coupled-solve
CONVERGENCE, a tractability problem. It is NOT a banked negative and NOT a positive.
The HIGHER-WINDING (m=2,3,4) shapes/masses were therefore NOT mapped (same
convergence gate). The capability needed next: a faster, better-conditioned
off-round 3-D solver (the dense-LM path on a moderate grid, a Newton-Krylov with a
real elliptic preconditioner, or a self-consistent-field iteration that decouples
the metric and matter blocks).

---

## 4. PREMISE LEDGER (chose or derived?)

| Item | tag | note |
|---|---|---|
| Action L2 + native L4 + seal, two-way phi | DERIVED | C-2026-06-14-1; reused (infra-audit CLEAN) |
| Unit S^3 hedgehog field, single Θ(r,θ,ψ), winding m | DERIVED (#55) restricted | the settled source; FREE over (r,θ,ψ); full S³ map (F,G,H) is residual |
| Corrected #56 round soliton (a,b indep) | DERIVED (#56, blind-verified) | validation target + seed |
| Cheb_r × GL_θ × Fourier_ψ spectral basis | CHOSE (numerics) | category-A: machine-exact ops; recovers #56 (§1.1) |
| Analytic 3-D Weyl Einstein (cot/1/sin symbolic) | DERIVED-numerics | same content as 2-D engine; flat/Schwarzschild/round (§1.2) |
| Diagonal Weyl gauge (a,b,c,d indep, ψ-live) | CHOSE (gauge) | B=1/A NOT tied; spatial off-diagonals NOT carried (residual, §5) |
| B=1/A FREE | DERIVED-need | recovered in exterior on the gate as a RESULT |
| Correct 3-D matter EL (direct variation) | DERIVED-numerics | machine-zero on round; symbolic div(T)=−EL∂Θ ν=r exact (§1.3) |
| Exact-chain-rule field gradient | DERIVED-numerics | stress matches 1-D to 1e-13 (§1.4) |
| core/axis regularity (GL off-axis; Cheb-edge excise 3 rows) | CHOSE (BC/conditioning) | required physics + coordinate-edge artifact removal |
| proper-volume weight; mass-weighted GI diagnostic | CHOSE (conditioning/diag) | does not change the solution set |
| matrix-free Jacobi-PCG LM | CHOSE (numerics) | the solver's local step; off-round convergence INSUFFICIENT (§3) |
| depth dial p, kap8=0.05; xi=kap=1 | CHOSE | declared control inputs, not fitted |

NEW DIALS introduced: none physical (basis orders Nr/Nth/Nps, edge-excision width,
LM damping, Hutchinson probe count, the geometry/mass weights are numerical-
conditioning / diagnostic choices, all flagged; none alters the native equations).
PRINCIPLE 2: full nonlinear throughout; spectral derivative + autograd + sympy
direct variation = sanctioned exact-on-poly / machine-precision function-
replacements. No linearization kept as a result.

---

## 5. HONEST COVERAGE / LIMITS (the ten criteria for THIS push)

- COVERED (validated): criterion-1 fields (a,b,c,d diagonal warps + Θ, all ψ-live);
  criterion-2/3 action terms & equations (full L2+L4, full mixed Einstein, matter
  EL — correct off-round); criterion-4 DOMAIN incl. ψ (the blind-spot OPENED:
  Fourier-ψ machine-exact, round gate clean in 3-D); criterion-5 BC/regularity.
- ATTEMPTED but SOLVER-LIMITED (no closure): criterion-6 winding m=2,3,4 (seeds
  built, shapes/masses NOT mapped — off-round convergence gate); criterion-8
  branch/bifurcation = the CATALOG (non-axisym charge-1 + higher-winding — the
  search is inconclusive, §3); criterion-9 stability (not reached).
- DROPPED (flagged blind-spots, could host structure):
  (i) the SPATIAL off-diagonal metric g_rθ,g_rψ,g_θψ — the analytic Einstein engine
      covers the diagonal Weyl class; a genuinely non-axisym METRIC shape generically
      needs these (the matter and the ψ-dependent diagonal warps carry SOME
      non-axisymmetry, but not all). This is the honest scope edge of the metric DOF.
  (ii) the FULL S³ matter map (F,G,H) — the single-Θ hedgehog is a restricted
      non-axisym family (div(T) ν=θ,ψ remainder, §1.3).
  (iii) criterion-7 rotation/twist (time-row off-diagonals g_tψ) — static here.
  (iv) criterion-10 regime: validated at p=0.4, kap8=0.05; the round gate is
      basis-robust, the off-round sector is untested across regime.
- REGIME OF VALIDITY: the VALIDATED results (Einstein engine, matter EL, round gate)
  are basis-robust at the canonical (p=0.4, kap8=0.05, 14L cell) point. The off-round
  search has NO established regime (it did not converge).
- ANTI-INFLATION: this is ONE tile. The 3-D non-axisym/winding CATALOG space is still
  BLANK as a verdict; what is newly filled is the 3-D ROUND-recovery and the correct
  3-D physics machinery.

---

## 6. NO-CATEGORY-B CONFIRMATION + housekeeping

NO category-B simplification used (confirmed): B=1/A free (recovered on gate); matter
FREE over (r,θ,ψ); no seal/source injection; no linearization kept as a result; no
dropped term; no imported mechanism; no dial tuned to a target; the analytic-G and
direct-variation-EL substitutions are the SAME native content (proven). The ONE
honest limitation is SOLVER CONVERGENCE off-round (§3), explicitly NOT a physics
simplification.

HOUSEKEEPING: `axisym_matter_el.py` marked DEPRECATED/INVALID-off-round (the #59
verifier's L4 bug); `axisym_matter_el_CORRECT.py` (2-D) and `matter_el_3d_gen.py`
(3-D) are the correct direct-variation ELs.

SCRIPTS (committed, all run IN-PROCESS / blocking; GPU V100 torch float64 + CPU
sympy/scipy): `spectral_sph.py`, `gen_einstein_3d_weyl.py` / `einstein_3d_weyl_gen.py`
/ `einstein_3d_eval.py`, `gen_matter_el_3d.py` / `matter_el_3d_gen.py`,
`full3d_spectral.py`, `full3d_solver.py`, `full3d_campaign.py`, `full3d_final_run.py`.
Reused validated physics (infra-audit CLEAN): `whole_metric_3d_matter.py`,
`whole_metric_3d_core.py`, `radial_Bfree_soliton.py`, `spectral_radial_soliton.py`,
`spectral_cheb.py`.

---

## 7. BLIND VERIFIER — PENDING.  ATTACK HERE:
1. THE ENGINES: re-run on OWN machinery — (a) analytic 3-D Einstein flat=0 /
   Schwarzschild exponential / 2-D-axisym match; (b) the 3-D matter EL machine-zero
   on round AND the symbolic div(T)=−EL∂Θ identity (ν=r exact; characterize ν=θ,ψ
   remainder as the single-Θ reduction, not a bug); (c) the field-gradient chain-rule
   (stress = 1-D to 1e-13).
2. THE GATE: re-confirm round #56 recovered in 3-D (M_MS=0.281; mass-weighted
   tvar/psivar decreasing with resolution -> round; B=1/A recovered exterior).
3. THE SOLVER LIMITATION (the load-bearing honest claim): confirm the AXISYM CONTROL
   does NOT relax to the round floor in this solver (the reason the non-axisym search
   is inconclusive) — i.e. verify the negative is a CONVERGENCE gap, not a hidden
   physics arrest. Try to converge ANY off-round seed to a clean floor (Phi ~ 1e-9
   AND a round-recovered axisym control); if you can, the search can be RE-RUN.
4. NO category-B: B=1/A free; matter free; no injection; the analytic-G / direct-EL
   are the same native content.
5. SCOPE: confirm the dropped criteria (spatial off-diagonal metric; full S³ map;
   twist; winding shapes) are honestly flagged and the catalog binary is left OPEN
   (not banked) in the 3-D sector.
