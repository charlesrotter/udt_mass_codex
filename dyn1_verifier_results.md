# dyn1 VERIFIER — independent blind adversarial prosecution of the CONTINUUM verdict

Verifier agent: blind adversarial verifier (Opus 4.8, 1M ctx), own machinery.
Date: 2026-06-14. New file (dyn1_verify.py + this record). Log /tmp/dyn1_verify.log.
DATA-BLIND (no lepton wall numbers loaded). Independent cell integrator,
independent self-adjoint FD operator, independent SYMMETRIC generalized
eigensolve (scipy eigvalsh) — did NOT re-run the challenger's scripts.

## CHARGE

dyn1_results.md claims: the single matter cell's dynamic radial stability is a
CONTINUUM — every cavity is linearly STABLE (all omega^2>0), no discrete
spectrum. The stability test used a NEUMANN seal BC. THE KILL-SHOT: the derived
w6/wcc seal has a PARITY DICHOTOMY — sigma-EVEN (static shape) -> NEUMANN;
sigma-ODD (f_T-driven, TIME-DEPENDENT amplitude) -> DIRICHLET. A dynamic
perturbation is time-dependent => plausibly the sigma-ODD/DIRICHLET branch.
dyn1 may have imposed the WRONG parity BC. If the correct (odd/Dirichlet, or
full mirror-fold) seal destabilizes a sub-range of cavities (omega^2<0 for SOME
depths, not others), the stable set is DISCRETE => the spectrum => OVERTURNED.

## VERDICT: CONTINUUM CONFIRMED. The correct seal BC does NOT destabilize.

The Dirichlet (sigma-ODD, time-dependent) seal and the antisymmetric mirror-fold
closure both leave EVERY cavity linearly STABLE, with omega^2_min STRICTLY
POSITIVE at every depth E and in fact LARGER than under Neumann (the Dirichlet
seal STIFFENS the cell). No negative mode appears under ANY metric-derived seal
closure, at any depth. The single-cell radial discreteness route is genuinely
exhausted. The prize (a discrete stable set from the correct seal) is NOT there.

## KILL-SHOT A (decisive) — omega^2_min vs depth E under EACH seal BC

I re-derived the linearized operator independently from the canon dynamic
equation v_TT = e^{-4v}(v_mm - S(v)):  J u = omega^2 W u, J = -d^2/dm^2 +
U''(v0), W = e^{4v0}. I built J as a SYMMETRIC matrix and solved the symmetric
generalized eigenproblem (not the challenger's non-symmetric ghost-row form)
under each seal BC. Cell L(E=3)=1.67427938129 (matches banked to 1e-12).

    E       L         NN          DD          DN        ND/mirror     robin-
   1.55  1.80877    2.019763    4.934583    2.111734    4.342474    -10.748915
   1.8   1.78381    0.754775    2.431400    0.768473    2.364804     -3.552772
   2.0   1.76425    0.456510    1.596392    0.463060    1.567610     -2.022767
   2.5   1.71752    0.185682    0.713749    0.187600    0.706145     -0.714370
   3.0   1.67428    0.096530    0.386662    0.097337    0.383594     -0.325391
   4.0   1.59798    0.036876    0.153003    0.037105    0.152163     -0.098198
   6.0   1.47777    0.010179    0.043160    0.010222    0.043004     -0.018508
   9.0   1.34913    0.002909    0.012446    0.002918    0.012415     -0.003389
  15.0   1.18466    0.000613    0.002635    0.000614    0.002630     -0.000347
  30.0   0.97185    0.000075    0.000324    0.000075    0.000324     -0.000002

  NN  = Neumann-Neumann (dyn1's choice; both ends turning-point seal).
        REPRODUCES dyn1's table to all printed digits (independent code).
  DD  = Dirichlet at the seal (the sigma-ODD / TIME-DEPENDENT branch).
  DN  = Dirichlet center / Neumann seal.
  ND  = Neumann center / Dirichlet SEAL = the antisymmetric mirror-fold
        (sigma-ODD perturbation -> u=0 at the crease), the physically-correct
        time-dependent closure.
  robin- = ARTIFICIAL inward/anti-stabilizing Robin (beta=-5) at the seal — a
        PLANTED control, NOT metric-derived, included to prove the test is live.

READING: every metric-derivable seal (NN, DD, DN, ND/mirror) gives
omega^2_min > 0 at EVERY depth. The Dirichlet/odd seal and the mirror-fold seal
do not merely fail to destabilize — they raise omega^2_min above the Neumann
value (a clamped boundary is STIFFER than a free one, as expected). omega^2_min
decreases smoothly toward 0+ as E grows (the soft breathing/translational mode
of an ever-wider cell) but NEVER crosses zero under any branch. STABILITY IS A
BAND under every correct seal BC — no sub-range is destabilized, so NO discrete
stable set is carved out. The continuum holds.

Grid convergence (most adversarial deep cells, DD & ND seals):
  E=9 : DD=0.0124464, ND=0.0124151 stable across N=1201/2401/4801.
  E=30: DD=0.0003241, ND=0.0003238 stable across N=1201/2401/4801.
The convex-DD ground eigenvector at E=3 is NODELESS (sign-definite) with
omega^2=0.3867>0 — a genuine positive lowest mode, not a missed crossing.

Instability-DETECTION control (validates the test is live): concave well
(W->-W) under Neumann gives omega^2_min = -56.70 (matches dyn1's -56.78); the
planted inward-Robin seal drives omega^2 strongly NEGATIVE (-10.7 at E=1.55).
So a "POSITIVE omega^2" verdict is a real detection, not a dead scheme.

## KILL-SHOT B — the convexity inference, independently audited

"U''>0 => all omega^2>0" is AIRTIGHT under every BC with a non-negative boundary
term, and I verified it does NOT secretly depend on the Neumann choice. The
Jacobi potential U''(v)=2e^{-2v}+e^{v} has its minimum at v*=ln4/3=0.462098,
value 2.381102 > 0 — strictly convex, no concave region (independently
reproduced, exact mpmath). RAYLEIGH ARGUMENT: for J=-d^2/dm^2+W with W>=2.381,
<u|J|u> = INT(u_m^2 + W u^2) - [boundary term]. Dirichlet (u=0), Neumann
(u_m=0), and outward-stabilizing Robin all give a NON-NEGATIVE boundary term, so
<u|J|u> >= 2.381 INT(u^2) > 0 — positive-definite REGARDLESS of the weight
W=e^{4v0} (a positive weight cannot flip the sign of the Rayleigh quotient). The
ONLY way to a negative omega^2 is a NEGATIVE boundary term, i.e. an
INWARD/anti-stabilizing Robin BC — which is NOT what the mirror-fold derives
(the fold gives Dirichlet OR Neumann, both stabilizing). The numerics confirm
the analytic statement: NN, DD, DN, ND all positive; only the planted inward
Robin (not metric-derived) goes negative. NO boundary-driven instability exists
in the correctly-derived closure.

## KILL-SHOT C — the chart reduction is correct

The flow-chart reduction v_mm = S(v) = e^{-2v}-e^{v} reproduces the validated
cell: my independent mpmath half-period L(E=3)=1.67427938129 matches the banked
anchor to 1e-12. The static limit is the canon cell; the dynamic operator
e^{-4v0}(u_mm - U''(v0)u) follows from it with no discarded term that matters for
the seal operator (the seal enters only through the BC, which I varied
exhaustively). Reduction CONFIRMED.

## KILL-SHOT D — multi-bounce orbits are period repeats (no nodal catalog)

At fixed E=3, integrating n=1,2,3 full bounces gives total chart length =
n x (single-bounce length) with IDENTICAL amplitude (1.895334) and IDENTICAL
turning points (vmin=-0.81616, vmax=1.07917). A multi-bounce orbit is the SAME
one-bounce cell traversed n times — a period multiple in the single convex well,
not a distinct sealed configuration. CONFIRMED: no discrete nodal catalog.

## WHICH KILL-SHOT DECIDED IT

Kill-shot A decided it, backed by the kill-shot B analytic argument. The
challenger's choice of Neumann was NOT load-bearing: the verdict is INVARIANT
across all metric-derivable seal BCs because the underlying operator is
positive-definite (W>=2.381>0) under any stabilizing boundary term. The
sigma-ODD/Dirichlet seal — the one thing that could have flipped the verdict —
STIFFENS rather than softens. The prize is genuinely absent here.

## WHAT IT MEANS

Single-cell RADIAL discreteness via dynamic stability is truly exhausted: it does
not depend on the seal-parity caveat, the inner-product weight, the chart, or the
nodal reading. Combined with #40 (boundary cohomology rigid) and #33/#34/#39
(bulk continuum), the SINGLE-CELL routes are closed. If a particle spectrum is
native to UDT it is NOT a lone-cavity stability catalog — it must come from the
GLOBAL critical-M condition and/or multi-cell ensembles (the orchestra), or from
the topological/cohomological sector (q=1/3, N=3 area form), which this dynamic
sign-test does not touch. NOTE (discipline): omega^2 here is a STABILITY SIGN-TEST,
never a mass — the masses are cavity depths/MS content, themselves a continuum in E.

## SCOPE / HONESTY of THIS verification

- Radial sector, linear stability about the round one-bounce cell, ON
  two-exponential source, flow-chart center turning-point + parity seal closure.
- Premises inherited and not re-litigated: the ON two-exponential matter source
  (w_alg PART E) and the same-minus mirror-fold parity dichotomy (w6/wcc D3,
  itself HYPOTHESIS-GRADE per wcc sec iv). My job was: GIVEN that dichotomy, does
  the time-dependent (odd/Dirichlet) branch destabilize? It does not.
- A fully NONLINEAR / finite-amplitude (fold/transcritical) instability not
  visible as a zero LINEAR mode is not excluded by a linear sign-test — same
  scope limit dyn1 and wcc sec(v)#2 already flag. Within linear stability under
  every correct seal BC, the continuum is confirmed.
