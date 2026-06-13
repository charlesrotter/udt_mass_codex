# NS-SCAN BLIND ADVERSARIAL VERIFIER — Verdict

Agent: ns-verify (Opus 4.8 1M), independent hostile verifier.
Date: 2026-06-13. Default posture: REFUTED. Own machinery throughout
(own sympy reductions, own Ricci derivation, own Cauchy march, own-seed
C-3 scan). Scripts: verify_ns_sign.py, verify_ns_sign2.py,
verify_ns_legb.py, verify_ns_c3.py, verify_ns_gauge.py. Log /tmp/ns_verify.log.

## VERDICT: PARTIALLY-CONFIRMED (scope)

The challenger's TYPE claim is CONFIRMED on its own terms: the diagonal
dilation-tie nonstationary operator is HYPERBOLIC in T, and v_a3.py line 23
carries a genuine f_T^2 sign error. BUT the claim's reach is correctly
self-scoped by the challenger, and the broader banked negative #22 does
NOT fall, because its load-bearing legs (b) the fate polynomial and (the
off-diagonal Q-partition) are independent of the corrected sign.

## What I confirmed with my own machinery

1. THE SIGN (axis 1) — CONFIRMED. From the canonical dilation-tie
   4-metric (g_tt=-e^{-2phi}, g_rr=e^{2phi}, sqrt(-g)=r^2 sin th) and the
   C1 dilation action, my own EL gives principal part:
     coeff(phi_TT)   = +c r^2 e^{2phi}
     coeff(phi_rr)   = -c r^2 e^{-2phi}
     coeff(phi_thth) = -c
     cTT/cRR = -e^{4phi} < 0 EVERYWHERE  => HYPERBOLIC in T.
   Wave speeds c_r^2 = e^{-4phi}, c_th^2 = e^{-2phi}/r^2, positive for all
   phi. The two stated action forms (ns_scan e^{-2phi}-weighted, v_a1_a2
   1/f-weighted) are the SAME object (L1/L2 = -1). My independent
   reduction of v_a1_a2's OWN action gives L_red = -(c/8)r^2(f_r^2 -
   f_T^2/f^2). v_a3 line 23 wrote -(c/8)r^2(f_r^2 + f_T^2/f^2); the
   difference is EXACTLY +c r^2 f_T^2/(4 f^2) — v_a3's f_T^2 sign is
   flipped. The "elliptic/no-propagation" verdict (v_a3 C-2) is computed
   from that flipped term and is therefore wrong in the diagonal class.

2. HIGH-K / well-posedness (axis 4) — CONFIRMED, not a coarse artifact.
   Under the corrected hyperbolic sign, seeded high-k modes (k=1..50) stay
   BOUNDED (maxabs ~1). Under v_a3's elliptic sign the SAME modes blow up
   ~1e59-1e60 and growth rises with k — textbook Hadamard ill-posedness.
   The "ill-posedness" was the sign error, not the metric.

3. T-dependence is PHYSICAL (axis 3) — not gauge. The Ricci scalar of the
   time-dependent dilation-tie 4-metric carries genuine phi_TT and phi_T^2
   (weighted e^{4phi}, exactly the hyperbolic balance). The propagating
   wave is a coordinate invariant.

## The strongest points AGAINST the claim being a kill of #22

4. LEG (b) STANDS (axis 2) — the decisive limiter. My independent
   rederivation of the off-diagonal shape-stationarity gives FATE numerator
   = 2 f q v_h (f q v_r - v_h)^3, identical to the banked
   -2 f q f_theta (f q f_r - f_theta)^3 up to sign, and it is f_T-FREE.
   "Motion never sources SHAPE" is an algebraic fact about (q,w)
   stationarity, UNTOUCHED by the time-kinetic sign. So even with T
   propagating, no shaped (non-spherical) matter is sourced by motion.

5. THE C-3 OBJECT IS SEPARATE (axis 5). The 0/6800 "e_T never timelike"
   result is the OFF-DIAGONAL Class-B eliminated object L* = -R/sqrt(fD2),
   where R = fP + D2 vT^2 ALREADY carries the correct +D2 f_T^2 sign. The
   diagonal sign error (v_a3 line 23) lives ONLY in the spherical L_red
   used by C-2. My own-seed C-3 scan reproduces the Q-partition exactly
   (7997/7997). NOTE: I find the timelike direction is e_T-dominated in
   ~12.5% of Lorentzian samples (1001/7997), so the literal "0/6800 / T
   never timelike" wording is metric-definition-dependent and weaker than
   stated — but the mixed-type partition itself is robust and the sign fix
   does NOT touch it. v_a3's OWN C-3b check already FAILED in the original
   suite (45%, not >90% theta-dominated) — the "T never marches" gloss was
   shaky before this challenge.

## Surviving exact statement

The nonstationary WHOLE diagonal dilation-tie metric PROPAGATES
hyperbolically in T (well-posed Cauchy, physical curvature wave); the
banked "elliptic-in-T / Hadamard-ill-posed / no sector propagates in T /
cells do not evolve" headline is WRONG in the diagonal class and rests on
the v_a3 line-23 sign error. HOWEVER the orthogonal leg "motion never
sources SHAPE" (fate polynomial, f_T-free) STANDS, and the off-diagonal
Q-partition object is untouched. So: the metric's time sector is a genuine
wave sector, yet under C1 alone that wave still sources no shaped matter.

## CONDITIONS-CHANGED flags (for the registry, pending Charles)

- Registry #22: FLAG CONDITIONS-CHANGED on the clauses "no sector
  propagates hyperbolically in T" and "cells do not evolve / 4D
  boundary-value equilibria" (premise: diagonal reduced time kinetic =
  +f_T^2/f^2). These are REFUTED in the diagonal class. The clauses
  "the fate polynomial is f_T-free; motion never sources shape" and the
  Class-B mixed-type partition REMAIN VALID — #22 is amended, not voided.
- Registry #5 "E0>=0 => elliptic, no real modes" lineage: re-grade any
  member resting on "C1 does not propagate in T".
- solution_space_baseline.md B3 "elliptic-in-T / motion-never-evolves":
  CONDITIONS-CHANGED on the propagation clause; the shape-sourcing clause
  stands.
- The off-diagonal Class-B "e_T never timelike (0/6800)" sub-claim:
  NOT refuted here, but flagged as metric-definition-sensitive (own-seed
  reproduction gives ~12.5% e_T-dominated; v_a3's own C-3b failed) —
  recommend re-stating quantitatively before any forward use.

## Bottom line

The discreteness-reopening route (nonstationary phi-angular wave sector)
is alive — the time sector genuinely propagates. But the propagation does
NOT by itself produce shaped matter (leg b stands); the program's forced
object (native w-stiffness sector) and the "motion never sources shape"
no-go are NOT overturned. The challenger's self-scoping was honest and
accurate.
