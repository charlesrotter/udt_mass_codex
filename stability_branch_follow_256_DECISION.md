# H3 static-mass — 256³ branch-following stability test: DECISION POINT

**Date:** 2026-07-11 · **Branch:** grok · **Status:** PROVISIONAL / decision pending (Charles + collaborating AI)
**DATA-BLIND.** No lepton/hadron/wall/SNe/BAO/CMB/SM targets loaded. EH/metric-only action stays
tagged CONDITIONAL-DERIVED (Lovelock-conditional, not native-dilation-derived — CLAUDE.md trigger #6).

This doc exists so a collaborating AI can weigh in on a genuine methodological fork before ~3 h of
compute is spent. All numbers below are reproducible from the committed scripts + the local (gitignored)
`.npz` fields.

---

## 1. Where we are in Charles's dispatch

Charles (2026-07-11) redirected: **stay at 256³ and do a proper branch-following stability test before
any 384³ escalation.** Verbatim intent:

> Save and M-normalize the lowest negative vector v. Construct both branches n± = normalize(n0 ± εv)
> for several controlled ε, with fixed boundary. Relax each branch for hours using a stronger
> constraint-respecting optimizer — Riemannian L-BFGS, nonlinear CG, or Newton–Krylov — with line
> search and no Derrick rescaling in the final criticality stage. Follow the complete trajectory …
> Determine whether each branch: returns to the original carrier; reaches a lower-energy Q_H=1
> stationary carrier; or undergoes an explicitly resolved lattice topology slip. Replace the short
> Rayleigh iteration with a converged block LOBPCG/Lanczos (rel < 1e-2, pref 1e-3). Do not use the
> known stability of external Faddeev–Skyrme solutions to grade the result. Only afterward test
> higher-order derivatives at 256³ and then 384³ if the negative direction appears tied to lattice
> resolution. [+ Phase C flux correction — see §5.]

## 2. Prerequisite — the eigenmode (DONE, meets spec)

`stability_eigenmode_256.py` — block LOBPCG (bs=4, manual Gram-Schmidt, streamed HVP, FD-of-gradient
HVP verified against exact analytic HVP to 6.5e-10, manual-autograd gradient). At the best-relaxed
carrier (`controlled_best_field.npz`, gradnorm 0.085, Q 0.9918):

- **Lowest mode: λ_phys = −290.70, rel_res = 9.48e-3 (< 1e-2 ✓), core-fraction = 1.0000, M-normalized (vᵀMv = 1).**
- **The negative subspace is a CLUSTER of ≥3 localized modes: λ = −290.7, −269.9, −236.1** (all core-localized).
  A single-vector iteration stalls at rel≈0.11 and *rises* — a block was required (as Charles anticipated)
  because the lowest mode is near-degenerate with the next two.

Saved: `stability_lowmode_256.npz` (v, v1, v2; gitignored, local). `stability_eigenmode_256_out.json`.

## 3. The finding that triggers this decision (smoke test, 25 s/branch)

`stability_branch_follow_256.py` — Riemannian L-BFGS (memory 6, transport-by-projection, backtracking
Armijo line search, fixed asymptotic boundary, **no Derrick rescaling**), 7 branches:
control (δ=0) + ±0.05, ±0.10, ±0.20 relative-L2 displacement along v. A 25 s/branch smoke test (to
validate the harness before the full run) already gave a clear, assumption-breaking result:

| branch | start Q | end Q | ΔE from carrier | class |
|---|---|---|---|---|
| **control (δ=0, UNPERTURBED)** | 0.992 | **0.078** | **−106** | topology_slip |
| p05 / m05 (±0.05·v) | 0.581 | 0.18 / 0.14 | −85 / −89 | topology_slip |
| p10 / m10 (±0.10·v) | 0.464 | 0.16 / 0.16 | −88 / −88 | topology_slip |
| p20 / m20 (±0.20·v) | 0.369 | 0.15 / 0.16 | −87 / −84 | topology_slip |

Carrier reference: E0 = 283.37 (E2 = 140.78, E4 = 142.59), Q0 = 0.9918, gradnorm0 = 0.085.

**Two load-bearing observations:**

1. **The unperturbed control unwinds on its own** (Q 0.99 → 0.08, E −106) under unconstrained strong
   descent. So the topology slip is **NOT caused by v** — it is generic to strong descent on this
   discrete carrier. The control *is* the calibration, and it says the instability is not v-specific.
2. **v is exactly the unwinding direction.** A 5% L2 nudge along v drops Q from 0.99 to 0.58 *before*
   any relaxation; the three negative modes (−291, −270, −236) are the lattice-unraveling directions.

## 4. Interpretation + the methodological catch

Coherent physical picture: **at 256³ the Q=1 carrier is not a stable minimum.** The topology-safe
(arrested-Newton, small-step) descent *stalled* at gradnorm 0.085 precisely because it could not
descend further without unwinding — i.e., the carrier is a constrained shoulder whose one extra descent
direction leads to vacuum. That direction is the negative-mode cluster. Because the real Faddeev–Skyrme
hopfion is known-stable (used here as **contrast only**, per Charles — not as a grade), a genuine
unwinding mode at 256³ is the fingerprint of **256³ under-resolution** (the grid-artifact hypothesis),
now with direct evidence: the control unravels.

**Catch:** a full-step L-BFGS *bolts* to vacuum from any start — the gradient GREW 16× (0.085 → 1.4)
while energy fell. That is falling off a cliff, not settling at a critical point. As literally
configured the test can only ever return "slip"; it never gives the other two dispatch outcomes
("returns to carrier" / "lower-energy Q=1 carrier") a fair chance, because the optimizer never lingers
near the carrier to find them. A **step-size cap / trust region** (still no Derrick rescaling) would let
each branch explore its neighborhood instead of sprinting to vacuum.

## 5. Also done (Charles's Phase C flux correction, point 9)

`discrete_face_flux` in `hopfion_static_mass_common.py` is the **exact one-sided telescoping flux** of
the 7-point Laplacian (not centered): verified `face_flux == Σ_box lap_FD(u)·h³` to |diff| ≤ 2.8e-14
(machine precision) at R = half·h for half ∈ {30,60,90}. Charles's note reflected the pre-correction code.

## 6. THE FORK (for Charles + collaborating AI)

- **Option 1 (Claude's lean): refine, then run the full ~3 h test.** Add a trust-region step cap so
  branches genuinely follow their neighborhood; keep control as calibration; run all branches to full
  budget; record complete trajectories. Faithful to the dispatch AND preserves the "does a nearby
  stable Q=1 carrier exist?" question that Option 2 discards.
- **Option 2: run the full 3 h test exactly as-is.** High confidence it just re-confirms "everything
  slips, control included" at greater length — literal dispatch, lower marginal value.
- **Option 3: pivot now to the resolution test.** The control already answers the discrimination
  (slip is a generic lattice-unwinding artifact, not v-induced) — the trigger Charles named for
  escalation ("384³ if the negative direction appears tied to lattice resolution"). Go to higher-order
  derivatives at 256³, then 384³.

**Open questions for the collaborating AI:**
- Is the "control unwinds too" calibration sufficient to call the negative modes a lattice artifact, or
  is a trust-region branch-follow needed to rule out a nearby lower-energy Q=1 carrier first?
- Does a trust-region cap violate the spirit of "no Derrick rescaling / constraint-respecting," or is it
  a legitimate criticality-search tool (it caps step length, not field scale, and adds no topology
  constraint)?
- Given the negative direction is *already* strongly tied to lattice resolution (control unwinds), does
  the higher-order-derivative test at 256³ add information before 384³, or should we go straight to 384³?

## 8. RESOLUTION — decision taken + STEP 1 result (2026-07-11, Charles + collaborating AI)

**Decision: modified Option 3.** Do NOT spend 3 h on the present operator; do NOT jump to 384³. The
present discrete energy AND hopf_charge use the centered first difference `D^c f=(f_{i+1}-f_{i-1})/2h`
(`fs_hopfion.py:48`), which annihilates the checkerboard mode `(-1)^i` exactly — an operator Nyquist
null that 384³ cannot remove. Ordered plan: (1) audit the negative modes for checkerboard content;
(2) replace the centered energy with a no-Nyquist-null discretization (link/forward-backward or
finite-volume), convergence-tested on smooth manufactured fields; (3) re-solve the carrier;
(4) geodesic-S² perturbations (max-rotation amplitude, Q preserved) + quadratic-regime check of
⟨v,Hv⟩; (5) full trajectories incl. θ_max; (6) trust-region branch test, THEN 256³ vs 384³.

**STEP 1 DONE — `stability_checkerboard_audit.py` / `..._out.json`.** Calibrated (smooth ref R_cb=0.997,
nyq=0.000; pure-checkerboard ref R_cb=0.0001, nyq=1.000). The three converged negative modes:

| mode | λ_phys | R_cb = ‖D^c v‖²/‖D^+ v‖² | Nyquist power frac | verdict |
|---|---|---|---|---|
| v  | −290.7 | **0.0084** | 0.9995 | checkerboard-dominated |
| v1 | −269.9 | 0.0169 | 0.963 | checkerboard-dominated |
| v2 | −236.1 | 0.0135 | 0.998 | checkerboard-dominated |

**The entire negative cluster lives in the centered operator's Nyquist null** (R_cb ≈ 0.01 vs smooth
0.997; >96% spectral power on the Nyquist faces). ⇒ **The "unwinding negative mode" is an OPERATOR
ARTIFACT, not a physical or continuum instability** — and NOT a mere resolution deficit (the null is
exact at any N). The Phase-B "localized negative persists" concern is thereby explained and defused.
Carrier n0 max nearest-neighbor angle = 0.173 rad (smooth).

**STEP 1 BLIND-VERIFIED** (independent agent, own probes + own calibration, adjudicated Nyquist-artifact
vs smooth-physical): CLAIM SUPPORTED in full. Independent numbers — ‖D^c v‖/‖D^+ v‖ = 0.091/0.130/0.116
for v/v1/v2 (= sqrt of my R_cb: 0.091²=0.0083 ✓), Nyquist-face power 0.9995/0.963/0.9975, low-k power
< 0.05%, eigenvectors mutually orthogonal (not degenerate/identical), carrier exactly unit-norm.
Nuance: NN correlations −1/3,+1/3 (alternation along 1–2 axes, not all 3) — near-null, not perfectly
monochromatic, but decisively in the centered null vs the 0.997 a smooth mode gives.

**STEP 2 DONE + validated — `noNull_energy.py`.** A no-Nyquist-null Faddeev–Skyrme energy: the SAME
continuum functional discretized as the average over the 8 one-sided orientations s∈{+,−}³ of the
density built with one-sided differences D^{s_a}_a (symbol nonzero at k=π/h ⇒ no null); 8-fold average
is cubic-symmetric and O(h²)-consistent; fully autograd-differentiable. Manufactured-field tests:
- **(A) Convergence:** on a smooth periodic field, E_noNull and E_centered → the SAME limit (~35.345)
  at O(h²) (Richardson ratios 3.96–3.99 ≈ 4); E_noNull − E_centered → 0 as O(h²). ⇒ valid representation
  of the same continuum energy, NOT a new physical operator.
- **(B) No null:** a pure Nyquist mode (smooth envelope × checkerboard) costs 1.63e5/δ² in E_noNull but
  only 175/δ² in E_centered (centered sees 0.1%). The null is closed.
- **(C)** autograd gradient finite/correct.
**STEP 3a DONE (cheap, decisive) — `noNull_curvature_check.py`.** Quadratic form
q(v)=[E(n0+εv)+E(n0−εv)−2E0]/ε² (→ λ_phys for M-normalized v) along the three old Nyquist eigenvectors,
under both operators (ε ∈ {2e-3,1e-3,5e-4}, quadratic regime clean):

| mode | q_centered (→ matches saved λ) | q_noNull |
|---|---|---|
| v  | −290.70 (saved −290.70 ✓) | **+30769** |
| v1 | −269.86 (saved −269.86 ✓) | **+15454** |
| v2 | −236.10 (saved −236.10 ✓) | **+28784** |

Two results: (i) q_centered reproduces the block-LOBPCG eigenvalues to the digit — an independent
validation that the FD-Hessian + M-normalization + eigensolve are correct. (ii) Under the corrected
operator the SAME directions have LARGE POSITIVE curvature — the negative "unwinding" modes become stiff
stable directions once the operator can see them. **Confirms the negative cluster was an operator
artifact.** (The huge +3e4 is the correct O(1/h²) stiffness of high-frequency lattice modes.)

**STEP 3b PARTIAL (strong qualitative win + a conditioning bottleneck) — `noNull_resolve.py`.**
- **Stage 1 (relax under E_noNull):** 475 L-BFGS iters. **Q stays 0.99 throughout (0.9918→0.9915) — the
  carrier does NOT unwind**, vs the centered operator's unwind to Q=0.08 in ~50 iters. E→275.5 plateau,
  gradnorm→0.061 (L-BFGS oscillating 0.06–0.4). ⇒ removing the Nyquist null removes the unwinding — the
  carrier is topologically stable under the corrected operator.
- **Stage 2 (lowest Hessian mode of E_noNull):** block LOBPCG lowest Ritz value descends monotonically
  from +842 → +74 (it=30, not converged), staying POSITIVE, eigenvector smoothing (R_cb 0.62→0.92);
  lam1,2,3 clustered at ~74–78. **NO negative mode appeared** (the −290 Nyquist artifact appeared within
  ~20 iters before) and the lowest modes are now SMOOTH, not checkerboard.
- **HONEST caveats:** LOBPCG bounds the lowest eigenvalue from ABOVE, so +74 is not converged — a *large*
  negative is excluded, but the *sign of the fully-converged* lowest mode is not yet pinned. Also the
  field is only near-critical (gradnorm 0.061), and both the relax and the eigensolve are ill-conditioned
  by the operator's huge Nyquist stiffness (+3e4; condition number ~300) → slow/oscillatory.

**Provisional read:** the −290 negative cluster was an OPERATOR ARTIFACT (confirmed, blind-verified); the
carrier is topologically stable under the corrected operator; the precise sign of the near-zero lowest
smooth mode at a TIGHT critical point is the remaining rigor, bottlenecked by Nyquist stiffness.

**FORK (Charles + collaborating AI):**
1. Precondition the operator (damp/deflate the +3e4 Nyquist band, or spectral preconditioner) → tight
   critical relaxation + converged lowest Hessian eigenvalue (the rigorous stability number).
2. Proceed BEHAVIORALLY to steps 4–6 now: geodesic-S² perturbations along SMOOTH modes + trust-region
   branch relaxation under E_noNull — directly tests return-vs-slip (Stage 1 already shows no unwind).
3. Both, in parallel.

## 7. Reproduce

- Eigenmode: `RESUME_EIG=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True timeout 2400 python3 stability_eigenmode_256.py`
  (warm-starts from the saved v; converges rel<1e-2 in ~30 block iters). Launch via a live `timeout … python3`
  command — NOT `nohup … &` (the latter's process group gets cleaned up early in this harness).
- Branch-follow smoke: `BRANCH_BUDGET_S=25 python3 stability_branch_follow_256.py`. Full run: set
  `BRANCH_BUDGET_S=1500` (25 min/branch). HVP/gradient use manual autograd (functorch leaked at 256³).
- V100-32GB, float64. Memory is stable ~22–25 GB (verified flat by `scratchpad/memdiag*.py`); the
  earlier "OOM deaths" were a cuSOLVER tall-QR spike (fixed by manual Gram-Schmidt) + the nohup issue.
