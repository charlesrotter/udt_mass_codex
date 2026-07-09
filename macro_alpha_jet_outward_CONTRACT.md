# CONTRACT — outward integrate from α&lt;0 regular center jet

**Date:** 2026-07-08 · **Pre-registered before compute.**  
**Framing:** `macro_no_GP_framing.md` (no Branch G/P labels).  
**Parents:** `macro_phi_blindness_reaudit.md` · `macro_clean_core_first_observe_results.md` · `macro_Q1_source_posture.md`.

## Goal (OBSERVE)

From a **regular geometric center** with free `D_A` and a **direct** matter–φ weight α≠0, integrate **outward** and report what structure appears.

Not: SNe fit, cosine targeting, 1101, critical matter for Pantheon, G/P choice.

## Equations (this probe — all tags visible)

Round free `D_A`, uncompensated `𝒦` in the reduced radial action (same CAS family as first observe), plus Thread-B-style direct weight:

```
π := Z D_A² φ'
π' = 4 e^{−2φ} (D_A')² + α e^{αφ} σ(r)
φ' = π / (Z D_A²)

D_A'' from EL_D_A of
  L = (Z/2) D_A² φ'² − 2 e^{−2φ} (D_A')² − D_A² ρ_eff
```

Stand-ins (FREE temporary):

| Symbol | Choice | Tag |
|--------|--------|-----|
| `Z` | 1 | FREE convention |
| `α` | scan {−2, −1, −0.5} | FREE (not derived) |
| `σ(r)` | `σ0 exp(−(r/r_c)²)` with `σ0 = −4/α` (leading center cancel) | FREE stand-in; pin only for jet |
| `ρ_eff` | 0 for primary scan; optional = `σ` cross-check | FREE |
| Center | `D_A(0)=0` series: `D_A=r+c_3 r^3`, `φ=p_2 r^2`, `φ'(0)=0` | THEORY-motivated regularity |
| `c_3` | scan small set incl. 0 | FREE |
| `r_c` | scan {0.5, 1, 2} | FREE |
| Box | `r ∈ [ε, r_max]`, `r_max ≤ 8`, anti-hang | FREE box |
| Optics / SNe / 1101 / cosine target | OUT | — |

**𝒦 treatment:** uncompensated in this probe (CHOSE for geometry-coupled φ); not a “branch.”  
**Compensated vacuum** only if needed as separate reference — not mixed in.

## Start from series (not singular seed)

At `r=ε≪1`:

- `σ0 = −4/α`
- `p_2 = 2(6 c_3 r_c² + 1) / [r_c² (3Z + 2α + 4)]`  (from re-audit; skip if denom≈0)
- `D_A(ε) = ε + c_3 ε³`
- `D_A'(ε) = 1 + 3 c_3 ε²`
- `φ(ε) = p_2 ε²`
- `π(ε) = Z D_A(ε)² φ'(ε)` with `φ' ≈ 2 p_2 ε`

## Pre-named outcomes (characterize, do not filter)

| ID | Meaning |
|----|---------|
| J0 | α=0 control still singular / fails regular start |
| J1 | α&lt;0 regular start succeeds (finite φ', finite fields at ε) |
| J2 | Integration reaches `r_max` with finite fields |
| J3 | `D_A` monotone / turnover / collapse |
| J4 | `φ` growth: Δφ, sign, any plateau |
| J5 | Any natural edge signal in-box (blowup, `D_A'→0`, …) — report only if seen |
| J6 | Empty: no global extension in box (stiff fail) |

No merit gate on “looks like cosmology.”

## Outputs

- `macro_alpha_jet_outward.py`
- `macro_alpha_jet_outward_results.md`
