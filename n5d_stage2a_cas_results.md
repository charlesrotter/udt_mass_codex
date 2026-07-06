# N5d Stage-2a CAS Derivation — Results (π₂ axisymmetric tile; DESIGN / PROVISIONAL)

**Date:** 2026-07-06 · CAS = sympy · script `h4_scripts/n5d_stage2a_cas.py` · **π₂ AXISYMMETRIC S² tile ONLY —
NOT the π₃ hopfion sector.** No implementation, no pilot, no physics verdict, no Outcome A/B, no continuum lead.
Derives the off-round co-relaxed matter equations from one native φ-blind, h_AB-side action for the live
`φ(r), ρ(r), f(r,θ)=θ+u, s=a2(r)P2, L`.

**Metric (pinned by matching the base `cell_solver_f2d` f-PDE coefficients):** `g_rr = 1`, `√g = ρ²sinθ`
(s-independent), `h_θθ = ρ²e^{s}`, `h_ψψ = ρ²e^{−s}sin²θ`. Map `n=(sin f cos Nψ, sin f sin Nψ, cos f)`,
axisymmetric (∂_ψf=0). `L2 = (ξ/2)[f_r² + f_θ²/h_θθ + N²sin²f/h_ψψ]`,
`L4 = (κ/2)[F_rψ²/h_ψψ + F_θψ²/(h_θθ h_ψψ)]`, `F_rψ=N sin f f_r`, `F_θψ=N sin f f_θ`.

## 1. Equations derived (all reduce to the base at s=0)

- **Off-round f-PDE** `∂_r(A f_r) + ∂_θ(B f_θ) − pot = 0`:
  - `A/f_r = ξρ²sinθ + κN²sin²f·e^{s}/sinθ`  (ξ-kinetic s-free; κ term gains **e^{s}**)
  - `B/f_θ = ξ·e^{−s}·sinθ + κN²sin²f/(ρ²sinθ)`  (ξ term gains **e^{−s}**; κ term s-free)
  - `pot = (N²sin f cos f/sinθ)·[e^{s}(ξ + κf_r²) + κf_θ²/ρ²]`
- **Live shear source** (the residual addend beside `E_s_geom`), `T_s = T^θ_θ − T^ψ_ψ` (Hilbert
  `T^{AB}=(2/√h)δS_m/δh_AB`, repo convention):
  `T_s = (ξ/ρ²)[N²e^{s}sin²f/sin²θ − f_θ²e^{−s}] + (κN²/ρ²) f_r² e^{s} sin²f/sin²θ`,
  `Tshear_live = δS_m/δs / sinθ = (ρ²/2)·T_s
   = (1/(2sin²θ)) e^{−s}[ κN²e^{2s}sin²f f_r² + ξ(N²e^{2s}sin²f − f_θ²sin²θ) ]`.
- **ρ-EOM matter force** (pointwise): `δS_m/δρ = ξρ f_r² sinθ − κN²sin²f f_θ²/(ρ³sinθ)` — **s-independent**
  (the e^{±s} cancel in ∂/∂ρ); its θ-integral is exactly the base moment combination `ξρI_r − κN²I_4θ/ρ³`.
  (The base ρ-EOM's `e^{2φ}/4` prefactor is the GEOMETRIC normalization, not a matter φ-coupling — carries over.)
- **φ-EOM:** `δS_m/δφ ≡ 0` — matter is directly φ-blind (no φ in L_m); the off-round φ-ODE is the base φ-ODE
  **+** the already-derived off-round correction `+(1/5Z)e^{−2φ}a2'²` (`n5d_shear.phi_source_offround_correction`).

## 2. CAS exact-zero checks (all = 0 symbolically)

| check | result |
|---|---|
| (9) round-limit `A/f_r − A0` (s=0) | **0** |
| (9) round-limit `B/f_θ − B0` (s=0) | **0** |
| (9) round-limit `pot − pot0` (s=0) | **0** |
| (5) ρ²/2 emergence `δS_m/δs − (ρ²sinθ/2)T_s` | **0** (ρ²/2 is automatic — matches the blind-verified §4f factor) |
| (6) `δS_m/δρ(s=0) − [ξρ f_r²sinθ − κN²sin²f f_θ²/(ρ³sinθ)]` | **0** |
| (10) rigid hedgehog `T_s(L2)\|_{s=0,f=θ,N=1}` (f_θ=1) | `ξ(1−f_θ²)/ρ² = 0` |
| (7) `δS_m/δφ` | **0** (directly φ-blind) |

## 3. Unresolved / not-yet-closed

- **(8) Off-round H(r) / dH/dr = 0 on-shell:** NOT CAS-closed here. Needs the full geometric variation +
  the θ-integrated moments + all EOMs on-shell (the off-round H gains the shear kinetic term and the off-round
  matter moments). The base H is conserved (V4/V5); the off-round closure check is **owed before implementation**.
- The **full geometric** off-round ρ-EOM/φ-EOM forms use the already-derived shear pieces (the a2'² φ-correction
  and `E_s_geom`) — audited/relied-upon here, not re-derived from scratch in this pass.

## 4. Were the design-doc candidate formulas correct?

- **f-PDE structure: CORRECT** (the e^{±s} placement matches: e^{s} on the κ-A term and the pot ξ/κf_r² terms,
  e^{−s} on the ξ-B term).
- **T_s formulas: SIGN-FLIPPED.** CAS: `cand_T_s(L2) + derived_T_s(L2) = 0` ⇒ the design candidates were the
  NEGATIVE of the correct T_s under the repo's Hilbert `T^{AB}=(2/√h)δS_m/δh_AB` convention. **The correct
  residual addend is `+(ρ²/2)T_s` with T_s as in §1 (= `Tshear_live`).** The magnitude/ρ²-power were right; the
  overall sign was wrong. (This is exactly the kind of error the CAS gate exists to catch.)

## 5. Safe to gate implementation next?

**The MATTER SECTOR is CAS-clean** (f-PDE, T_s with correct sign, ρ-force, φ-blindness, round-limit, rigid
hedgehog — all exact). **Before Stage-2b implementation, still OWED:** (i) an **independent blind re-derivation
of T_s** (the sign is load-bearing — same discipline as the ρ²/2 blind pass); (ii) the **off-round H / dH/dr=0**
closure (§3); (iii) confirmation of the full geometric off-round ρ/φ forms. Recommendation: proceed to the blind
T_s re-derivation + the H check; **do not implement until (i)–(iii) clear.**

## 6. Topology warning (binding)

This is the **π₂ axisymmetric S² winding tile.** It **cannot bank Outcome A/B for the π₃ hopfion question** —
the axisymmetric (r,θ) map carries π₂ winding, not the 3D Hopf linking (π₃). Whether the pin/continuum question
requires the full π₃ hopfion (⇒ a 3D co-relaxed matter) is an OPEN premise for Charles. Status: DESIGN /
PROVISIONAL / Outcome D / no A/B / no continuum lead.
