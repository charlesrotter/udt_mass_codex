# P5e Off-Round Classical Discreteness — INDEPENDENT Blind Adversarial Verifier

**Verifier:** claude-opus-4-8[1m] (INDEPENDENT, blind, DATA-BLIND; distinct from build agent).
**Date:** 2026-06-20. **Branch:** `offround-classical`. **Target:**
`offround_classical_discreteness_results.md` + `p5e_offround_qep.py`.
**Mandate:** confirm or BREAK "off-round classical channel is box-controlled (no classical
discreteness before quantization)", TOP PRIORITY on the build's own flagged residual #2
(unresolved high core modes near w~1/ell -> could there be an R-INDEPENDENT intrinsic level
even with a box continuum).

Anti-hang HELD: single sequential process per solve, Nr<=24, each call <~90 s, no
background poll left dangling (each blocked to completion). Scratch probes
(`vfy_offround_squareqep.py`, `vfy_decisive.py`, `vfy_persist.py`, `vfy_offround_fullspec.py`)
run then DELETED, not committed. All numbers below are mine.

---

## HEADLINE

### (a) THE DECISIVE CHECK — VERDICT CONFIRMED. NO R-INDEPENDENT INTRINSIC LEVEL.

The build gate (committed `qep_scan`) only reports the GLOBAL min of sigma_min(w) — it does
NOT look at higher modes, so the build's own residual #2 was genuinely open. I closed it by
computing the **FULL discrete off-round spectrum** via a SQUARE QEP (Petrov-Galerkin
left-projection by K^T -> square 72x72 (Nr=16) / 112x112 (Nr=24) pencil, companion-
linearized, all complex eigenfrequencies), exposing low AND high modes including the
w~1/ell band, then scanning cell R and testing each mode for R-independence.

**Crossing-immune test (the decisive one):** mode-index tracking is confounded by mode
crossings, so I tested box-vs-intrinsic by SPECTRUM PERSISTENCE across THREE wall
relocations (Nr=24, cells 14/20/28, 2x total). A box mode has w~1/R (w*R const, w*R does
NOT grow); a TRUE intrinsic level holds w~const across ALL THREE cells (w*R grows ~R).

**RESULT: ZERO frequencies persist (within 4%) across all three cells — anywhere in the
physical band (w up to ~9, well past 1/ell~1).** The 2-cell test (14->28) threw up 4
apparent "unscaled" near-matches (~0.575, ~0.88), but those are mode-density COINCIDENCES
(unscaled rel.err ~ boxed rel.err — a tie, not a signature); the moment a third cell (R=20)
is interposed they EVAPORATE (e.g. the ~0.58 "candidate": 14->0.585, 20->0.538 [no 0.58
mode], 28->0.575; ~0.88: 14->0.844, 20->0.929, 28->0.882 — wandering, not fixed). Look-
elsewhere across ~28 dense modes manufactures such 2-cell flukes; the 3-cell filter is the
honest discriminant and it returns nothing.

Spectrum behaviour with R (Nr=24, full square-QEP, physical band <12):
```
cell=14 (28 modes): 0.0035 0.015 0.054 0.055 0.287 0.288 0.585 0.588 0.637 0.638 0.844 ... 9.52
cell=20 (27 modes): 0.017 0.017 0.025 0.025 0.463 0.463 0.538 ... 0.929 ... 9.86
cell=28 (18 modes): 0.0006 0.0077 0.0077 0.140 0.141 0.461 0.462 0.575 0.696 0.882 ... 8.42
```
The whole spectrum RESHUFFLES and the mode COUNT in the band DROPS (28->27->18) as R grows
— modes drain out the bottom toward w->0 as the box widens. This is textbook box-control;
no level pins.

Low-end is unambiguous box: in the 14->28 (2x) overlay, the low modes match the BOXED
(w*R1/R2) spectrum spectacularly — w2=0.0077 vs boxed 0.0077 (e=0.006), w2=0.140 vs 0.144
(e=0.028), w2=0.461 vs 0.422 (e=0.085) — and the lowest mode collapses 0.0034->0.0006.

**=> The ENTIRE spectrum (low AND high, Nr=16 and Nr=24) is box-controlled. No intrinsic
core level survives. The build verdict is SOUND and COMPLETE on this point — and I closed
the gap the build itself flagged unresolved.**

### (b) LOWEST-MODE BOX-CONTROL ON A RELAXED BG — GENUINE, NOT DRIVEN BY WARP CONTAMINATION.

Reproduced the build's RELAXED basin backgrounds (genuine coupled-floored off-round solns,
walls 37-43, R0~0.1) exactly:
```
oblate   ||K||=2.100 ||M||=8.247 ratio=3.93  global-min w=0.0000  (continuum from 0)
toroidal ||K||=2.112 ||M||=7.418 ratio=3.51  global-min w=0.0000
prolate  ||K||=2.859 ||M||=8.239 ratio=2.88  global-min w=0.0000
```
All three relaxed configs: continuum starting at w=0, no gap. Bitwise-matches doc lines
96-98. **The verdict does NOT rest on the contaminated imposed-warp bg — the relaxed-bg
result stands alone.** Independently reproduced the warp-bg structural scalings on the
committed path (Nr=16, cells 10/14/18/28): ||M|| R-INDEPENDENT (16.76/16.72/16.74/16.92,
const <1%); ||K|| ~ 1/R^2 (144.5->17.9 over 10->28, ratio 8.07 vs (28/10)^2=7.84); sig(0)
~1/R^2 -> 0, global-min AT w=0 every cell (continuum from zero — if anything STRONGER box
evidence than the doc's narrower-wmax w*R~77 at Nr=12).

### (c) STRUCTURAL ARGUMENT — SOUND.

- Derrick intrinsic-size step VERIFIED (sympy): E(lam)=xi*lam+kap/lam, lam*=sqrt(kap/xi)=ell,
  d2E/dlam2 = 2*xi^(3/2)/sqrt(kap) > 0 (genuine stable minimum). Matter L2(xi)+L4(kap) with
  unique length sqrt(kap/xi); code uses xi=kap=1 => L=ell=1, consistent. So matter genuinely
  pins a core size — the loophole vs scale-free vacuum #62 was real and is now closed.
- "ell sets only HIGH core modes, lowest is the box mode" — the load-bearing claim. My full-
  spectrum + 3-cell persistence test confirms it EMPIRICALLY and goes further: not even the
  HIGH band carries an R-independent level. ||M|| R-indep (I~ell^3) and ||K||~1/R^2 (H_box)
  both reproduced. The asymptote-to-scale-free-vacuum logic (grad n->0, L4 negligible, only
  scaleless L2 survives at the wall) is consistent with the basin continuum-from-0.
- M!=0 off-round GENUINE (check 3): reproduced ||M||/||K||=0.53 (warp Nr=12 cell=14, matches
  doc) and 2.9-3.9 on basins — off-round inertia is O(0.1-4), not the round ~5e-10 floor.

---

## NET VERDICT

**"No classical off-round discreteness before quantization" is SOUND AND COMPLETE on the
fixed-background + structural pair, INCLUDING the high-mode band the build left unresolved.**

The off-round l>=2 channel carries a genuine classical oscillator (M!=0), but its spectrum
— low AND high, Nr=16 and Nr=24, square-QEP full diagonalization, 3-cell persistence test,
warp + 3 relaxed basin backgrounds, committed qep_scan + my independent square-QEP solver —
is a CELL-SET CONTINUUM (w->0 as R grows, ||M|| R-indep, ||K||~1/R^2, no persistent level).
No R-independent intrinsic core mode exists in the physical band. The intrinsic length ell
pins the static soliton's SIZE but NOT any off-round eigenfrequency for box>>core.

The build's headline residual #2 (high core modes -> possible hidden intrinsic level) is the
one place this could have broken, and it does NOT: I resolved it at Nr=24 and the high band
reshuffles/collapses with R like everything else. Two apparent intrinsic candidates from a
naive 2-cell test were look-elsewhere flukes killed by the 3-cell filter.

## RESIDUAL THAT REMAINS (NOT closed here — honest scope)

- **FIXED background, not fully coupled.** Same residual the build flagged #1 and P5d
  carried: the live amplitudes fluctuate on a FROZEN off-round bg. A fully-coupled P5e
  (off-round bg relaxes WITH the fluctuation) is the only way to make it airtight; this pass
  did not do it (out of the cheap fixed-bg budget, and not in mandate). Per MISMATCH->SOLVER
  + the box-control discipline, this is the SOLVER-completeness item the quantization step
  inherits — NOT a reason to reach for a mechanism.
- l=2 only (l>=3 untested; l(l+1) only deepens the box, so unlikely to tower — agreed).
- The square-QEP K^T projection produces a few spurious huge eigenvalues (~1e5, pinv null
  directions of Mhat); I filtered them (band <1e3) and cross-checked the physical band
  against the committed rectangular sigma_min scan — they agree, so the projection did not
  manufacture or hide a physical level.

**Discipline:** DATA-BLIND (only norms, w-scalings, dimensionless ratios — no mass/ratio
banked). OBSERVE-not-target: I hunted for an intrinsic level as hard as I could (that would
BREAK the build verdict and be the major finding) and did not find one — the absence is the
result, not a target. Box-control gate applied with negative control: candidate matches
vetted against mode-density coincidence via the 3-cell persistence filter; the two 2-cell
"candidates" were correctly rejected.
