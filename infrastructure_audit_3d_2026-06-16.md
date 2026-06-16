# Infrastructure Audit #2 — Full-3-D Spectral Machinery (#60) — 2026-06-16

**Auditor:** Claude (Opus 4.8, 1M), driving, via THREE concurrent independent
verifier agents (Einstein side / matter side / contamination+off-round).
**Method:** adversarial, independent; each agent re-ran the code and reported
actual numbers, not claims. GPU (V100, float64) + CPU spot-checks. DATA-BLIND.
**Trigger:** HANDOFF flagged the #60 full-3-D machinery as NOT independently
audited (its final summary was lost to an API error) — verifier-first before
building the Phase-2 off-round solver on it. Standing proactive infra-audit
practice (Charles, 2026-06-16) + [[audit-solving-infrastructure]].

**Scope (files):** full3d_spectral.py, full3d_solver.py, full3d_campaign.py,
full3d_final_run.py, einstein_3d_weyl_gen.py / gen_einstein_3d_weyl.py /
einstein_3d_eval.py, matter_el_3d_gen.py / gen_matter_el_3d.py, spectral_3d.py,
spectral_sph.py.

---

## HEADLINE VERDICT: TRUSTWORTHY TO BUILD ON — with 3 premise corrections + 1 must-fix

The #60 base is CLEAN of contamination and the core algebra is exact. But three
things previously recorded as "round gate PASS at machine zero, div(T) exact" are
CORRECTED below, and one operator must be wired in before higher-winding work.

---

## 1. CONTAMINATION SCAN — CLEAN (no category-B)

No recurrence of the two historical scars, and no new smuggled physics:
- **B=1/A (g_tt=1/g_rr) NOT tied.** Metric built from independent warps a,b
  (full3d_spectral.py:42-45,162-165). Residual imposes (t,t) and (r,r) Einstein
  eqns SEPARATELY (full3d_solver.py:76-89). `a=-b` appears only as the radial SEED
  (spectral_radial_soliton.py:173, comment "freed by solve"); the converged state
  does not hold it. Verified numerically.
- **No injected/seal source.** Stress is the literal Hilbert variation
  T = xi*G + kap*C + g*L (whole_metric_3d_matter.py:99-105); residual is exactly
  Gmix - kap8*Tmix. No mass-smear / seal-injection term.
- **No linearization-as-result.** GN/LM is the linear step; the accept test checks
  the FULL nonlinear Phi decreases (full3d_solver.py:188,212). Matter EL = autograd/
  analytic variation of the true action.
- **No dialed M_MS.** M_MS is a pure diagnostic output; nothing feeds a target back
  into the residual. Only physical dials are p (depth) and kap8.
- **No Cholesky-broadcast pitfall** anywhere in the stack (uses torch.linalg.inv
  with the explicit V100 note, and dense solve / Jacobi-PCG).

## 2. EINSTEIN ALGEBRA — EXACT (trustworthy)

- (a) FLAT -> max|G| = 0.000e+00 EXACTLY (pole structure cancelled symbolically
  pre-numerics), all resolutions.
- (b) SCHWARZSCHILD -> vacuum G exp-convergent in Nr (2.05e-3 @Nr16 -> 4.15e-7
  @Nr48); INDEPENDENT from-scratch sympy Christoffel/Ricci/Einstein cross-check of
  all 16 components at 25 random fully-3-D points: max diff 2.4e-15 (algebra
  correct, not merely vacuum-nulling).
- (c) Axisym config in the 3-D psi-live basis MATCHES validated 2-D engine:
  3.4e-14 (grid) / 1.9e-14 (200-pt pure-algebra). psi-deriv of psi-flat field = 8e-17.
- (d) Pole-stable: true-vacuum max|G| FLAT at 4.08e-6 as Nth 6->28 (min sinθ 0.084);
  no NaN/Inf. The analytic cure does not grow at the poles where a naive NR engine would.

## 3. MATTER EL — CORRECT (trustworthy)

- Machine-zero on round: max|EL| body 3.7e-12 (Nr48) .. 6.0e-11 (Nr64), refinement-stable.
- 3-D EL restricted to axisym == corrected 2-D EL (axisym_matter_el_CORRECT.py),
  BIT-EXACT (0.0) over 2000 random off-round points; does NOT reproduce any off-round bug.
- Independently = the action's true variation: analytic matter_el_3d vs continuum
  autograd, ratio -0.99998 off-round (all angular components nonzero).

---

## PREMISE CORRECTIONS (things prior #60 notes overstated — fix the record)

**C1. The off-round WALL is the SOLVER, not the physics — and the CURE is demonstrated.**
- Matrix-free Jacobi-PCG LM (full3d_solver.py:103-149, 199-223; 6-probe Hutchinson
  Jacobi precond) CRAWLS: Phi 1.7e3 -> 1.6e-5 then ~halves per 10-iter block. No hard
  floor — just linear convergence on ill-conditioned J^TJ (steep core x 1/r^2,1/r^4 x
  Chebyshev; the diagonal precond can't tame it).
- DENSE LM (dense_lm_solve, jacobian_dense; full3d_solver.py:152,167) on the SAME
  physics: Phi 4.0e2 -> **7.4e-13 in 16 iterations (QUADRATIC)**, driving (θθ),(ψψ) to
  machine zero. => a true full-3-D solution PROVABLY EXISTS at the floor; the matrix-free
  CG simply never reached it.
- The axisym CONTROL (#59 relaxes it fine) ALSO fails matrix-free but SUCCEEDS dense =>
  isolates the wall to the solver, NOT to non-axisymmetry or the physics. Category-A.

**C2. "Round recovered at machine zero in 3-D / gate PASS" was OVERSTATED — it's ~1%.**
- The radial #56 slice imposes only (t,t),(r,r),EL and explicitly does NOT impose the
  ANGULAR (θθ) Einstein eqn (spectral_radial_soliton.py:45 "Bianchi consistency check,
  NOT imposed"). That check FAILS: max|res_θθ| = 0.21 on the converged radial soliton.
- In full 3-D that equation is LIVE, so the round seed carries ~1% per-component
  residual (G^r_θ=4.2e-2, G^r_r=2.4e-2, EL=1.3e-2) until c,d warps relax. The reported
  "Phi=3e-4" is the SUM of squared body residuals, not a per-component floor.
- M_MS = 0.2808-0.2809 (vs 1-D ref 0.2812) IS real and confirmed. But the honest
  statement is "round recovered to ~1%, M_MS≈0.281", NOT "machine-zero gate PASS".
  The dense Newton (C1) is what actually drives it to machine zero.

**C3. The committed div(T) conservation GATE is BROKEN (no real evidence).**
- divT_identity (full3d_spectral.py:350-380) spectrally differentiates sqrtg*T (a steep-
  core product) with NO core-edge excision => O(N^2) Chebyshev edge amplification:
  body max divT^r DIVERGES with resolution (6.4 -> 19 -> 92 -> 340 for Nr 48/64/96/128)
  while EL stays machine-zero. The gate demonstrates nothing; the EL's stress-consistency
  rests on the autograd identity instead. NEEDS a core-excised rewrite before any Phase-3
  stability/conservation check.

## MUST-FIX BEFORE HIGHER-WINDING (Phase 2/3)

**M1. The live θ operator is NOT spectrally exact for m≠0.** spectral_sph.py:50-59 is the
Legendre `-sinθ·d/dμ`, exact only for polynomials in μ (m=0/axisymmetric). For genuine
azimuthal winding (m≠0, sin^|m|θ profiles) it is INEXACT. An SH-exact operator WAS written
(spectral_3d.py:107-139, sh_dtheta_matrix via pinv) but is UNWIRED (spectral_3d.py imported
by nothing). => wire the SH-exact θ operator in (or verify error is negligible at working
modes) before trusting higher-winding off-round shapes — else the winding-3 target sits in
the operator's inexact regime.

## DEAD/MISLEADING CODE (latent, not affecting current results)
- full3d_spectral.py:262-270 `matter_action`: references undefined `n`, shadows dV =>
  NameError if ever called. Not on the live path. Remove/fix.
- full3d_spectral.py docstring (24-33) "MATTER EL by AUTOGRAD": the live solve uses the
  ANALYTIC matter_el_3d (full3d_spectral.py:335, full3d_solver.py:68). Misleading provenance.
- spectral_3d.py entirely dead (unwired); the SH-exact operator there is the M1 fix source.
- axisym_matter_el.py (the documented "buggy" L4 file) now evaluates BIT-EQUAL to
  axisym_matter_el_CORRECT.py (max diff 2e-13 on ~1100) — the textual bug no longer
  produces a numerical disagreement on the committed file. (3-D-vs-CORRECT = 0.0 regardless.)

---

## CONSEQUENCE FOR PHASE 2 (off-round static solver)
The fix is essentially PROVEN: replace the matrix-free Jacobi-PCG with Newton on an
explicit Jacobian + direct factorization (the dense path already converges to 7e-13
quadratically). Scale it to production grid by BATCHING the Jacobian (torch.func.jacrev/vmap
with a manual 4x4 cofactor inverse to dodge the vmap+linalg.inv issue), or Newton-Krylov
with a real elliptic preconditioner, or block/alternating SCF (KEH). State vector
u = pack(a,b,c,d,Th) (five (Nr,Nth,Nps) fields); residual F = residual_vector(u,G,p,kap8,m,wbc)
(full3d_solver.py:42-91). Entry points jacobian_dense (:152), dense_lm_solve (:167).
ALSO carry M1 (SH-exact θ) and a fixed div(T) checker (C3) into Phase 2/3.

## Verifier agent IDs (for provenance)
Einstein: a395acd674a403347 · Matter+gate: a152fdf565ed84ec2 · Contam+off-round: a643fb7f8615bf791.
Throwaway check scripts in /tmp (not committed): verif_einstein3d.py, verif_spectral.py,
verif_pole2.py + the agents' off-round dense-vs-matrixfree probes.
