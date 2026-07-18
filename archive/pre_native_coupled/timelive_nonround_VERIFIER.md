# BLIND VERIFIER — Time-Live Non-Round Native Solve (structural-first)

**Verifier agent:** claude-opus-4-8[1m] (blind adversarial). **Date:** 2026-06-19.
**Target:** `archive/pre_2026-07-01/timelive_nonround_native_solve_results.md` (constructor) + the three load-bearing claims.
**Method:** independent re-derivation. Did NOT run/trust the constructor's scripts; built my own
sympy symbolic derivations (full Christoffel->Ricci->Einstein from scratch for Claim 2) and an
independent numpy `eigvalsh` self-adjoint finite-volume eigensolver (different assembly than the
constructor's) for Claim 3. Data-blind (no empirical masses). No git commit.
**Scripts:** `timelive_nonround_verif_claim1.py`, `timelive_nonround_verif_claim2.py`,
`timelive_nonround_verif_claim3.py`.

---

## CLAIM 1 — the angular nonlinearity variation is a DRIFT, not a binding potential — **STANDS**

Independent sympy:
- **(a)** `d/d_eps[ -(v_theta)^2 ]|_0 = -2 v0_theta u_theta` **EXACTLY** (symbolic identity, zero residual);
  about a round background (`v0_theta = 0`) it is **EXACTLY ZERO** — B2 reproduced.
- **(b)** Operator `A[u] = u'' + p u'` with `p = cot(theta) - 2 v0_theta` is self-adjoint in weight
  `w = sin(theta) e^{-2 v0(theta)}`: I confirmed `w'/w == p` symbolically AND that
  `w*A[u] - (w u')' == 0` identically. The new term is absorbed by the weight change `sin -> sin e^{-2v0}`.
- **(c) ATTACK (the decisive one):** a first-order drift in a real self-adjoint 1D operator **cannot**
  create a bound state or flip the sign by itself. Proof: the Liouville form makes the operator
  `L = (1/w) d_theta(w d_theta)`, whose quadratic form is `<u,Lu>_w = -INT w (u')^2 dtheta <= 0` for any
  real bounded `v0` (since `w = sin th e^{-2v0} > 0` on `(0,pi)`). Numerically confirmed: with drift
  amplitudes 0, 0.5, 2.0, 5.0 the maximum eigenvalue of `L` stays strictly negative
  (-0.13, -0.16, -0.52, -1.40) — **no positive (bound) eigenvalue ever appears**, however strong the drift.

**One-line reason:** the variation is exactly `-2 v0_theta u_theta`, exactly zero round, and is a pure
weight-reshaping drift that keeps the operator sign-definite — a drift cannot bind. CONSTRUCTOR ACCURATE.

---

## CLAIM 2 — time-live converts sign-definite damping to omega^2>0 standing waves — **STANDS**

- **PART A (the logic):** wave eqn `M u_tt = L_space u` with `L_space = -l(l+1)W < 0` (the wcc/B2 damping)
  and `M > 0` gives, under `u = U e^{i omega t}`, `omega^2 = -L_space/M = l(l+1)W/M > 0`. Sign-definite-NEGATIVE
  `L_space` + positive `M` + a **hyperbolic** (`-omega^2`) time term **does** give `omega^2 > 0` (real
  standing wave). The verdict hinges entirely on the d_t^2 sign — tested in Part B.
- **PART B (ATTACK — recompute the d_t^2 sign FROM SCRATCH):** I rebuilt the full Christoffel -> Ricci ->
  Einstein for the l=2 quadrupole warp `g_thth = r^2(1+eps h P2)`, `g_psps = r^2 sin^2 th (1-eps h P2)` on a
  flat round background, independent of the constructor. To O(eps):

  ```
  coeff(h_tt) = r^2 (3cos^2 th - 1) / (4 c^2)      [nonzero, theta-weighted by P2, survives projection]
  coeff(h_rr) = r^2 (1 - 3cos^2 th) / 4
  coeff(h_tt) / coeff(h_rr) = -1/c^2   (EXACT)
  ```

  The d_t^2 and d_r^2 terms have **OPPOSITE relative sign** with ratio exactly `-1/c^2` — a **Lorentzian
  WAVE operator** of speed c, **NOT** a diffusion/elliptic operator (which would give `omega^2 < 0` = decay).
  My from-scratch `G_thth` matches the constructor's quoted expression term-for-term.

**One-line reason:** the d_t^2 coefficient is `r^2 P2 / c^2` (nonzero, gauge-invariant/radiative) and its
ratio to d_r^2 is exactly `-1/c^2` — a genuine hyperbolic wave, so `omega^2 = l(l+1)W/M > 0`. CONSTRUCTOR ACCURATE.

---

## CLAIM 3 — intrinsic centrifugal FLOOR + box-controlled CONTINUUM, no bound tower — **STANDS** (with a sharpening)

Independent eigensolver (self-adjoint finite-volume `eigvalsh`, my own assembly; not the constructor's FD).
Profile `v0 = -0.4 e^{-r}` (and variants), inner Dirichlet, seal Dirichlet/Neumann.

- **(a) floor R-independent — STANDS, and is CLEANER than reported.** With the constructor-style scan
  (rmin and h scaling with R) the floor drifts mildly (l=1: 1.97->1.99; l=3: 9.87->10.25 over R=8..512).
  I traced this to a **discretization artifact** (inner cutoff + grid spacing both moving with R). Holding
  rmin=0.02 and h=0.04 FIXED and varying only R, the floor is **R-independent to 5 decimals** once R
  contains the core (l=1: 1.97440 flat at R=32,128,256; l=3: 9.91471 flat). So R-independence is GENUINE
  and the residual drift the constructor showed was numerical, not physical. (Minor UNDER-claim: the
  constructor presented a noisier flat than the physics actually delivers.)
- **(b) Q=0 floor ~ l(l+1) W_inf — STANDS.** l=1: 1.974 vs 2.0; l=2: 5.36 vs 6.0; l=3: 9.87 vs 12.0. The
  shallow attractive core dips it slightly below the bare barrier, more for higher l — exactly as stated.
- **(c) band spacing -> 0 as R grows — STANDS.** l=1 gap(omega2_2 - omega2_1): 0.107 (R=16) -> 0.043 (32)
  -> 0.029 (64) -> 0.024 (128) -> 0.019 (256). Box-discretized continuum confirmed.
- **(d) ratios ~ sqrt(l(l+1)/2) — STANDS (approx).** omega_l/omega_1 = 1.00, 1.66, 2.25, 2.82 vs
  1.00, 1.73, 2.45, 3.16. Close, trending below the bare-barrier ratio because the core well deepens the
  dip with l (consistent with (b)). Constructor reported the same approximate match honestly.

**KEY ATTACKS:**
- **(i) Q proxy:** with Q=0.5 e^{-r} the floor shifts (->2.000) but stays R-independent (2.00149 @ R=32,
  2.00003 @ R=128,512). Not the artifact.
- **(ii) non-asymptoting exterior** (`v0 = -0.4 e^{-r} + 0.05 ln(1+r)`, no flat W_inf): the floor VALUE
  moves (~2.236) but **R-independence SURVIVES** (2.236 @ R=8, 2.235 @ 32, 2.246 @ 128, 2.283 @ 512 —
  the slow rise is the log exterior the cell is now sampling, i.e. genuine local-potential content, not the
  wall). This is the constructor's own predicted outcome: "floor value moves but R-independence persists,
  since it is the potential floor not the wall." Confirmed.
- **(iii) BC:** Dirichlet vs Neumann seal agree to 5 decimals (1.97238 vs 1.97237 @ R=32; identical @
  R=128,512). The floor is NOT a boundary artifact.

**One-line reason:** the floor is the intrinsic `l(l+1)`-centrifugal potential value (R-independent, BC-robust,
survives a non-flat exterior with only its value moving), while the levels above it are a box-discretized
continuum (spacing -> 0). No discrete bound tower. CONSTRUCTOR ACCURATE; if anything the R-independence is
sharper than shown.

---

## OVER/UNDER-CLAIM NOTES

- **UNDER-claim (Claim 3a):** the constructor's tabulated floor showed ~1% R-drift that is a pure
  discretization artifact; the true physics floor is R-independent to <1e-4 when the grid is held fixed.
  The constructor's conclusion is correct and actually conservative.
- **No over-claims found.** The doc correctly does NOT bank a discrete mass ladder, correctly flags the
  box-continuum levels as box-controlled, correctly identifies the intrinsic floor as the already-banked
  angular `l(l+1)` (charge) discreteness rather than a new bound spectrum, and honestly tags both shortcuts
  (modeled radial v0; full coupled solve unbuilt). The two SHORTCUTS do not change any structural verdict I
  could reproduce — the structural conclusions follow from sign-definiteness (Claim 1) + the wave-sign
  (Claim 2) + the SL floor/continuum structure (Claim 3), all of which I confirmed independently.
- **Caveat carried forward (not a refutation):** the ABSOLUTE floor value rides on the modeled exterior
  W_inf, as the constructor states; my attack (ii) confirms the value is profile-dependent while the
  STRUCTURE (R-independent floor + box continuum, no bound tower) is profile-robust. The one place a bound
  WELL could still appear — the fully-coupled nonlinear-amplitude back-reaction — is genuinely unbuilt by
  both constructor and verifier, and is correctly listed as OPEN, not closed.

---

## NET VERDICT

| Claim | Verdict |
|---|---|
| 1 — `-v_theta^2` variation is a drift, not a binding potential (cannot bind) | **STANDS** |
| 2 — time-live (hyperbolic d_t^2, ratio -1/c^2) gives omega^2 > 0 standing waves | **STANDS** |
| 3 — intrinsic centrifugal floor + box-controlled continuum, no bound tower | **STANDS** (R-independence cleaner than reported) |

All three load-bearing claims survive independent adversarial re-derivation. The headline — time-live
non-round revives the dead static operator into a real standing-wave eigenproblem with an INTRINSIC floor
that is the already-banked angular `l(l+1)` (charge) barrier, a BOX-CONTROLLED continuum above it, and NO
new discrete bound mass tower — is **CONFIRMED**. The generations discretizer remains genuinely missing;
the constructor's "half-open / PARTIAL" framing is honest and not over-sold.
