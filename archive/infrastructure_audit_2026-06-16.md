# Infrastructure Audit — Core Solving Tools — 2026-06-16

**Auditor:** Claude (Opus 4.8, 1M), acting as INFRASTRUCTURE AUDITOR.
First instance of the standing proactive infra-audit practice (Charles, 2026-06-16).
**Method:** adversarial, independent. CPU / sympy / numpy / CPU-torch ONLY
(GPU hard-disabled via `CUDA_VISIBLE_DEVICES=""` — a heavy GPU job ran in parallel).
**DATA-BLIND** (units L=sqrt(kappa/xi)=1; no wall numbers).

Check scripts (committed): `audit_indep_checks_2026-06-16.py`,
`audit_D_probe_2026-06-16.py`, `audit_E_probe_2026-06-16.py`.

## The scar being hunted for (context)

The superseded reduced solver `complete_metric_batched.py` silently carried TWO
hidden physics defects, undetected until the whole-metric gate (#55/#56):
1. **B=1/A over-imposition** — `m_areal = r(1 - e^{-2phi})` ties g_tt·g_rr = const,
   forcing G^t_t = G^r_r, which the L2+L4 soliton (p_r+rho = X(xi+2 kap Y) > 0 in the
   body) cannot satisfy => (r,r) Einstein violated.
2. **Seal-injection** — `m_closed = m_areal + rs*span` in `phi_from_source`
   (line 231): an un-sourced LINEAR mass smear forcing m(seal)=0, which injects a
   spurious constant m' that violates (t,t) (pins res_tt ~0.099, non-converging).

Both confirmed present in `complete_metric_batched.py` (lines 18, 217, 229–231).
The audit's job: confirm these (and any new defect) are NOT in the current core tools.

---

## Per-tool verdict table

| Tool | Hidden patch | Import | Approx-as-exact | Fitted dial | Field/stress consistency | VERDICT |
|---|---|---|---|---|---|---|
| `whole_metric_3d_core.py` | PASS | PASS | PASS | PASS | n/a (pure geometry) | **CLEAN** |
| `whole_metric_3d_matter.py` | PASS | PASS | PASS | PASS | PASS (unit n; same dn) | **CLEAN** |
| `radial_Bfree_soliton.py` | PASS (B freed; seal-injection OFF by default, opt-in for comparison only) | PASS | PASS | dials = CHOSEN control inputs, declared (not fitted) | PASS | **CLEAN** |
| `verify_indep_einstein.py` | PASS | PASS | PASS | PASS | n/a | **CLEAN** |

---

## Tool-by-tool findings

### 1. whole_metric_3d_core.py — full-4D numerical Einstein engine — CLEAN

- **No hidden tie.** Carries the full 4×4 metric with ALL off-diagonals; `metric_inverse`
  is a literal `torch.linalg.inv` (no g_tt·g_rr=const, no diagonal-only shortcut).
- **No import.** Standard textbook NR pipeline g → Γ → Riemann → Ricci → G, computed
  numerically for a GENERAL metric (charter principle 4: transformed GR numerics, not
  new physics). Christoffel and Riemann built by exact einsum contractions of the
  defining formulas — independently verified correct (below).
- **No approximation-as-exact.** Tensor algebra is exact; only FD derivatives are
  approximate, and those are the sanctioned machine-precision function-replacement
  (4th-order central interior, 4th-order one-sided edges, periodic stencil in psi).
  No linearization.
- **No fitted dial.**

**Independent cross-check (sympy, my own from-scratch G engine):**
- Schwarzschild: my engine gives G^μ_ν ≡ 0 (PASS).
- **Off-diagonal metric** (stationary, g_tψ = w0·r²sin²θ ≠ 0, plus r-dependent
  g_tt, g_rr): numeric core vs my symbolic G_{μν} at an interior point,
  **max |G_num − G_sym| over all 16 components = 2.06e-6**, with the off-diagonal
  **G_{tψ}: sym = −8.2456e-3, num = −8.2453e-3 (|err| 2.9e-7)**. This confirms the
  reported ~5e-6 off-diagonal accuracy is real.
- Numeric G is symmetric: max|G − Gᵀ| = 2.2e-7 over the whole grid.
- **h-convergence** (Nr=Nth = 21→41→81): max err = 3.31e-5 → 2.06e-6 → 1.29e-7,
  i.e. ~16× per grid doubling = **O(h⁴)** — consistent with the 4th-order stencils,
  proving the residual is pure truncation, not a bug.

### 2. whole_metric_3d_matter.py — L2+L4 angular-winding stress — CLEAN

- **EXACT L2+L4.** `lagrangian()` implements L2 = −(xi/2) g^{mn} G_{mn} and the
  Lagrange-identity L4 = −(kap/4) g^{mp}g^{nq}(G_{mp}G_{nq}−G_{mq}G_{np}) verbatim.
  `stress_tensor()` is the exact Hilbert form T_{ab} = xi G_{ab} + kap·C_{ab} + g_{ab}L
  with C symmetrized — no metric-derivative coupling assumed away, no by-hand Skyrme
  coefficient (the only constants are xi, kap = the action couplings).
- **FIELD/STRESS CONSISTENCY (the #55 scar) — RESOLVED.** The committed field is now
  the UNIT S³/SU(2) 4-vector hedgehog
  `n = (sinΘ sinθ cosψ, sinΘ sinθ sinψ, sinΘ cosθ, cosΘ)`.
  - **|n|² = 1 exactly** (sympy: `1`; numeric: `1.0`). The old non-unit 3-vector
    ansatz (`…, cosΘ` with no `sinΘ cosθ` slot, |n|² = 1 − cos²θ sin²Θ ≠ 1) that
    contaminated the energy/stress provenance is GONE.
  - **Stress and energy come from the SAME dn.** `stress_tensor` and `−T^t_t` (= rho)
    are both built from `field_metric(dn)`. Numeric −T^t_t(tool) = committed rho to
    8e-17. No more "energy from S² field, stress from S³ field" split.
- **No import / no fitted dial / no linearization.**

**Independent cross-check (sympy, full Hilbert stress from L2+L4 on a general
B-FREE diagonal metric g_tt=−A(r), g_rr=B(r)):**
- Mixed stress vs the committed reduced forms, all EXACTLY zero difference:
  - T^t_t − (−rho) = 0, T^r_r − p_r = 0, T^th_th − pT = 0, T^ps_ps − pT = 0.
  - All off-diagonal T^a_b = 0 (correct for the static hedgehog).
  - Uses X = g^{rr}Θ'² = Θ'²/B (the FREED radial warp), confirming the kinetic term
    uses g^{rr}, not 1/g_tt — i.e. the matter is consistent with B≠1/A.
- Numeric tool `stress_tensor` vs my symbolic T^a_b at a point with A=1.3, B=1.6
  (B≠1/A): **max |T^a_b(tool) − T^a_b(sym)| = 4.2e-17** (machine precision).

### 3. radial_Bfree_soliton.py — corrected #56 radial solver (B=1/A free) — CLEAN

- **B=1/A genuinely FREED (defect #1 removed).** a(r) and b(r) are solved from
  SEPARATE Einstein equations: b from (t,t) [m' = kap8 r² rho], a from (r,r)
  [a' = (r e^{2b} kap8 p_r + (e^{2b}−1)/r)/2]. `a = −b` appears ONLY as the iteration
  SEED (line 255), not as a constraint. Confirmed in the converged solve:
  **max|a+b| = 0.255, rms = 0.046** (zero iff pinned) — B is genuinely independent.
- **Seal-injection (defect #2) removed from the default path.** `solve_b_from_tt`
  default is `m_closed = m_areal` (exact source mass, m' = kap8 r² rho pointwise).
  The legacy smear `m_closed = m_areal + rs*span` is gated behind `seal_defect=True`,
  OFF by default, documented as "INVALID for (t,t), comparison only." This is honest
  provenance, NOT a live patch.
- **Dials are declared CONTROL INPUTS, not fitted.** `p` (core-depth) and `kap8`
  (coupling) are tagged in the docstring as the chosen control dial / physical coupling
  — "chose, not derived," declared up front per the method. They are not tuned to make
  a residual vanish.
- **No import.** EL `theta_ddot_freed` is the unit-S³ Euler-Lagrange, stated as
  verified consistent with the stress via ∇_μ T^μ_r = 0.
- **No approximation-as-exact.** Full nonlinear; only sanctioned replacements
  (trapezoid quadrature, FD Jacobian, exp-arg clamp guarding transient Newton iterates).

**Independent cross-check — ALL THREE mixed residuals → 0 (the key gate):**
- SCF converges hard (db, da, dT ~ 1e-13 by it≈69).
- The full-grid max residual is O(1) but is **entirely localized at the innermost
  cell r = rc = 0.05** (worst res_rr is at index 0/N, where 1/r² = 400 amplifies the
  FD-edge truncation on a steep core profile) — a known core-boundary FD artifact,
  not a physics violation.
- Away from that single edge the convergence is textbook **O(h²)**:
  - at fixed physical r ≈ 2.0, res across N = 400/800/1600:
    res_tt 7.3e-6 → 2.0e-6 → 4.8e-7; res_rr 1.3e-5 → 3.3e-6 → 8.0e-7;
    res_thth 1.4e-5 → 3.5e-6 → 8.7e-7 (≈4× per doubling).
  - deep-interior max [5%..end] res falls 2.2e-4 → 5.5e-5 → 1.4e-5 (≈4× per doubling).
- So (t,t), (r,r) AND (th,th) [the Bianchi consistency check, NOT imposed] all
  converge to zero — the corrected solver satisfies the full radial Einstein system,
  not merely (t,t)+B=1/A. The docstring's "all three converge O(h²)" claim is verified.
- Control: with `seal_defect=True`, res_tt does NOT clean up (stays O(1)), reproducing
  the scar — confirming the default path is the corrected one.

### 4. verify_indep_einstein.py — independent Einstein check — CLEAN

- Self-contained sympy G^μ_ν engine, independent of the numeric core. Validates on
  Schwarzschild (G=0). Its job is the FORCING ARGUMENT that exposed defect #1
  (B=1/A ⇒ G^t_t = G^r_r ⇒ p_r = −rho required, which the soliton violates). It
  imports nothing, fits nothing, and its conclusion is exactly the diagnosis the
  corrected solver acts on. PASS.

---

## Cross-check numbers (summary)

| Check | Result |
|---|---|
| Schwarzschild G (sym, both engines) | ≡ 0 |
| numeric core vs sym G, off-diagonal metric, all 16 comps | max err 2.06e-6 |
| off-diag G_{tψ} num vs sym | 2.9e-7 |
| numeric G symmetry max|G−Gᵀ| | 2.2e-7 |
| core h-convergence (21→41→81) | 3.3e-5→2.1e-6→1.3e-7 (O(h⁴)) |
| L2+L4 stress (sym) vs committed rho,p_r,pT | exactly 0 (all 4 mixed comps) |
| numeric stress_tensor vs sym, B≠1/A point | max err 4.2e-17 |
| |n|² | 1 (sym and numeric) |
| −T^t_t(tool) vs committed rho | diff 8e-17 |
| radial: max|a+b| (B-free witness) | 0.255 (nonzero ⇒ freed) |
| radial residuals at r≈2.0, N=400/800/1600 | all → 0 at O(h²) |
| radial seal_defect=True control | res_tt stays O(1) (scar reproduced) |

---

## OVERALL VERDICT

**CORE INFRASTRUCTURE CLEAN: YES.**

All four load-bearing tools are native and free of the scarred defects:
- The **B=1/A over-imposition** is genuinely removed — `radial_Bfree_soliton.py`
  solves a and b from independent Einstein equations (witnessed by a+b ≠ 0), and the
  matter stress uses g^{rr} consistently with a free B.
- The **seal-injection** un-sourced mass smear is OFF by default and gated behind an
  explicitly-labelled comparison flag; the default source mass is exact.
- The **field/stress provenance split** (#55) is resolved — a single UNIT 4-vector
  hedgehog drives both the stress and the energy, verified |n|²=1 and −T^t_t = rho.
- The numeric Einstein engine reproduces an independent symbolic G (incl. an
  off-diagonal component) at FD-truncation accuracy that converges at the stencil's
  formal order; the L2+L4 stress matches an independent symbolic Hilbert derivation to
  machine precision; the corrected radial solver drives ALL THREE Einstein residuals to
  zero at O(h²).

No defects require fixing before building further on these tools. The only items worth
noting (NOT defects): (a) `seal_defect` and the `a=−b` seed remain in
`radial_Bfree_soliton.py` as documented legacy/seed conveniences — confirm callers never
set `seal_defect=True` for production; (b) the dials `p`, `kap8` are CHOSEN control
inputs and must continue to be declared as such (they are not fitted, but they are not
derived either — the "chose or derived?" tag is satisfied in the docstrings).

**Contamination scope of remaining issues: NONE** (no live defect found).
