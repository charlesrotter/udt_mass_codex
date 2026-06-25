# BLIND VERIFIER — the Boundary-Cohomology Type Question (RIGID)

Independent hostile blind verifier of `h1_types_results.md` +
`h1_types_derive.py` + `h1_types_adversary.py`.
Verifier agent id: **h1v-2026-06-14-opus48** · Date: 2026-06-14.
Own machinery (own sympy 1.13.1 / mpmath 1.3.0; own cohomology bookkeeping;
own SO(3) character integrals + algebraic CG identity; own quantization
attacks). The challenger's scripts were READ for the claim, NOT re-run.
Scripts: `/tmp/h1_verify.py` (16/16), `/tmp/h1_so3.py`, `/tmp/h1_torsion.py`.
Log: `/tmp/h1_verify.log`. New file, append-never-edit.

Data-blind: NO lepton wall numbers loaded, matched, or consulted.

## VERDICT: RIGID is CONFIRMED — correctly SCOPED. No discrete family exists now.

The boundary-cohomology area-form object gives ONE topological type
(deg-1 H^2(S²,Z) generator; N=3, q=1/3) × a CONTINUOUS depth/mass. Under
EVERY currently-derived condition the seal-depth `(ln f)_seal` is a free
continuum; NO derived condition discretizes it. None of the five kill-shots
(A–E) landed a quantum. The E-quantization-by-global-critical-condition is a
**GENUINE OPEN ROUTE** (the real next question), NOT a hole that already
flips the verdict.

## Independently reproduced (kill-shots B, C, E)

All re-derived from scratch with independent constructions (16/16 PASS):

- **B (cohomology facts).** Own build of `omega_H1 = n·(∂_θn × ∂_φn) =
  sin θ` from the ℓ=1 carrier; ∫ = 4π. `Θ = (ln f)·sin θ dθ∧dφ`;
  `Ξ = dΘ` has only the `(ln f)' sin θ dr∧dθ∧dφ` component — the dθ/dφ
  derivative terms self-annihilate under the wedge, so **Ξ is EXACT** with
  global primitive Θ. Stokes reduction gives `D = 4π(ln f)_seal` both
  symbolically and via a concrete collar integral with the actual law
  `ln f = -q ln(r/r₀)` (got `4π·(-⅓ ln(r_s/r₀))`, exact match). Betti by my
  own Künneth: absolute `b0=1, b1=0, b2=1`; relative `(I×S², ∂I×S²)`:
  `H¹=R, H²=0, H³=R` — all R-valued. The relative-H³ period is a real
  pairing, NOT a lattice value. **"Exact ⇒ zero periods ⇒ no quantization"
  is airtight.**
- **B-extra (TORSION / equivariant — the challenger did NOT run this).**
  Integral UCT: all `H_*` free ⇒ `H^*` torsion-free; relative pair free by
  Künneth ⇒ **no Z/k discrete class** hides under the de Rham (R) reading.
  The Z/2 fold involution's equivariant cohomology DOES carry a Z/2 torsion
  class `u` (`H*(BZ/2;Z)=Z[u]/2u`) — but σ acts trivially on the spatial
  collar and the depth is σ-EVEN, so the depth sits in the `u⁰` summand;
  the Z/2 class measures the time-row action, orthogonal to the mass. No
  equivariant quantum of the depth. (New seam checked, closed.)
- **C (the 4 quantization attacks), all reproduced independently:**
  Dirac/flux — `(1/4π)∫_{S²} ω = 1` is the only flux quantum; the exact
  3-form Ξ has no 2-cycle period; depth multiplies as a scalar VALUE.
  Holonomy — σ-even ⇒ `ln f` single-valued across the fold ⇒ loop period 0.
  Regularity — even-in-ρ field has automatic Neumann (slope 0) for ANY
  value a₀ ⇒ fixes slope, leaves VALUE free (continuum); regular Lorentzian
  fold, not a cone. q=⅓+4π — `(ln f)_seal = -⅓ ln x`, `d/dx = -1/(3x) ≠ 0`,
  continuous; charge ⊥ mass. **No attack yields a quantum.**
- **E (no dim-7 / 1+3+5 exhaustive — the anti-numerology anchor).** Two
  independent methods: (i) algebraic CG identity `χ₁² - (χ₀+χ₁+χ₂) = 0`
  EXACTLY; (ii) numeric SO(3) character-orthogonality multiplicities
  `m₀=m₁=m₂=1`, `m₃ ≈ 7.4e-20`, `m₄ ≈ -7.4e-20`. So `3⊗3 = 1+3+5` with
  spin-3/**dim-7 absent**. The `{3,5,7}` numerology (registry #35) stays
  dead, re-confirmed by my own quadrature.

## Kill-shot A (the decisive one): E-quantization — OPEN, correctly scoped

I prosecuted this precisely and refused to inflate it either way. Two facts:
- **Single-cell closure ⇒ E free continuum** (registry #33/#34/#39, blind-
  verified): the whole-profile closure is over-determined by +1 over a
  system WITH a conserved first integral ⇒ a 1-parameter CURVE, not a
  discrete set. #39 states this explicitly: the single-cell solve RELATES
  r* to (p,Φ) and DETERMINES nothing; the one-universe-vs-family thread is
  UNADVANCED. So RIGID's "E free" is correctly scoped to currently-derived
  closures.
- **The global-critical condition is NOT yet a derived closure.** The
  frame's "matter at ONE critical amount" (c²=2GM/r*, the finite-cell
  mirror, the whole-universe tiling of #33's note (i)) is a GLOBAL
  condition that has never been written down as a closure that acts on E.
  c²=2GM/r* RELATES M and r* and fixes neither (#32, theorem-grade).

Therefore: **no currently-derived condition selects discrete E**, so RIGID
is not flipped now; AND the global-critical / cell-tiling closure is a
**genuine open route** to a discrete catalog — exactly the program's real
next question. The challenger's scoping is honest. I explicitly reject the
inflation "the single-cell closure doesn't pin E ⇒ no closure could": the
tiling/global axis is live (registry #33 CONDITIONS-CHANGED trigger).

## Kill-shot D (nonlinear breather): does not refute RIGID-cohomology

wcc PART B gives a STRICT positive damping gap on every θ-varying mode ⇒
no marginal/zero linear mode to seed a stationary breather; and a breather
would be a DYNAMICAL object, outside the cohomological claim's scope. It
does not overturn RIGID-as-cohomology. It is correctly the only dynamical
residue, and remains hypothesis-grade / open as a dynamical question (not a
cohomological family). Honestly flagged, not load-bearing for RIGID.

## SCOPE & where the types can still live

RIGID is SOLID as scoped: the boundary-cohomology area form carries charge
(4π, N=3, q=1/3) + a continuous mass, ONE rigid type, under all currently-
derived conditions. A discrete TYPE family can therefore only come from:
(i) the **global-critical / cell-tiling closure** selecting discrete E
(kill-shot A — OPEN, the sharp next object); (ii) the **#37 core-closure
3-manifold** winding class (S³/S²×S¹/L(p,q) — bundle c1, a SEPARATE
integer, never the scalar depth; my probe (3) confirms the area form's own
leaf class stays deg-1 rigid in every branch); or (iii) a nonlinear
breather (dynamical, gap-obstructed at linear order). The types are NOT in
the boundary cohomology. This NEGATIVE confirms the running picture and is
correctly recorded.

## Verifier checklist (16/16 PASS, `/tmp/h1_verify.log`)
B1-areaform, B1-int4pi, B2-exact, B2-slope, B3-stokes, B3-concrete, B4-abs,
B4-rel, C-dirac, C-holonomy, C-regularity, C-qseam, E-decomp, E-dim,
A-scope, D-breather — plus torsion/equivariant + #37-leaf extra probes.
