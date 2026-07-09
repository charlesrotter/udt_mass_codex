# CONTRACT — Dilated dust interior → Path B vacuum S2 soft-close

**Date:** 2026-07-08 · Pre-registered.  
**Go:** dilated BVP soft-close; bracket M.  
**Frame:** `macro_matter_dilation_edge_FRAME.md`  
**Parents:** `macro_pathB_dilated_dust_results.md`

## System

| Item | Tag |
|------|-----|
| Path B gravity | CHOSE |
| Dilated dust `L_m = −ρ₀ f(r) D_A² e^{−2φ}` | FREE probe; weight THEORY-motivated |
| f = gauss | FREE |
| Exterior ρ=0 Path B vacuum | CHOSE handoff |
| α free grid | OUT |
| SNe / G/P | OUT |

## Interface

`r_int = κ r_c` with κ∈{2.5, 3, 4} (FREE).  
C⁰ continuous `(D, D', φ, φ')`; ρ switched off for r>r_int.

## Soft-close success (MATCH_S2)

After vacuum exterior to `r_ext = r_int + L` (L=8 FREE):

1. Finite, no D-floor crash  
2. **S2-like:** mean`|φ'|` on outer third `< ε_Q` (e.g. 0.05)  
3. **S2-like:** mean`|D''|` proxy `|ΔS/Δr|` on outer third `< ε_S` (e.g. 0.15)  
4. Optional: `|φ(r_ext)−φ(r_int)| < Δφ_max` (e.g. 0.5)

## Classes

NO_INT (interior dies) · EXT_FAIL · MATCH_S2 · EXT_OPEN (healthy but not S2)

## Scan

ρ₀ log grid → M; primary r_c=1 Q₀∈{0,0.5}; cross r_c=2.

## Outputs

`macro_pathB_dilated_softclose.py` · `macro_pathB_dilated_softclose_results.md`
