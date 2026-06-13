# W6 — The Coupled Branch Operator & the Delta_w Flux Test: Results

Date: 2026-06-12/13. Driver: Claude. Declaration: W6 section of
w_stiffness_push_declaration.md (uncover the coupled operator, then
test bands-vs-lines). The bands-vs-lines question routed (W-ALG,
registry #30) to a single physical question about the Delta_w = 0
surface, which W6 answered by an invariant-first flux test.

## VERDICT: MIRROR FOLD, not an edge (Charles's reframe, verified)

The Delta_w / D = 0 surface (D = r^2 W - f q^2, W = (1+w)^2) — where
the q*-branch signal speeds diverge as 1/D — is NOT a curvature
singularity / edge of spacetime (the Phase-0 static-slice reading),
and NOT a benign coordinate type-change (VWALG's prior). It is a
MIRROR-FOLD CLOSURE of the finite cell: the fixed surface of the
same-minus involution (a,b) = (g_Tr, g_Ttheta) -> (-a,-b), where the
STATIC SLICE (a=b=0) degenerates but the full time-row-on geometry is
regular Lorentzian. This is CANON-consistent (C-2026-06-10-2: matter
and universe cells are finite MIRRORED domains — the fold is a mirror
crease, not a ragged edge).

Process: Phase 0 (arm, agent a43014014c558c3e5) computed the surface's
character on the STATIC class and found a curvature singularity
(invariants diverge, det g4 -> 0 linearly, signature lost at finite
proper distance) — but FLAGGED the same-minus/time-row completion as
the one unrun class-generality gap. The independent main-loop blind
verifier (agent a091cecbdfdb2c1ef, own Schwarzschild-validated
curvature engine, no shared machinery) ran exactly that gap and
OVERTURNED the interpretation. The two passes are consistent, not
contradictory: edge ON the measure-zero fixed slice, fold in the full
geometry.

## The decisive computation (Charles's same-minus fixed-surface test)

The arm computed curvature only on the a=b=0 static slice — which IS
the fixed-point set of the same-minus involution (a frame-symmetric
mirror crease, not a generic point; "no observer" in Charles's sense:
the two frames coincide there, no asymmetry to host a preferred clock).

- DETERMINANT LIFT (EXACT, class-general): with the time row on,
  det g4 = -(r sin theta)^2/[f(1+w)^2] * [ f D (1+a^2) + (b - f q a)^2 ].
  ON D=0 this = -(r sin theta)^2 (b - f q a)^2/[f(1+w)^2] — NONZERO for
  any (a,b) with b != f q a. The static degeneracy is exactly the
  a=b=0 special case. (This exact identity is the load-bearing,
  class-general result; the verifier re-derived it by independent
  cofactor expansion.)
- FIXED SET: the metric is involution-invariant iff a=b=0 — i.e. the
  arm's singular locus IS the involution fixed slice.
- CURVATURE LIFT (verifier engine, 90-110 dps; member-numerical):
  a=b=0 control K ~ D^{-4} -> 1.8e37 (diverges); every nonzero (a,b)
  tested (a-only, b-only, mixed signs) -> K finite (D^0). With a
  genuinely time-dependent member and the same-minus STATIONARY row
  (a* ~ f_T, b* = (f_theta/f_r) a*): control diverges, completion
  gives K finite. The divergence is controlled exactly by the residual
  (b - f q a)^2, which is proportional to f_T and vanishes only on the
  static f_T=0 slice.
- GEODESIC / FOLD-vs-EDGE: with the time row on, the full 4-metric
  keeps Lorentzian signature through and past D=0 (both sides);
  Christoffels finite across D=0; geodesics cross smoothly = a FOLD.
  The static slice has Gamma ~ 1/D and degenerates at finite proper
  distance = an EDGE only on the measure-zero fixed slice.
- CHART-INVARIANCE: the static-slice divergence is a real invariant
  ON THAT SLICE (cannot be charted away); but the static slice and the
  time-row-on completion are DIFFERENT 4-geometries, not different
  charts. The physical (same-minus) completion is regular.

## What the arm's algebra got right (reproduced exactly by the verifier)

det g4 = -(r sin theta)^2 D/(1+w)^2 on the static slice (linear
vanishing; signature eigenvalue -> 0); static-slice divergence
exponents q* branch K ~ D^{-3}, R ~ D^{-3/2}, generic transversal q
K ~ D^{-4}, R ~ D^{-2} (q*-vs-generic distinction real; not a
q*-elimination artifact); the float64 catastrophic-cancellation trap
near D ~ 1e-7 (mpmath clean). The arm's negative for the
INSULATING-WALL mechanism still stands (no interior flux wall
partitioning a valid region). Only its stronger "geometry genuinely
ends here / discreteness closed" reading is overturned.

## Consequence for discreteness (the route reopens, where canon said)

The "edge of spacetime => angular discreteness must live elsewhere"
conclusion does NOT survive. Cell-count discreteness REOPENS in the
quotient/mirror structure of the fold — and the lift is driven by f_T
(the time row), i.e. it lands precisely on the NONSTATIONARY
phi-angular sector that CANON C-2026-06-10-3 already redirected the
program toward, and where the same-minus theorem lives. The orchestra
(Charles's architecture: the angular sector composing on the metric)
is the live frame: the fold is a mirror crease of the finite cell, and
the angular structure that quantizes (if it does) lives in how the
cell closes on its mirror, not in a single cell's interior modes (the
retired resonator template).

## Defects in the arm record (verifier-found)

1. The Phase-0 headline overclaimed class-generality; the determinant
   identity det g4 ∝ D holds only on the diagonal-time three-field
   block; the same-minus enlargement lifts it. (The arm's own scope
   note + attack item flagged this; the targeted check refutes the
   edge reading.)
2. Vacuous asserts: phase0b check("4b", True) is hardcoded; phase0
   B1/D3 assert f/f == 1 (tautology dressed as a local-speed check —
   claim correct, test does not earn it).
3. w_alg #30's caution (q-elimination breaks at Delta_w, L_qq ~
   Delta_w^{-3}, unreduced 3-field EL finite there) was right and
   under-weighted; the generic-q control addressed the q*-artifact but
   not the time-row completion.

## Status / scope

VERDICT (fold, not edge) is CLASS-GENERAL via the exact determinant
identity. The exact finite curvature VALUES are member-numerical
(C=0 ell=2 family, q* tangential + generic transversal q, constant
and same-minus-stationary time rows) — matching the arm's own
member-specificity scope. Open for a deeper pass (queued): a
class-general curvature-finiteness statement (vs member-numerical);
the coupled operator's bands-vs-lines now re-posed in the
fold/quotient with the time row ON (not the static slice). All
kappa != 0 / time-dependent physics remains hypothesis-grade.

## Registry

#30 RE-AMENDED (see NEGATIVES_REGISTRY.md): the Delta_w = 0 surface is
a mirror-fold closure (same-minus fixed surface), not an edge; the
static-slice curvature singularity is the measure-zero crease; the
time-row completion is regular Lorentzian (det g4|_{D=0} =
-(r sin)^2 (b-fqa)^2/[f(1+w)^2], exact); cell-count discreteness
reopens in the fold/quotient on the nonstationary phi-angular sector.
