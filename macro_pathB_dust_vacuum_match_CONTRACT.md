# CONTRACT — Match dust interior to Path B vacuum exterior at turn

**Date:** 2026-07-08 · Pre-registered.  
**Go:** Charles — match at turn; re-score mass window by matchability.  
**Parents:** `macro_pathB_dust_closure_window_results.md`

## Setup

| Item | Tag |
|------|-----|
| Path B gravity | CHOSE |
| Dust interior α=0 `L_m=−ρ D²` | FREE probe |
| Vacuum exterior ρ≡0 | same Path B EL |
| Interface | at **qualifying turn** (R_exp≥3, r_turn≥2 r_c) |
| Matching | **C⁰**: continuous `(D, D', φ, φ')` — automatic by continuing IVP with ρ switched off |
| No SNe / G/P | OUT |

## Exterior health (MATCH_OK if all)

After integrating vacuum from `r_turn` to `r_ext = max(r_turn+8, 3 r_turn)` (FREE box):

1. Fields finite throughout  
2. `D > D_floor` (no collapse)  
3. `φ` finite, `φ_max_ext − φ(r_turn) < Δφ_blow` (e.g. 10) — no runaway  
4. Optional soft: `D` does not drop below `0.5 D(r_turn)` (no immediate re-collapse)

## Classes

| Class | Meaning |
|-------|---------|
| NO_TURN | never qualified CLOSE interior |
| MATCH_OK | turn + healthy vacuum exterior |
| MATCH_FAIL | turn but exterior collapses/blows |
| COLLAPSE_INT | interior dies before useful turn |

## Mass window

Report M distribution for MATCH_OK vs MATCH_FAIL vs NO_TURN.  
Primary family: gauss r_c=1, Q0=0.5; cross-check Q0=0 and r_c=2.

## Outputs

`macro_pathB_dust_vacuum_match.py` · `macro_pathB_dust_vacuum_match_results.md`
