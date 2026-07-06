# N5d Stage-2b Gate-0 — BLOCKER FOUND; coupled residual NOT implemented (π₂ tile; DESIGN/PROVISIONAL)

**Date:** 2026-07-06 · CAS = sympy · scripts `h4_scripts/n5d_stage2b_gate0.py`,
`h4_scripts/n5d_stage2b_gate0_rho_norm.py`. **π₂ AXISYMMETRIC S² tile ONLY — NOT the π₃ hopfion sector.**
No solver code changed; no pilot; no verdict; no Outcome A/B; no continuum lead. Gate-0 ran BEFORE any residual
edit, per the plan — and it **caught a normalization blocker**, so implementation is HALTED (Gate-0 rule 5).

## Gate-0 results

| Gate-0 check | result |
|---|---|
| **1. Pin shear-kinetic C** by matching certified `n5d_shear` φ-correction `+(1/5Z)e^{−2φ}a2'²` | **C = 1/10** ⇒ `H_shear = +(1/10)e^{−2φ}ρ²a2'²` (i.e. K=−1/5 in the `−(K/2)` form). **PASS.** |
| **3. Same L reproduces `E_s_geom` operator** | `(δS/δa2)/E_s_geom_op = 1/5` (constant) ⇒ **same operator up to overall scale. PASS.** (φ-correction from this L = `−(1/5Z)e^{−2φ}a2'²` exactly.) |
| **4. Off-round matter-H → base H at s=0** | **FAILS as posed — see BLOCKER.** The matter Hamiltonian density from the standard L_m is **−2×** the base H matter integrand (not equal), and independently the ρ-EOM matter force is **−2×** the base's. |

## THE BLOCKER (load-bearing normalization inconsistency)

Using the standard Faddeev–Skyrme matter action `L_m = (ξ/2)g^{μν}∂n·∂n + (κ/4)F²` (the SAME L_m whose `δS_m/δf`
**matches the base f-PDE coefficients exactly at s=0**, Stage-2a §9), the CAS gives:

- **ρ-EOM (rigorous, `n5d_stage2b_gate0_rho_norm.py`):** `my matter force / base matter force = −2` **exactly.**
  My `δS_m/δρ` integrates to `2(ξρI_r − κN²I_4θ/ρ³)`; the base `rho_ode` carries `+(e^{2φ}/4)(ξρI_r −
  κN²I_4θ/ρ³)`, implying `δS_m/δρ = −(ξρI_r − κN²I_4θ/ρ³)` — a factor **−2** off.
- **H matter (Gate-0.4):** the Beltrami matter-H density from L_m is likewise `−2×` the base H matter integrand.

**Interpretation:** the base solver's matter→GEOMETRY coupling is `−½` of the naive Hilbert `T^{AB}=(2/√h)δS_m/
δh` convention. This is consistent with H4_N1's note that the base ρ-EOM matter weight `e^{2φ}/4` "emerges from
the GEOMETRIC W_χ𝒦√h term" — i.e. the matter sources the geometry through the **𝒦 (extrinsic-curvature)
coupling with a specific normalization**, NOT the naive `(2/√h)δS_m/δh`. The base f-PDE (`δS_m/δf`, pure matter,
no gravity coupling) is UNAFFECTED and matches; only the matter→geometry channel carries the −2.

**Consequence for Stage-2b:** the live shear source `Tshear_live = (ρ²/2)T_s` sources the geometry through the
**same matter→geometry channel** as the ρ-EOM term. The blind-verified `(ρ²/2)T_s, +sign` is correct for the
**naive Hilbert** convention — but the BASE solver uses the `−2`-different 𝒦-coupling, so the residual-level
source would be **mis-normalized (≈ factor −2, i.e. ~−(ρ²/4)T_s in the base convention, sign/factor TBD)**.
Implementing `(ρ²/2)T_s` as-is would inject a source that is ~2× too large and sign-inconsistent with the base
ρ-EOM/H. The off-round H matter terms carry the same −2. **⇒ do NOT implement the coupled residual (Gate-0.5).**

## What is NOT blocked (clean, carries forward)

- Off-round **f-PDE** (A, B, pot with e^{±s}) — matches base at s=0, CAS-exact (Stage-2a §9). It is pure
  `δS_m/δf`, no gravity-coupling factor.
- **φ off-round correction** `+(1/5Z)e^{−2φ}a2'²` — certified `n5d_shear`, unchanged.
- **Shear kinetic C=1/10** and the `E_s_geom` operator (Gate-0.1/0.3).
- **T_s sign = +** and the ρ²/2 measure emergence (blind-verified) — correct WITHIN the Hilbert convention; only
  the matter→geometry coupling constant is the open factor.

## Required report items

1. **Files changed:** NONE in the solver. Added: `n5d_stage2b_gate0_report.md`, `h4_scripts/n5d_stage2b_gate0.py`,
   `h4_scripts/n5d_stage2b_gate0_rho_norm.py`. `cell_solver_f2d.py` UNTOUCHED.
2. **K pin:** C = 1/10 (K = −1/5); `H_shear = +(1/10)e^{−2φ}ρ²a2'²`; reproduces the φ-correction + `E_s_geom`.
3. **Matter-H check:** **FAILED** — matter-H (and ρ-EOM matter force) is −2× the base; the base's matter→geometry
   coupling is −½ the naive Hilbert convention.
4. **Test results:** none run — Gate-0 halted implementation before the residual edit (no pilot, no preflight).
5. **Stage-2 pilot allowed next?** **NO.**
6. **Exact blocker:** the matter→geometry coupling normalization factor (base = −½ naive Hilbert; CAS ratio −2 in
   the ρ-EOM and H). The live source `Tshear_live` and the off-round H matter terms must be re-derived in the
   base's actual (𝒦-mediated) coupling convention — pin the factor λ (ρ-EOM gives λ=−½, sign to confirm for the
   shear component), verify against the base f-PDE↔ρ-EOM↔H consistency, THEN re-run Gate-0.4. Only after that is
   the coupled residual safe to implement.

## Topology warning (binding)

π₂ axisymmetric S² tile only. **Cannot bank Outcome A/B for the π₃ hopfion question.** Status: DESIGN /
PROVISIONAL / Outcome D / no A/B / no continuum lead.

**Recommended next gate (Charles):** a focused CAS pass to re-derive `T_s`→`Tshear_live` and the H matter moments
in the base's matter→geometry coupling convention (resolve the −2), independently blind-verified — before any
Stage-2b implementation. This blocker also raises a question worth Charles's eye: whether the base solver's
f-PDE and ρ-EOM/H matter terms are in a mutually consistent normalization, or whether the −2 reflects a latent
base convention (the 𝒦-coupling) that simply must be applied to the new source too.
