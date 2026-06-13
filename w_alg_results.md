# W-ALG — Algebraic Exploration of the Solution Space: Results

Date: 2026-06-12. Driver: Claude. Push born from three Charles
instructions (this session): "force less, explore more" (do the
solution-space solve algebraically where possible); "the angular
sector is algebraic — it's probably just tying them together with
slightly more complex math"; and the founding INTEGER INSIGHT
(~2026-03, memory: integer-insight-origin) — a clean numeric constant
is a SEARCH KEY into exact space, not a measurement to refine.
Binding tripwire throughout: CLASSIFICATION, NEVER DEFORMATION (take
the derived equation exactly as given and ask whether mathematics has
already solved it — the nu = sqrt(17) Bessel precedent; never deform
toward a solvable cousin and bank the cousin's results).

Scripts: w_alg_class.py (19/19), w_alg_statics_fold.py (19/19),
w_alg_closure.py (15/15). Independent main-loop blind verifier:
VWALG = agent a96bb99b1da5aaa54 (own machinery, four scripts; all
three committed scripts rerun clean; theorem-grade content earned a
clean pass; the one mechanism claim refuted-as-reading, see below).
An arm-spawned verifier (ae8be76c472e65bf7) had already folded in
calibration; VWALG is the independent pass of record.

## HEADLINE 1 — the mystery constant is now an EXACT IDENTITY

The W4/VB4 "1.90-class" selection ratio, banked for two sessions as a
member-independent number nobody could derive, is on the flat-weight
(f ~ 1/r) member EXACTLY:
    kappa_s/kappa_c = 2 pi^2 / (3 G*) = 1.87252511385...
where G* = 8 s*^2 sech^2(s*) = 3.5138307191... is the classical
GELFAND-BRATU constant (s* the root of s tanh(s) = 1). VWALG
independently re-derived G* by solving the classical Bratu BVP fold
from scratch (same number), confirmed the "3" is FORCED (= -d/dv
(e^{-2v} - e^v)|_0, not tuned), confirmed the Bratu map y = -2v is a
genuine point transform of the DERIVED static EL (not a deformation),
and settled the cancellation as REAL (every member parameter
a, a_u, u, T0 cancels; VWALG's first apparent refutation was its own
chart-factor error, corrected). Fold and gap are the SAME
Sturm-Liouville operator (saddle-node of the beta=0 nonlinear BVP vs
zero of its linearization at beta=1) — not a flat coincidence. The
banked member spread 1.89-1.90 is now a COMPUTABLE weight-non-flatness
correction (+1.2-1.6%), not numerology. This is the integer insight
vindicated: the digits were a key; the lock was Gelfand-Bratu.

Banked numerics -> identities (for any future sweep, these are now
LOOKUPS not measurements): 1.87253 -> 2 pi^2/(3 G*); 3.513830719 ->
G* (root of s tanh s = 1); the source exponent pair (+1, -2) and the
-2/f weight mismatch -> the Tzitzeica integrable member's exponents;
the OFF fold kappa_s = (1 - u^2) a_u^2 T0^2/(4 G* a^2) on the flat
member (closed identity to check numeric folds against).

## HEADLINE 2 — the angular sector closes algebraically, and points
## at a NON-resonator discreteness candidate (theorem core + a
## hypothesis-grade reading, firmly separated)

THEOREM-GRADE (VWALG-confirmed by independent re-derivation): on the
q* branch the (r,theta) block determinant is D|q* = r^2 W Delta_w^2/P^2,
so both spatial signal speeds c_ang^2 = f/D and c_rad^2 = f^2 r^2 W/D
DIVERGE as 1/D at Delta_w = 0; the latitude u*^2 = 1 - a^3 W/(a_u^2 r)
is a genuine IRREGULAR CHARACTERISTIC SURFACE of the coupled wave
operator; the COUNT of such latitudes = deg(Delta_w in u^2) and RISES
with angular harmonic content (an ell=2 lobe lifts the count 2 -> 6).
This is the Delta_w surface for the fourth time (W3 turning surface,
W4 dressing zero, W5 q-elimination breakdown, now coupled-operator
characteristic) — one locus, now four-way characterized. The
discreteness candidate it suggests is NOT the single-cell resonator
template (mass as a mode eigenvalue): it is discreteness as CELL
COUNT — the sphere potentially partitioning into a discrete,
ell-dependent number of angular cells (the orchestra / finite-cell
picture, Charles's standing reframe destination).

HYPOTHESIS-GRADE, REFUTED AS A MECHANISM (VWALG, load-bearing — do
NOT upgrade): the inference "degenerate characteristic => zero angular
flux => insulating wall => discrete cell count" is unsupported and
sign-backwards — at Delta_w -> 0 the speeds DIVERGE (signals cross
instantly; a type-change/horizon-like surface) and the flux
coefficient g^{thetatheta} = 1/D BLOWS UP rather than vanishing;
finite energy forces a Neumann-like turning condition (d_theta u -> 0),
which is NOT a zero-flux wall decoupling the sphere into dynamically
independent cells. And (banked W5) the q-elimination itself breaks
down at Delta_w = 0, so the "characteristic" is partly an elimination
artifact; the unreduced 3-field EL is finite there. The cell-partition
leap is the resonator-template risk in new clothes and must remain a
labeled hypothesis pending a genuine W6 DYNAMICAL FLUX TEST (march the
coupled (f,q,w) operator across a u* latitude on a trust window and
measure actual angular energy current). SCOPE FLAG: u* is real only
in the OUTER radial band r > a^3 W/a_u^2 — absent in the deep core;
the wall-count is a flat-member result, untested for C(u) != 0.

## Integrability classification (VWALG-confirmed)

The derived per-ray wave sources are EXACTLY integrable exponential
members of the Mikhailov-Shabat-Zhiber list, taken as derived (no
deformation): OFF = LIOUVILLE (general solution e^{-2V} =
-/+ 4 F'G'/(F+G)^2, two free chiral functions, both sign branches
verified by substitution); ON = TZITZEICA / Dodd-Bullough-Mikhailov,
exponent pair (+1, -2) — the SAME integer pair as the -2/f weight
mismatch (consilience, not coincidence). WTC/Painleve: ON slice
PASSES (resonances {-1, +2}, j=2 compatibility identical); off-slice
OBSTRUCTED, the obstruction closing exactly to
-psi'^2 (ln K)''/K^2 (integrable iff K exponential in tortoise x — the
SAME family the Lie-symmetry analysis independently selects). The
transport obstruction beta = 2f/r is a point-invariant: NO
non-spherical vacuum-family background is globally integrable (clean
scoped death). f ~ 1/r (rho = 1) is the UNIQUE exactly-solvable
radial scaling; all rho != 1 collapse to one scale-invariant
Emden-Fowler class.

## Spectra and statics (VWALG-confirmed)

The dressed radial pencil on the flat member is EXACTLY POSCHL-TELLER
(lambda = 1, reflectionless); its even zero-energy mode 1 - X tanh(X)
solves the linearized equation identically and hits Dirichlet exactly
at the fold s tanh s = 1 (zero eigenvalue <=> fold, theorem-grade on
the member; the dev-note correction from sech(X) to 1 - X tanh X is
sound). Static OFF EL -> standard Bratu under y = -2v (genuine point
transform), closed-form general solution
v = ln[(sqrt(Phi)/theta) cosh(theta(m - m0))]; ON statics reduce to
the exact elliptic quartic y_m^2 = -Phi y^4 + 2E y^2 - 2 Phi y.

## What this changes (the method verdict)

Charles was right: much of the solution-space solve IS algebraic, the
angular sector closes in closed form, and the suspicious numerics were
exact constants in disguise. The exact-solvability is now an
established PATTERN of the theory, not a string of coincidences
(perfect squares, nu^2 = 17 - 8n, the exactly-free v-chart, the
envelope theorem, exact rationals, and now Gelfand-Bratu /
Liouville / Tzitzeica / Poschl-Teller). Going forward, banked
numerics are treated as search keys first; numeric sweeps validate
and locate, they do not define constants.

The discreteness question now has a SHARP, NON-TEMPLATE form and a
SHARP test: is the Delta_w characteristic an insulating wall (=> a
derived, ell-dependent angular CELL COUNT — discreteness without a
resonator) or a benign coordinate type-change? That is a dynamical
energy-flux measurement on the coupled operator, and it is the live
W6 deliverable.

## Registry / discipline

- NEW #30 appended: the W4/W5 selection ratio = 2 pi^2/(3 G*) exactly
  (flat member; Gelfand-Bratu); the per-ray sources are
  Liouville/Tzitzeica integrable; f ~ 1/r the unique solvable scaling;
  the Delta_w characteristic + ell-rising wall-count are theorem-grade
  but the INSULATION/cell-partition reading is hypothesis-grade
  (VWALG-refuted as a mechanism — Neumann turning, not a flux wall;
  partly a q-elimination artifact). Premise set: flat C=0 member;
  q*-branch; frozen-f; outer radial band for u* reality.
- All kappa != 0 physics remains hypothesis-grade; the exact
  identities (ratio, G*, integrable classes, Poschl-Teller, Bratu
  closed forms) are theorem-grade on their stated members.
