# Off-Round 3-D Static Solver — the #60 wall broken (category-A) — 2026-06-16

**Push:** Phase 2 of the "fix-static-then-eigenvalue" sequence (Charles 2026-06-16).
**Mode:** OBSERVE / solver-build. Category-A (conditioning) ONLY. DATA-BLIND (L=sqrt(kappa/xi)=1).
**Driver:** Claude (Opus 4.8, 1M), agent-fanned. **Verifier-before-record:** PASS (agent a57302bada835a340).
**Builds on:** INFRA-AUDIT #2 (infrastructure_audit_3d_2026-06-16.md), which established the
#60 base is clean and that the off-round wall is the SOLVER (matrix-free Jacobi-PCG), not the
physics — a DENSE explicit-Jacobian path provably reaches the floor.

## THE RESULT
The off-round 3-D coupled Einstein+L2+L4 static solve — solver-LIMITED at #60 (matrix-free
Jacobi-PCG crawled, stalling ~1e-5) — now CONVERGES to a clean floor via an explicit-Jacobian
Newton/LM solver. The #60 "INCONCLUSIVE / solver-limited" gate is REMOVED. This is pure
category-A conditioning: the equations are UNCHANGED (verified value-equivalent to round-off).

## NEW MODULES (committed with this doc; new files, no committed file edited)
- `full3d_newton.py` — production explicit-Jacobian Newton/LM. Builds J=dF/du in one batched
  reverse pass via torch.func.jacrev; takes the exact LM step by direct factorization. To be
  vmap-safe it replaces torch.linalg.inv/.det in the 4x4 metric inverse with MANUAL analytic
  cofactor (adjugate/determinant) — bit-equivalent (verified). Imports the residual physics
  verbatim from the committed full3d_solver. Includes parameter CONTINUATION.
- `sh_theta_operator.py` — spectrally-EXACT polar-angle derivative for m!=0 (fixes must-fix M1:
  the live Legendre op is exact only at m=0). Machine-exact m=0..4; reduces to the live op at
  m=0 (cannot regress round). NOT yet wired into a full coupled off-round solve — that is the
  Phase-3 integration gate.
- `divT_excised.py` — core/seal-excised stress-conservation checker (fixes broken-gate C3:
  the committed divT diverged with resolution). Converges x20 with resolution; identity
  nabla_mu T^mu_nu = -EL*d_nu(Theta) holds on the interior. For Phase-3 stability/conservation.

## VALIDATION (builder gates + independent verifier, actual numbers)
- VALUE-EQUIVALENCE (headline correctness): full3d_newton vmap-safe residual vs committed
  full3d_solver.residual_vector on 6 random states across varied (p,kap8,m,wbc):
  **max abs 1.4e-14, max rel 4.3e-17.** Same equations to round-off. No category-B.
- ROUND FLOOR (grid 20x6x8): Phi 1877 -> **3.8e-13 in ~14-20 Newton iters**. Per-component
  max|res| (via the INDEPENDENT committed CORE.metric_inverse path): tt 4.6e-8, rr 8.2e-9,
  thth 1.9e-8, psps 2.4e-8, rth 4.8e-9, rps 2.1e-16, thps 1.4e-16, el 1.3e-7. The ANGULAR
  (thth/psps) Einstein eqns — which the radial #56 slice never imposed (res_thth=0.21 there) —
  are now driven to ~1e-8. => a genuine FULL-3-D round solution, not the radial slice.
- B=1/A FREEDOM: maxB1A = max|a+b| on body = **1.42e-1** (converged). If B=1/A were tied this
  would be ~0. g_tt, g_rr independent. Category-A confirmed.
- PRODUCTION grid (32x10x8, nF=17280): quadratic descent (Phi 3590 -> 6.5e-7 in 4 it).
- CONTINUATION: p=0.40->0.42->0.44 each re-converges in 5-6 it to ~2e-12, M_MS~0.289 stable.
  (The Phase-3 enabler — step a deformation/winding parameter, re-solve from the prior solution.)
- ENV/COFACTOR SAFETY: CPU run (CUDA off) bit-consistent with GPU (Phi 3.8e-13, M_MS 0.28939,
  maxB1A 1.42e-1). PYTORCH_NO_CUDA_MEMORY_CACHING + manual cofactor inverse do NOT corrupt.

## CAVEATS / HONEST LIMITS (verifier-required, recorded)
- OFF-ROUND PROBE = RELAXED-BACK, NOT a catalog member. A small sin(psi) Theta deformation
  converges (Phi -> ~1e-11/1e-12) but its psi-structure DECAYS ~6x: seed psi-spread 3.8e-2 ->
  converged 5.9e-3..1.3e-2. The perturbation largely dies back toward axisym. This is the
  EXPECTED null for "no off-round member near the round soliton" — it is NOT yet the catalog
  search and must NOT be recorded as a discovered off-round solution. A genuine search needs
  topological WINDING (m=2,3,4) configs + amplitude scaling, not a perturb-and-relax (Phase 3).
- M_MS: 3-D round M_MS = 0.28939 at the gate1 grid. The radial reference itself moves with
  grid (0.281 production-radial vs 0.28465 at Nr=19), so the "0.290 vs 0.281 = 3% refinement"
  partly conflates radial-grid resolution with the genuine angular-Einstein effect. Report
  M_MS ~ 0.289 (gate-grid 3-D value); a clean physical refinement claim awaits a grid-converged
  radial reference + a finished 3-D grid bump (the lstsq path is slow at larger grids).
- SH-exact theta op validated in ISOLATION only; the coupled-solve integration is a Phase-3 gate.
- TRACTABILITY: the explicit-Jacobian path is exact but the augmented lstsq cost grows fast
  (32x10x8 ~ minutes/iter; 28x10x8 grid-bump did not finish in 25 min). Phase 3 may need the
  batched-jacrev Jacobian assembled + a sparse/iterative direct solve, or block-SCF, for larger
  grids and the winding search.

## COMPLETENESS-MAP IMPACT (the ten criteria)
- COVERS: criterion-10 tractability for the OFF-ROUND 3-D coupled solve (the gap isolated at #60
  is closed for convergence); criteria 1-5 for the round/near-round 3-D class now to ~1e-12 incl.
  the angular Einstein eqns; continuation infrastructure for criterion-8 traversal.
- STILL BLANK: criterion-6 (winding m>=2 shapes — seeds exist, not mapped), criterion-8
  (branch/bifurcation = the CATALOG — the perturb-relax null is NOT a catalog verdict),
  criterion-9 (stability spectrum off-round). These are Phase 3.
- Regime of validity: validated at p~0.4, kap8~0.05, grids to 32x10x8; off-round convergence
  demonstrated on perturbations (relaxed back) — the genuine-winding regime is untested.

## STANDING-QUESTION ANSWERS (push: off-round solver)
1. COVERS: off-round convergence (tractability) + full-3-D round to 1e-12. DROPS: the genuine
   winding/non-axisym catalog SEARCH, off-round stability, the SH-exact-theta coupled integration.
2. Dropped criterion hosting structure? YES — criterion-8 (catalog) is exactly the open prize;
   this push only gives the TOOL to search it, not the search. Flagged blind-spot, not a closure.
3. REGIME: p~0.4, kap8~0.05, grids <=32x10x8; perturbative off-round only.
4. Category-A only? YES — value-equivalent to 1.4e-14; B=1/A free; verified GPU==CPU. No category-B.
5. Tooling next: wire SH-exact theta + amplitude-scaled winding seeds + continuation => Phase-3
   catalog search; faster Jacobian assembly for larger grids.
6. ONE tile: the catalog VERDICT is still BLANK; what is newly filled is the off-round SOLVER
   (the #60 wall) + the full-3-D round solution to 1e-12.

## PROVENANCE
Build agents: af442a3b0e3c88257 (Newton), a01d74a8b7d103773 (SH-theta), a854463189f03b1a1 (divT).
Verifier: a57302bada835a340. Audit base: INFRA-AUDIT #2 (a395.../a152.../a643...).
