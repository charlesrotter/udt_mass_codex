# E2c — OPTIMIZER HARDENING for the coupled composite solver

**Date:** 2026-07-04. **Owed step:** PURSUIT_CHARTER_2026-07-04 §5 (E2c: "globalization / deflation
/ extended-precision / explicit soft-direction (dilation-slide) handling; CERTIFICATION = the MMS
gauntlet from seed-class distances to max|F|≤1e-8"). **Category:** A (numerical conditioning — making
the UDT equations solvable; the always-green lane). **No physics/equation change** — the composite
residual `residual_comp` is untouched. **Data-blind** (synthetic MMS problem; no observational numbers).
**pytest 32/1xfail** (unchanged; `lm_hardened` is an added function, `lm_qr` and the pure-universe
recovery are byte-identical). **Scripts (committed with this doc, NOT run as the sweep):**
`cell_solver_composite.py` (added `_ruiz_equilibrate` + `lm_hardened`), `e2c_mms_certification.py`.

---

## 1. SHARPENED DIAGNOSIS (solver-first on our own numerics; the purest cure per flaw)

Rebuilt the MMS gauntlet (manufactured composite state `v*` with an EXACT root guaranteed by
forcing-subtraction `resfn(v) = residual(v) − residual(v*)` — same Jacobian and stiffness as the
physical system) at the production grid (Nr=12, Nθ=8, Na=192, kmap=2.5, n=506). Reproduced the
documented ~1e-3 radius (baseline `lm_qr`: boundary offset dr=10 floors at max|F|=2.15e-8; a cell
field perturbation of 0.3 stalls at 3.8e-4). Then pinned the failure mode PRECISELY — it is **two
distinct phenomena**, not one:

### (a) The soft dilation-slide = a near-EXACT TRANSLATION GAUGE of the boundary pair
- **SVD of J at the root:** the softest singular direction carries **0.500 / 0.500 energy on
  (r_p, r_sU), ≈0 on all field DOFs**; σ_min ≈ 2.2e-9 vs σ_max ≈ 8.0e7 → **raw cond(J) ≈ 3.6e16 ≈
  1/ε_float64** (numerically singular). Present AT THE ROOT (not a seed artifact).
- **The mechanism (derived, not posited):** the two boundary columns are **exactly anti-collinear**
  — `dF/dr_p = −1.0000·dF/dr_sU` (cos = −1.000000; longdouble finite-difference residual frac 9.7e-5).
  The ambient EOMs (`cell_solver_universe_T3` φ''/ρ'' formulas) are **AUTONOMOUS in r** (no explicit
  r-dependence), so a rigid radial TRANSLATION of the shell [r_p, r_sU] → [r_p+δ, r_sU+δ] with the
  same node values is a near-symmetry — broken only at the ~1e-4 level by the cell coupling at the
  seal (the cell sees r_p explicitly via r=(r_p/2)(ζ+1)). This is the E2a/R1 "99.9%-pure r_sU slide"
  softness, now identified exactly: it is a **translation gauge**, and it is the source of the
  observed **outward boundary drift** in the sweeps.
- **Why the old column-scaled LM could not decide it:** after Ruiz equilibration σ_soft ≈ 4.4e-7
  (equilibrated). A Tikhonov damping λI filters this direction by σ²/(σ²+λ); ANY λ ≳ 1e-13 damps it
  by ~2e-5 (kills the weakly-determined but NECESSARY slide), ANY smaller λ lets a full
  Gauss-Newton step **catapult the shell** (a healthy GN step has scaled-norm ‖y‖≈5; the runaway GN
  step has ‖y‖≈399 and moves r_p 548→1804 in one step). A scalar λ cannot give a *controlled*
  slide step — the razor edge is 1e-14…1e-13.

### (b) Stiffness / conditioning, curable by two-sided equilibration
- Column scaling alone (the old LM) leaves **cond ≈ 5.7e11** (the float64 wall — this is the direct
  cause of the ~1e-3 to 1e-8-edge floors).
- **Ruiz two-sided (row+col) inf-norm equilibration → cond ≈ 1.9e7** (a 4–5 order improvement). Row
  scaling matters enormously because the residual blocks span **1e-19 (fold_phi) to 1e-3 (ambient
  ODE)**; column-only scaling ignores that.

### (c) Float64 residual floor — SECONDARY, not binding
At the MMS root max|F(v*)| = **0.0 exactly** (forcing-subtraction is bit-exact). Near the root the
residual is resolved against terms up to ‖Ψ‖~1e6, so the float64 cancellation floor is ~1e-10 — below
the 1e-8 target. The binding constraint was (a)+(b), not (c). (The GPU/CPU residual paths agree to
~1e-8, which IS the honest achievable floor of this float64 architecture — matching the E2 verifier's
"1e-8 certification floor at the float64 edge.")

### (d) A SECOND, DISTINCT failure axis surfaced by the sharpened gauntlet — the field axis
Perturbing fields component-by-component localizes a stiffness INTRINSIC to the problem:
`phi_c`/`u` perturbations converge to 0.3, `rho_c` to 0.1, but **`phi_a`/`rho_a` (ambient dilaton/
density) EXPLODE the residual** (max|F| 47→1.5e4 at perturbation 0.1) because e^{−2φ} ≈ 1e4 at the
ambient depth φ≈−4.9 (up to ~1e6 in deeper brackets): a 10% dilaton error is a 10% error in a
1e4-scale term. **Combined** field perturbations ≳0.1 descend fast (Phi 6.5e-2→3.1e-6 in ~40 iters)
then hit a **spurious LOCAL MINIMUM of ‖F‖²** (a merit stationary point with F≠0, residual
concentrated in the seal-matching rows C1a/C2 + the f-PDE). Verified genuine: a fresh-Δ restart from
the stall reproduces it, and **pure-GN+line-search hits the SAME minima** — so it is an intrinsic
NLLS property of this stiff coupled system, NOT a conditioning or globalization defect.

---

## 2. THE MATCHED FIXES (each Category-A; soundness check attached) — `lm_hardened`

| Diagnosed flaw | Purest fix applied | Soundness (does it preserve the solution set?) |
|---|---|---|
| stiffness cond 5.7e11 (col-only) | **Ruiz two-sided (row+col) equilibration** each iter → cond 1.9e7 | Diagonal similarity `D_r J D_c`: solving `D_r F(D_c y)=0` has the **same zeros** as `F=0`; it rescales rows/cols, never reshapes. |
| soft translation gauge (σ_min~2e-9), Tikhonov cannot control | **Powell DOGLEG trust region** (GN leg includes the slide fully; Cauchy/steepest-descent leg has ≈0 component along the flat slide, so a dogleg biased toward Cauchy when far **never runs away**; trust radius truncates the ‖y‖≈399 catapult while passing healthy ‖y‖≈5 GN steps) | Trust-region metric = the **TRUE** residual ‖F‖² in col-scaled variables, so the Cauchy leg is a genuine descent direction and the gain ratio is consistent (actual vs predicted both unscaled). No damping of the solution — only step-length control. |
| float64 residual edge | residual + iterate ACCUMULATION in longdouble; `res_hp` extended-precision residual path available (reused from the pure-universe recovery) | Same formulas, higher precision. (The linear `lstsq` stays float64 — this numpy has no longdouble LAPACK path — which after equilibration already resolves the step well below 1e-8.) |
| unphysical steps (r_p≤0, r_sU≤r_p) | boundary POSITIVITY + ORDER guards as trust constraints (shrink Δ, don't accept) | A domain guard (provenance/feasibility), **not** a merit filter — it never judges the shape of a solution, only that the coordinate is physical. |

Reparameterization note (charter §5 "reparameterize/gauge-fix the slide"): the dogleg makes an
explicit gauge-fix UNNECESSARY — it handles the soft translation mode directly in step-length space
without pinning it (pinning would bias the weakly-determined true value). The mixed (r_p, r_sU)
coordinate is kept; the trust region supplies the "treat the soft direction separately" behaviour
the charter called for.

---

## 3. CERTIFICATION TABLE (MMS gauntlet; `e2c_mms_certification.py`; GPU + CPU spot-check)

Two manufactured solutions (a different bracket + a nonzero-bulge root, so it is not a single lucky
point). PASS = max|F| ≤ 1e-8 (GPU) with CPU spot-check ≤ 1e-7. Axes reported SEPARATELY (they have
different intrinsic radii, per §1d).

**MMS#1 (A1 Z=8 wall-slice, n=506).  BASELINE (old `lm_qr`) for contrast:**
| case | ‖v0−v*‖∞ | end max|F| | verdict |
|---|---|---|---|
| boundary dr=10 | 11.0 | 2.15e-8 | FAIL (floats at edge) |
| cell 0.3 | 0.29 | 3.78e-4 | FAIL (stall) |

**HARDENED (`lm_hardened`):**
| axis / case | ‖v0−v*‖∞ | end max|F| (GPU / CPU) | verdict |
|---|---|---|---|
| **boundary (soft-mode) dr=1** | 1.1 | 1.8e-9 / 1.7e-8 | **CONV** |
| **boundary dr=5** | 5.5 | 1.4e-9 / 2.2e-8 | **CONV** |
| **boundary dr=10** | 11.0 | 7.1e-10 / 1.1e-8 | **CONV** |
| **boundary dr=20** | 22.0 | 9.6e-10 / 2.7e-8 | **CONV** |
| **boundary dr=30** | 33.0 | 2.4e-9 / 9.4e-9 | **CONV** |
| cell 0.1 (combined) | 0.10 | 7.7e-4 | fail — spurious ‖F‖² local min (§1d) |
| cell 0.2 / 0.3 / 0.5 | ≤0.49 | 4e-3 / 2.9e-3 / 1.6e-2 | fail — local min |
| ambient 0.02 / 0.05 / 0.1 | ≤0.05 | 3e-4 / 1.2e-2 / 1.5e-2 | fail — intrinsic dilaton stiffness |
| combined cell 0.1–0.3 + dr 5–10 | ≤11.0 | 4e-4 / 2.5e-3 / 1e-3 | fail — field local min |

**MMS#2 (A3 Z=1 plateau-slice + nonzero bulge 0.4, n=506):**
| axis / case | ‖v0−v*‖∞ | end max|F| (GPU / CPU) | verdict |
|---|---|---|---|
| **boundary dr=5** | 5.5 | 4.0e-12 / 2.1e-11 | **CONV** |
| **boundary dr=10** | 11.0 | 1.2e-12 / 1.3e-11 | **CONV** |
| **boundary dr=20** | 22.0 | 5.0e-13 / 3.5e-12 | **CONV** |
| cell 0.1 / 0.2 / 0.3 | ≤0.29 | 8e-3 / 4.2 / 0.33 | fail — field local min |

Single-component field results (separate probe): `phi_c` and `u` perturbations converge to 0.3 at
2e-10…6e-10; `rho_c` to 0.1 at 3.5e-9; ambient components fail from ~0.1. So the field radius is
direction-dependent; the COMBINED field radius is set by the seal-matching local minima.

---

## 4. THE CERTIFIED CONVERGENCE RADIUS + READINESS VERDICT

- **The soft-dilation-slide / boundary axis — THE DOCUMENTED FAILURE MODE that made 0/256 undecided
  (convergence radius ~1e-3) — is DEFINITIVELY FIXED.** Certified radius on the boundary/size axis:
  **≥ 30 in the free boundaries (3× the O(1–10) spec) at max|F| 1e-9…1e-12**, on BOTH manufactured
  solutions. The outward boundary drift is eliminated (dogleg + equilibration). This was the axis
  that defeated every seed in E2 regardless of field distance.
- **The float64 achievable floor is ~1e-8** (GPU/CPU residual agreement), consistent with the E2
  verifier; boundary convergences sit at 1e-9…1e-12 (GPU), 1e-8…1e-11 (CPU) — at or below the target.
- **The field axis is NOT certified to the charter's O(0.3–1.5) target.** Combined field
  perturbations ≳0.1 hit **spurious local minima of ‖F‖²** (residual in the seal-matching C1a/C2 +
  f-PDE rows) — an intrinsic property of local Gauss-Newton/trust-region NLLS on this stiff coupled
  system (VERIFIER-CORRECTED ab6305ce222eee961: dogleg AND pure-GN+line-search BOTH stall short of the root — at DIFFERENT points, ‖·‖∞ ~1e2–1e3 apart — so it is an intrinsic local-NLLS trap that multiple globalizations all hit, NOT a solver defect; the earlier 'same minima' wording was overstated). The ambient dilaton axis is
  additionally stiff (e^{−2φ}~1e4–1e6 at depth) — but the ambient IS the known/banked universe
  scaffolding, seeded accurately, so it is not the uncertain DOF a sweep varies.

**READY for a gated re-sweep — with a scoped, honest boundary:**
- YES for removing the dominant defeater: the re-sweep will no longer return false "no-convergence"
  from soft-mode boundary drift, and convergences it reports will be real (1e-8 floor certified on
  the boundary/size axis and near-field single-component cell structure).
- BUT non-existence STILL cannot be certified from field-distant seeds: the seal-matching local
  minima mean a re-sweep must use **multi-start + continuation/homotopy** (the standard NLLS escape;
  the sweep already varies amp/rp0 — extend with mesh or parameter continuation) and must read
  non-convergence as "not found from these seeds," never "does not exist" (charter trap #1, now with
  a sharper instrument). What remains for a FULL field-axis certification: a continuation driver
  (coarse→fine grid, or a stiffness/source homotopy) layered on `lm_hardened` — a bounded follow-on,
  not a reopening of the physics.

---

## 5. Premise ledger (Category-A conditioning; all provenance/soundness, no merit judgement)
Ruiz equilibration (root-preserving similarity); Powell dogleg trust region (true-metric Cauchy,
consistent gain ratio); longdouble accumulation + optional `res_hp` (same formulas, higher precision);
boundary positivity/order guards (feasibility, not merit). No physics premise changed; `residual_comp`
untouched; the MMS problem is synthetic and data-blind. Grid/iters/trust params are Category-A
soundness knobs (bounded per anti-hang).

## 6. Verifier-before-record
NOT YET blind-verified. A blind adversarial verifier should: (i) re-derive `dF/dr_p = −dF/dr_sU`
independently and confirm the autonomous-ambient translation gauge; (ii) re-run the MMS gauntlet
fresh and confirm the boundary axis converges to ≥30 while the field axis hits ‖F‖² local minima;
(iii) confirm `lm_hardened` changes no physics (residual identical to `lm_qr`'s) and pytest 32/1xfail;
(iv) attack the READY verdict — is the boundary-axis certification enough to call the re-sweep
meaningful, and is the field-axis local-minimum finding correctly scoped (not overclaimed as
nonexistence, not underclaimed as a solver bug).

---

## VERIFIER RECORD (blind adversarial pass — agent ab6305ce222eee961, 2026-07-04): SAFE TO BANK

Independent pass; every load-bearing claim reproduced with the verifier's OWN perturbations/harness.
- **#1 NO PHYSICS CHANGE (the load-bearing check) — HOLDS.** git diff = insertions only, 0 deletions;
  `residual_comp`, `residual_pure`, `lm_qr`, `solve_pure_universe` byte-identical. Ruiz re-derived as an
  invertible diagonal similarity (D_r·J·D_c y = −D_r·F ⇔ J·dx=−F) — root set untouched; dogleg accepts
  only on the TRUE residual ΣF² (no penalty) ⇒ fixed point = F=0, the untouched root (independent CPU
  residual ≤1e-7 confirms CONVs are real roots, never spurious-min false positives); guards only reject
  steps.
- **#2 translation-gauge diagnosis — HOLDS** (cos=−1.000000, anti-collinearity residual 9.73e-5 = the
  ~1e-4 cell breaking; col-only cond 5.67e11, Ruiz cond 1.89e7; Tikhonov dilemma confirmed — one soft
  direction, monotone attenuation, so no scalar λ works; trust region acts on step-length instead).
- **#3 boundary-axis certification — HOLDS** (verifier's own basis: baseline lm_qr dr=10 FAILs at 1.76e-8;
  lm_hardened dr=5/10/20/30 → ~5e-9; builder table reproduced incl. the bulged MMS#2 at 1e-12…5e-13).
- **#4 field-axis intrinsic minima — HOLDS-WITH-CORRECTION** (applied above: dogleg AND pure-GN+LS both
  stall short of the root at DIFFERENT points ⇒ intrinsic local-NLLS trap, not a defect; "same minima"
  reworded). Solver never emits a false CONV here.
- **#5 scoped-READY — HOLDS.** Soft-mode defeater (the 0/256 cause) genuinely removed; boundary CONVs are
  real roots (double-gated); charter-trap-#1 honesty preserved ("not found from these seeds" ≠ "does not
  exist"; field axis needs multi-start+continuation).
- **#6 hygiene — HOLDS** (pytest 32/1xfail; data-blind synthetic MMS; ld_polish flag clarified as
  accumulation-only, applied above — cosmetic).
**VERDICT: the solver is genuinely READY for a gated multi-start+continuation re-sweep; no physics moved.**
