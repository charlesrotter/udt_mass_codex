# CONTRACT — Improved closure window on Path B + dust probe

**Date:** 2026-07-08 · Pre-registered before compute.  
**Parents:** `macro_pathB_dust_WP2_results.md` · `macro_native_matter_edge_MAP.md`  
**Charles go:** improve “closes,” bracket in mass M, map narrow pass/fail band.

## Gravity / matter (unchanged tags)

| Item | Tag |
|------|-----|
| Path B: free `D_A` + EH + R1 kinetic | CHOSE |
| Dust `L_m=−ρ D_A²`, α=0 | FREE temporary probe |
| Profile gauss + top-hat cross-check | FREE shape |
| No SNe / 1101 / G/P | OUT |

## Improved “CLOSE” definition (primary)

A run is **CLOSE-candidate** only if **all** hold:

1. **Expansion first:** `D` grows: `D_max / D_0 ≥ R_exp` with `R_exp = 3` (FREE threshold).  
2. **Outer turn:** after the growth phase, `D'` crosses from `> +ε` to `≤ 0` at some `r_turn`.  
3. **Not core-stuck:** `r_turn / r_core ≥ R_sep` with `r_core = r_c` (profile scale), `R_sep = 2` (FREE).  
4. **Finite / non-collapse:** `D_min > D_floor` after turn (no crash to ε); integrate at least to `r_turn + Δ` or `r_max`.  
5. **φ not required →∞** (E-φ∞ secondary only).

**OPEN:** expands, no qualifying turn.  
**COLLAPSE:** D hits floor or S → large negative with D→0 without satisfying CLOSE.  
**CEIL:** `φ_max > 2.15` (diagnostic, not required for CLOSE).

## Mass invariant

```text
M = ∫ 4π D_A² ρ dr    (G=c=1)
```
Also report `M / r_c` (dimensionless-ish in probe units).

Primary scan variable: **target M** via ρ₀ for fixed r_c (or scan ρ₀ and bin by M).

## Pass/fail band map

For fixed profile family, plot/class vs M:

- OPEN / CLOSE-candidate / COLLAPSE  
- Width of M interval with CLOSE-candidate  
- Whether top-hat and gauss agree on M-window (overlap)

## Outputs

`macro_pathB_dust_closure_window.py` · `macro_pathB_dust_closure_window_results.md`
