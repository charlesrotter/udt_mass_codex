# N5d Stage-2b Gate-0.5 — matter→geometry coupling RESOLVED: λ = −1/2 (π₂ tile; DESIGN/PROVISIONAL)

**Date:** 2026-07-06 · CAS = sympy · script `h4_scripts/n5d_stage2b_gate05.py`. **π₂ AXISYMMETRIC S² tile ONLY —
NOT the π₃ hopfion sector.** No solver code changed; no pilot; no residual edit; no verdict; no Outcome A/B; no
continuum lead. Resolves the Stage-2b Gate-0 blocker.

## Result: λ = −1/2, CONSISTENT across the ρ-EOM and H ⇒ a deliberate base convention (not an inconsistency)

The base solver's matter action is **`S_m^base = λ·S_m^std` with `λ = −1/2`**, where `S_m^std` is the standard
Faddeev–Skyrme density whose `δS_m/δf` matches the base f-PDE. CAS (`n5d_stage2b_gate05.py`):

| source of λ | value |
|---|---|
| **λ from ρ-EOM** (`λ·δS_m^std/δρ` matches base `+(e^{2φ}/4)(ξρI_r − κN²I_4θ/ρ³)`) | **−1/2** |
| **λ from H matter** (`λ·H_m^std,Beltrami` matches base H matter integrand) | **−1/2** |
| `λ·H_m^std − base_H_matter` at λ=−1/2 | **0** (exact) |

**Both projections give the SAME λ = −1/2, exactly.** Two independent constraints (the trace/ρ channel and the
Hamiltonian) agree, so this is a **deliberate, internally-consistent base normalization** — answer **(a)** in the
Gate-0.5 taxonomy (a K-mediated / geometric-weight convention), **NOT (b) a hidden inconsistency, NOT (c) a mere
sign artifact.** It is consistent with H4_N1's statement that the base ρ-EOM matter weight `e^{2φ}/4` "emerges
from the GEOMETRIC W_χ𝒦√h term" — i.e. the matter sources the geometry through the extrinsic-curvature (𝒦)
channel with strength −½ relative to the naive Hilbert `T^{AB}=(2/√h)δS_m/δh`. The **f-PDE is `δS_m/δf`
(homogeneous), so it is λ-independent and is consistent with any λ** — that is why the f-PDE matched at λ=1 while
the geometry rows require λ=−½; there is no contradiction, only a coupling constant the f-PDE cannot see.

## 3. Corrected live shear source

The shear source is the SAME matter coupling as the ρ-EOM/H, so it carries the same λ:
> **`Tshear_base = λ·(ρ²/2)·T_s = −(ρ²/4)·T_s`**, with `T_s = T^θ_θ − T^ψ_ψ` the blind-verified (Stage-2a §7)
> traceless transverse stress:
> `T_s = (ξ/ρ²)[N²e^{s}sin²f/sin²θ − f_θ²e^{−s}] + (κN²/ρ²) f_r² e^{s} sin²f/sin²θ`.
> Explicit: `Tshear_base = −(1/4)·e^{−s}[ κN²e^{2s}sin²f f_r²/sin²θ + ξ(N²e^{2s}sin²f/sin²θ − f_θ²) ]`.

vs the earlier naive `+(ρ²/2)T_s` (Hilbert): the correction is **×(−1/2)** — the magnitude halves AND the sign
flips. Injecting `+(ρ²/2)T_s` (the Gate-0 candidate) would have been ~2× too large and sign-inconsistent with
the base ρ-EOM/H — the blocker is exactly resolved.

## 4. Corrected off-round H matter moments (same λ)

`H_matter^base = λ·H_matter^std = −(ξ/2)ρ²I_r + (ξ/2)(I_θ^{e^{−s}} + N²I_s^{e^{s}}) − (κN²/2)I_4r^{e^{s}} +
(κN²/2)I_4θ/ρ²`, where the off-round moments fold `e^{±s}` INSIDE the θ-integral (`s = a2(r)P2(μ)`):
`I_θ^{e^{−s}} = ½∫sinθ f_θ² e^{−s}dθ`, `I_s^{e^{s}} = ½∫ sf² e^{s}/sinθ dθ`, `I_4r^{e^{s}} = ½∫ sf² f_r² e^{s}/
sinθ dθ`; `I_r` and `I_4θ` carry NO `e^{±s}`. Plus the shear kinetic `+(1/10)e^{−2φ}ρ²a2'²` (Gate-0.1) and the
`−2` constant. At `s=0` every `e^{±s}→1` ⇒ reduces to the base H exactly.

## 5. Exact-zero / ratio checks (CAS)

- ρ-EOM: `λ·δS_m^std/δρ / base_force = 1` at λ=−½ (⇔ raw ratio −2). ✓
- H matter: `λ·H_m^std − base_H_matter = 0` at λ=−½. ✓
- **f-PDE unchanged** (λ multiplies a homogeneous `δS_m/δf=0`; A, B, pot identical). ✓
- **φ-blindness** (no φ in `L_m`; λ scalar) preserved. ✓
- **Rigid hedgehog**: `Tshear_base(L2)|_{s=0,f=θ,f_θ=1,N=1} = 0`. ✓ (sign/λ-independent)
- Round-limit H matter → base (all `e^{±s}→1`, λ=−½ matches). ✓

## 6. Stage-2b implementation — safe to re-open?

**Conditionally YES**, once the independent blind verification (§below) confirms λ=−½ and the corrected source.
The corrected residual pieces are now fully specified: off-round f-PDE (Stage-2a, λ-free), `Tshear_base =
−(ρ²/4)T_s`, ρ-EOM matter force unchanged (already the base's), φ-correction `+(1/5Z)` (certified), Hseal with
the λ-corrected off-round matter moments + `+(1/10)e^{−2φ}ρ²a2'²` shear kinetic. **Do not implement until the
blind pass clears** (Gate-0.5 rule 9).

## 7. Independent blind verification — PASSED (2026-07-06, agent a99914ab5a36c2ba9)

An independent zero-context agent, forbidden from the Gate-0/0.5 scripts and reading ONLY the base ρ-ODE
(`cell_solver_f2d.py:245-246`) and H rows (`:305-307`), re-derived with its own sympy: **λ from ρ-EOM = −1/2;
λ from H = −1/2; they AGREE (single consistent λ, no base inconsistency); corrected source `Tshear = −(1/4)ρ²
T_s`.** IDENTICAL to §1–3. ⇒ **λ=−1/2 and `Tshear_base = −(ρ²/4)T_s` are BLIND-VERIFIED.**

**Stage-2b implementation: SAFE TO RE-OPEN** with the λ-corrected pieces (source `−(ρ²/4)T_s`; H matter `−½·std`
with `e^{±s}`; f-PDE/φ-correction/ρ-force unchanged). Charles-gated.

## Topology warning (binding)

π₂ axisymmetric S² tile only. **Cannot bank Outcome A/B for the π₃ hopfion question.** DESIGN / PROVISIONAL /
Outcome D / no A/B / no continuum lead.
