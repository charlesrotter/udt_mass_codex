# The Dynamic-Phi / Universal-MS-Scale Synthesis

Charles's synthesis, 2026-06-14, after the bulk + boundary were closed
(#34/#39/#40) and the static isolated-cell approach was found to leave the
scale free. CANON-CANDIDATE pending his sign-off. DEEPENS the
critical-universe frame (CRITICAL_UNIVERSE_FRAME.md). Append-only.

## What this fixes (the gap the whole session circled)

Every recent solve was a SINGLE CELL IN ISOLATION — inner radius set to 1,
source Phi set to 1, no connection to anything else. So the dimensionful
scale came out FREE (#39 RELATES-not-DETERMINES), and the two halves
didn't match at the seam: the matter-cell interface asymptote r*->2.5459
vs the universe-cell r*->1.6859. That asymmetry is the TELL — the dilation
field mirrors EXACTLY (reciprocal c_eff is dead-on, neg_sweep), only the
cell RADIUS is asymmetric, and r* is exactly the isolation-dependent
quantity we should never have read the scale off of. (The p~-2.75 "stall"
was a pre-Taylor-ruling numerical artifact, not physics.) So the
SCALE-related conclusions from isolated cells are SUSPECT.

WHAT SURVIVES (scale-independent, not in question): the cohomological
charge q=1/3, N=3 (topological); the nonstationary PROPAGATION (canon
C-2026-06-13-1, phi is dynamic); "a negative-phi cavity forms and is
smooth."

## The synthesis (Charles): re-derive the legacy physics NATIVELY

The legacy (udt_canonical_geometry.md) reached real physics — cavities, an
angular spectrum, a matter scale (r_*~6.99~7, cos(pi/5)) — but via a
DIRAC IMPORT (the resonator/mass-as-eigenvalue template, banked-dead).
Re-derive the SAME physics WITHOUT that import, from three ingredients:

1. DRIVE PHI NEGATIVE -> CAVITIES. Matter cells are wells in the
   negative-phi background (f=e^{-2phi}>1). Cavities form; that part is
   real.
2. ANGULAR-SECTOR MODULATION. The q=1/3 / N=3 cohomological charge selects
   which cavities are allowed -> the discrete types (the legacy spectrum
   without the Dirac machinery).
3. THE SINGLE UNIVERSAL SCALE = the universe's total MISNER-SHARP mass M.
   This is the piece missing the WHOLE TIME. phi is the dimensionless
   DYNAMIC field (it propagates); M sets the one dimensionful scale (the
   "units") phi lives in. NOT a static background phi sits in — M sets the
   units, phi does its dynamic thing on top. M is currently an
   observational INPUT (CMB: radius R from T_CMB, M=c^2 R/2G). Whether M
   is itself self-determined ("it only closes one way", bet (a)) is the
   deeper question, deferred; first pass takes M as the single input.

## Closes the loop with #40

Registry #40 proved discreteness requires a GLOBAL condition that pins the
otherwise-CONTINUOUS scale E. The open "what global condition?" is answered
here: the global condition is THE UNIVERSE HOLDING EXACTLY THE CRITICAL
MISNER-SHARP MASS. The thing #40 said we needed is the thing the frame has
pointed at all along. Pieces line up: dynamic phi (alive) + universal
MS-mass ruler (sets scale) + angular charge q=1/3 (selects cavities) ->
absolute, discrete particle masses.

## The critical window (two-sided critical point, made concrete)

Matter exists only at the CRITICAL M (two-sided, not a one-sided
threshold). The stable-matter window in M may be NARROW. If narrow (and
the observational M estimate slightly off), BRACKET M in sub-percent
increments to find the stabilization window; if the window is WIDE,
bracketing is unnecessary. The M-scan DOUBLES AS A TEST: a tight window
CONFIRMS the critical picture (and would EXPLAIN the observed near-critical
/ flat universe — matter being here requires criticality); a wide "mush"
CHALLENGES it. Either outcome is a real result. CAVEAT: sub-percent M
scanning is only meaningful if the machinery is accurate to better than the
window AND the physics genuinely carries that sensitivity.

## The bridge crux (still open, the real unknown)

HOW does the cosmic M set the PARTICLE scale? c, G, M alone hand back the
COSMIC size — so the bridge from universe-M to particle-scale cannot be a
plain dimensional formula; it must run THROUGH the cavity + angular
structure (ingredients 1+2). This is where the legacy's ~7 / cos(pi/5)
might genuinely RE-EMERGE — as the OUTPUT of that bridge, DERIVED natively,
never imported. Re-derive; if it comes back without the Dirac template it
is real and resurrected; if it cannot, it was numerology and stays buried.

## Discipline

NO Dirac import. The resonator/mass-as-eigenvalue template stays
BANKED-DEAD (discreteness = the critical-M global condition + the
cohomological charge, NOT a vibration spectrum). Metric-led; data-blind vs
the wall numbers; verifier-before-record; nothing canonical without
Charles. SOLVE THE WHOLE (dynamic, coupled, M-anchored), do not isolate
lone cells.

## The build (phased; see HANDOFF queue)

Drop static isolated cells. Build the DYNAMIC phi field with M wired in as
its single dimensionful scale, cavities + angular charge living in it, and
a real test of whether a cavity HOLDS TOGETHER (persists/recycles, doesn't
disperse — "stabilize" is a dynamic question, phi alive). Then scan M for
the stable-matter window.
- Phase 1: the dynamic phi evolver (the canonized propagating field, both
  sectors, the ON source), carrying a negative-phi cavity; Taylor/mpmath
  for deep phi; verify well-posed stable evolution.
- Phase 2: wire M in — total Misner-Sharp mass of the field; set the
  global dimensionful scale by the constraint total-MS = M (Phi becomes
  DERIVED from M, not free).
- Phase 3: cavity-stability test — initialize a negative-phi cavity,
  evolve, measure persistence vs M; bring in the angular charge as the
  discrete selector.
- Phase 4: the M-scan — the stable-matter window in M (bracket sub-percent
  if narrow); the test of the critical picture; watch for the native
  re-emergence of a matter scale (the legacy ~7 / cos(pi/5)).
