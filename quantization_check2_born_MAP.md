# Check 2 (pilot-wave): Does finite-cell TYPICALITY give the Born rule |psi|^2? — MAP

STATUS: conjecture-grade MAP (no-compute frame). Derivation track, LOCAL branch
session-2026-06-17 ONLY. NOT canon, NOT verified. Follows quantization_check1_guiding_MAP.md
and its Wall-1 result. Goal-correct: emergent quantization (the WHOLE quantum face).

## THE FRAME, WHOLE

CLAIM under test: in a pilot-wave ontology, the Born rule |psi|^2 is NOT a postulate. It is
the EQUILIBRIUM / TYPICAL distribution of the real particle's (the winding's) position. Two
ingredients (Durr-Goldstein-Zanghi "quantum equilibrium"):
- EQUIVARIANCE: the density rho=|psi|^2 is PRESERVED by the guidance flow (continuity:
  d_t|psi|^2 + div(|psi|^2 v) = 0). A property of the dynamics.
- TYPICALITY: among all initial configurations of the closed universe, the |psi|^2-typical
  ones OVERWHELMINGLY dominate (the |psi|^2-measure of the configs giving non-Born statistics
  is vanishingly small). A property of the MEASURE on configuration space.
UDT HOOK (the pilot-wave ponder's point): UDT's FINITE CLOSED universe-cell (no spatial
infinity; finite mirrored domains -- the finite-cell canon) is the cleanest possible setting
for a typicality argument -- a definite configuration space with a definite measure, where the
"typical" notion is rigorous, not hand-waved over an infinite universe.

## WHERE THE "SQUARE" COMES FROM (and what it inherits)

The square in |psi|^2 traces to the BILINEAR probability current j = Im(psi* grad psi) of a
COMPLEX wave: equivariance forces rho=|psi|^2 because j=|psi|^2 v. So the SQUARE is downstream
of (a) a complex/flowing wave and (b) the guidance current. Both are exactly Check 1's
conditional structure:
- complex flowing wave = the parked hbar/rest-clock (Check-1 Wall 1 result);
- guidance velocity v = Check 1's Wall 3 (UNBUILT).
=> Check 2 is CONDITIONAL ON Check 1. We can MAP it now; an OBSERVE of the equivariance half
must either assume the conditional complex-wave+guidance structure, or target the one piece
that is dependency-FREE (below).

## THE TWO GENUINELY-UDT QUESTIONS (what is native here, beyond inherited QM)

Q-MEASURE (dependency-free, answerable NOW, metric-led): what is UDT's NATURAL configuration
measure on the finite closed cell? Standard DGZ uses FLAT Lebesgue d^3x. UDT is curved/dilated
-- its natural measure is plausibly the PROPER-VOLUME sqrt(g) d^3x (dilation-weighted). THE
CRUX: against which measure is the equilibrium the square?
  - if the native measure is FLAT -> Born |psi|^2 survives unmodified;
  - if it is DILATION-WEIGHTED -> the equilibrium is |psi|^2 weighted by the metric factor,
    i.e. a NATIVE CORRECTION to Born deep in the dilation well (FALSIFIABLE), unless the
    weight is exactly absorbed by how a position "measurement" samples volume.
This is the sharpest, cleanest, dependency-free Check-2 probe: derive the native
configuration-space measure and see whether the square is flat-Born or metric-corrected.

Q-TYPICALITY (the deep half): does UDT's FINITE CLOSED cell make the typicality argument
actually GO THROUGH (the claimed advantage over infinite-universe DGZ), or is there a native
obstruction? Sub-questions: is there a unique natural measure (vs a family)? does the closed-
cell boundary/seal impose a condition that selects or spoils equivariance? is there a
relaxation-to-equilibrium dynamics (Valentini-style), or is the cell BORN at equilibrium?

## PREMISE LEDGER (chose-or-derived)

1. Born = equivariance + typicality (DGZ framework) -- CHOSEN framework (the pilot-wave
   reading). It is the established no-postulate route to |psi|^2; importing it is template-led,
   so the OBSERVE must ask what UDT NATIVELY does, not assume DGZ holds.
2. The complex/flowing wave exists -- INHERITED CONDITIONAL from Check 1 (= parked hbar).
3. The guidance velocity v -- INHERITED UNBUILT from Check 1 Wall 3.
4. Natural configuration measure = proper-volume sqrt(g) d^3x -- this is the OBSERVE TARGET,
   currently a HYPOTHESIS (flat vs weighted is exactly what to derive). Tag: to-be-derived.
5. Finite closed cell with a definite measure -- DERIVED (finite-cell canon); the asset that
   makes typicality potentially rigorous.

## WHERE IT BREAKS

- BREAK A (measure): if the native measure is dilation-weighted and the weight is NOT absorbed
  by measurement-sampling, UDT predicts a Born DEVIATION in deep wells -- either a falsifiable
  signature (interesting!) or a failure to match observed Born (a problem). Must be derived,
  not assumed away.
- BREAK B (dependency): the equivariance half cannot be cleanly OBSERVED until Check 1's
  guidance law (Wall 3) exists. Check 2's equivariance is conditional; only Q-MEASURE is
  dependency-free now.
- BREAK C (typicality): "finite cell makes typicality rigorous" is a HOPE; if the natural
  measure is non-unique or the seal spoils equivariance, the advantage evaporates.

## WHAT EXPLORING ALL OF CHECK 2 TAKES (gated, full apparatus)

(i) Q-MEASURE: derive UDT's native configuration-space measure on the finite cell; is the
equilibrium square flat-Born or metric-corrected? -- DEPENDENCY-FREE, metric-led OBSERVE,
FIRST. (ii) equivariance of |psi|^2 under the (conditional) guidance flow in the UDT metric
(curved continuity d_t(sqrt(g)rho)+div(sqrt(g)rho v)=0). (iii) the typicality argument on the
finite closed cell -- does it go through, uniquely? Each gated, each through pre-register +
full-space + blind-verify + premise-audit.

NEXT (Charles-gated): Q-MEASURE OBSERVE -- what natural measure does the UDT geometry put on
the space of winding configurations in the finite cell, and does the Born "square" come out
flat or metric-weighted? Observing, NOT targeting.
