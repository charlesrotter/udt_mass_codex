# SOLVER BUILD — MAP (constrained-two-player; return-to-solver phase, 2026-07-01)

MAP only (no build yet — for Charles's review). Goal + acceptance are FROZEN in
`discreteness_preregistration.md`. Binding rule: **solve the solution space, not "the electron."**
Modest FIRST goal: does the derived system have ANY stable isolated finite-cell solutions at all?

## What we solve (the DERIVED frame — not the old φ-outside-g solver)
Metric `ds² = -e^{-2φ}c²dt² + e^{2φ}dr² + h_AB dx^A dx^B` (two players: φ = longitudinal dilation, h_AB =
transverse 2-geometry), static. Action `∫c√h[(Z_φ/2)φ'² + R^{(2)}[h] + W_χ𝒦]`, `W_χ=1` interior P / `e^{2φ}`
exterior G, `Z_φ` held FIXED. Bulk EL + seal junctions JC1/JC2 (all derived + blind-verified this session).

## THE BIG SIMPLIFICATION — Stage 0/1 is a 1-D nonlinear BVP (not the 3-D monster)
Take the ROUND cell first (`h=r²Ω`; the only dynamical field is then φ):
- **Interior P**, `r∈[r_c,r_s]`:  `Z_φ (r²φ')' = 4e^{-2φ}`   (derived Branch-P round eq; nonlinear, Lane-Emden-like)
- **Exterior G**, `r∈[r_s,∞)`:  `(r²φ')'=0 → φ = φ_∞ − q/r`   (derived Branch-G; ANALYTIC — no numerics needed)
- **Seal `r_s` (JC1):** φ and `r²φ'` continuous → `q = (r²φ')|_{r_s}` (the flux = the public charge).
- **Seal `r_s` (JC2), round + source-free:** MAP OBSERVATION (to CAS-confirm in the build): with `h` round and
  continuous both sides, `(K^{AB}−Kh^{AB})_P = e^{2φ_s}(K^{AB}−Kh^{AB})_G` reduces to `1 = e^{2φ_s}` → **`φ(r_s)=0`**
  (a DERIVED Dirichlet seal BC — the Class-B charged seal), UNLESS a seal surface stress absorbs the mismatch.
- **Core `r_c`:** regularity BC (finite-core model — CHOSE, canon intrinsically-singular core).

⇒ a well-posed **nonlinear 2-point BVP** for φ on `[r_c,r_s]` (core-regular + `φ(r_s)=0`), each `r_s` giving a flux
`q`. **The discreteness question becomes a NONLINEAR-EIGENVALUE question:** does a stable solution exist for ALL
`r_s` (a continuum of cells) or only ISOLATED `r_s` (a discrete family)? Cheap, fast, CPU-fine — the derived frame
turned the 3-D basin-flooring monster into a 1-D BVP.

## Instrumenting the 9 pre-reg criteria
1. **isolated/gapped:** scan `r_s` (and core data); map where stable solutions exist → points/bands vs continuum.
2. **seed-independent:** solve by BOTH shooting and relaxation, many initial guesses → same families.
3. **stability w/o targets:** 2nd-variation / small-perturbation test of each solution; nothing imposed.
4. **grid/method independent:** vary N, basis (Chebyshev vs finite-diff), shooting vs relaxation, tol → families survive.
5. **Z_φ fixed:** one global `Z_φ` across the whole scan (report the value; it's the one open constant).
6. **quantized q:** the allowed seal-flux `q` values — isolated?
7. **branch-consistent:** P + G + JC1 (+JC2 seal BC) satisfied together (built into the BVP).
8. **perturbation survival:** kick a solution → returns to same cell or jumps to another allowed one (not a drift).
9. **blind classification:** output UNLABELED `(r_s, q, ratios)` families; compare to particles only AFTER.

## Staged plan
- **Stage 0 (build):** the 1-D round BVP solver (interior P numeric + exterior G analytic + JC1 + the JC2 `φ(r_s)=0`
  seal BC — CAS-confirm that BC first). Bounded, single process (1-D is cheap).
- **Stage 1 (FIRST goal):** does ANY stable round cell exist? Scan `r_s` → isolated or continuum? (criteria 1–5,7).
- **Stage 2:** robustness (seeds/grid/method) + perturbation + quantized-q (criteria 2,4,6,8).
- **Stage 3 (later, likely where discreteness lives):** OFF-ROUND — `h_AB` dynamical, full JC2, the φ-angular
  coupling LIVE. Round is highly symmetric; if it gives only a continuum, that itself points to discreteness needing
  the angular sector (consistent with the φ-angular hunch). Heavier (2-D+), anti-hang discipline returns.
- **Stage 4 (blind, after):** compare families' ratios to known particles.

## Premise ledger (chose/derived)
| choice | status |
|---|---|
| round-first (`h=r²Ω`) | SLICE — labeled; the WHOLE is off-round (Stage 3). Simplest first test, not a verdict. |
| interior-P / exterior-G / JC1 / JC2 equations | DERIVED (this session, blind-verified) |
| seal BC `φ(r_s)=0` (round source-free) | DERIVED-candidate (CAS-confirm in build); alt = seal surface stress |
| `Z_φ` value | FREE, held FIXED (one global choice; consilience later) — NOT a per-solution knob |
| finite-core model at `r_c` | CHOSE (canon core) |

## Anti-hang / op
Stage 0/1/2 are 1-D BVPs — fast, CPU-fine, low hang risk; still: bounded, single process, unbuffered, no nohup.
Stage 3 (off-round) reintroduces 2-D cost — apply the full anti-hang discipline there.

## First build increment (on Charles's go)
(0a) CAS-confirm the round JC2 → `φ(r_s)=0` seal BC. (0b) code the 1-D round BVP solver (P-interior shooting +
relaxation, analytic G-exterior, JC1 flux, core-regular BC). (1) scan `r_s`, report: do stable cells exist, and are
they isolated? Blind/unlabeled output. THEN ponder with Charles.
