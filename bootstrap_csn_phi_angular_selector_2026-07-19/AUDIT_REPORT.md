# Bootstrap/CSN Phi–Angular Selector Audit

Date: 2026-07-19

## Result

The frozen post–July-1 C0/C1 plus current UDT bootstrap/Common-Scale Neutrality source set does
**not derive** a native local selector that forces either a nontrivial lightlike `d phi` or one
uniquely repeated curvature direction.

Exact bounded verdict:

> `EXACT_CSN_INVARIANCE_OF_A_CHOSEN_ACTION_IMPLIES_A_GAUGE_NOETHER_IDENTITY_NOT_A_PHI_ANGULAR_EOM; BOOTSTRAP_SUPPLIES_GLOBAL_ADMISSIBILITY_NOT_CURRENT_LOCAL_SELECTOR; EIKONAL_UNIQUE_CONDITIONAL_ONLY_WITHIN_LOCAL_DIFF_COVARIANT_METRIC_PLUS_ONE_WEIGHT_ZERO_COVECTOR_HOMOGENEOUS_QUADRATIC_FIRST_JET_SCALAR_CLASS; ALGEBRAIC_SPECIALITY_CSN_COMPATIBLE_BUT_UNIQUE_PND_NOT_FORCED; CONDITIONAL_C2_BACH_AND_ZERO_LAMBDA_EH_DO_NOT_FORCE_TARGET; NO_LOCAL_SELECTOR_FOR_NULL_DPHI_OR_ONE_UNIQUE_REPEATED_PND_IS_DERIVED_FROM_THE_FROZEN_POST_JULY_1_C0_C1_PLUS_CURRENT_CSN_BOOTSTRAP_SOURCE_SET`.

This closes the question for that **audited affirmative source set**, not for every historical UDT
record or every future completion of the bootstrap principle. A future explicitly derived global
functional, representative-selection map, action, or boundary operator could add the missing
equation. No such object is present in the audited current sources.

The scope correction matters. `CANON.md` entry `C-2026-06-10-3` records a canonized nonstationary
`phi`-angular rung-2 weld. The controlling July-1 provenance firewall permits pre-July material here
only as failure/counterexample/question evidence, not as affirmative UDT physics. This audit neither
rederived that weld nor adjudicated whether it forces either requested selector. It is therefore
disclosed rather than silently erased or used to overstate source absence. See
`POST_PREREG_SCOPE_CORRECTION.md`.

## The structural point hiding in plain sight

Use logarithmic diagonal metric components only to expose the independent local variations. The
three relevant tangents are

\[
t_{\rm CSN}=(1,1,1,1),\qquad
t_\phi=(-1,1,0,0),\qquad
t_A=(0,0,1,-1).
\]

They have rank three and are mutually orthogonal in this bookkeeping basis. For a general metric
Euler covector `E=(E0,E1,E2,E3)`, their projections are

\[
E_{\rm trace}=E_0+E_1+E_2+E_3,
\quad E_\phi=-E_0+E_1,
\quad E_A=E_2-E_3.
\]

CSN controls the first direction. Reciprocity identifies the second as meaningful, and the full
angular geometry retains the third. Controlling one cannot set the other two to zero. Exact
trace-zero examples make the obstruction constructive:

\[
(1,-1,0,0):\ E_{\rm trace}=0,\ E_\phi=-2,
\qquad
(0,0,1,-1):\ E_{\rm trace}=0,\ E_A=2.
\]

Thus neither a reciprocal `phi` Euler equation nor an angular shear equation is a disguised CSN
trace equation.

## What exact CSN invariance would supply to a chosen action

CSN is a founding equivalence statement; by itself it does not supply an Euler tensor. If a chosen
action is exactly invariant under `g_ab -> Omega^2 g_ab` and any extra fields transform only by
algebraic conformal weights, its infinitesimal common-scale variation gives the Noether identity

\[
2g_{ab}E^{ab}+\sum_i w_i\Phi_i E_i=0,
\]

up to the corresponding boundary identity. Inhomogeneous or derivative field transformation laws
can add derivatives of Euler expressions. Either form is a gauge identity. In a metric-only class
the displayed formula reduces to a trace identity. It is an off-shell dependency among Euler
expressions, not an extra equation that selects a solution. Extra field terms cannot be silently
dropped to manufacture a `phi` equation.

This result is stronger than saying “CSN is inconclusive,” but it remains action-conditional. It
says exactly which equation-like statement **exact invariance of a chosen action** would supply and
why that gauge identity misses the reciprocal and angular directions absent an additional redundancy
theorem.

## What bootstrap currently supplies

The owner-stated principle says the realized universe is globally self-consistent and that complete
matter-bearing solutions occupy a narrow total-proper-density window. Under its registered primary
reading, this is an after-solution admissibility condition. It filters complete solutions after the
local equations, boundary, proper volume, and total ledger exist; it does not write a new local
Euler operator.

The two stronger placements remain formal possibilities:

1. A varied global constraint would give
   \(E_{ab}+\eta\,\delta B/\delta g^{ab}=0\), but the functional `B`, its fields, variation domain,
   multiplier rule, and boundary terms are not supplied.
2. A bootstrap-selected representative `Sigma:[g]_CSN -> g_*` would restrict the allowed tangents
   and produce a normal-to-section condition, but `Sigma` and that normal condition are not supplied.

Naming either formula does not derive its missing object. The prior bootstrap selector audit already
showed that after-solution, varied-constraint, and representative-selection placements are mutually
underdetermined by the present words. The new tangent algebra shows that this underdetermination is
exactly where a `phi`–angular correlation would have to enter.

## Strongest lightlike counter-derivation

For an independently defined, CSN-weight-zero scalar `phi`, and no additional fields, the eikonal
zero set

\[
P_\phi=g^{ab}\partial_a\phi\partial_b\phi=0
\]

is conformally well typed because `P_phi -> Omega^-2 P_phi`. Moreover, inside the deliberately narrow
class “local, diffeomorphism-covariant, metric plus one weight-zero covector,
first-derivative-only, nontrivial homogeneous degree-two scalar equation,” this norm is the sole
contraction, up to a
nowhere-zero coefficient function of `phi`. The nowhere-zero condition matters: allowing the
coefficient itself to vanish adds separate algebraic branches. The lightlike equation is therefore
`UNIQUE-CONDITIONAL` only inside that narrow class.

That is the strongest honest derivation found. It does not close the native question because every
class premise just named remains open: whether `phi` is an independently varied field, absence of
extra fields, locality, first-derivative order, scalar rather than tensor equation,
homogeneous-degree-two minimality, and the bootstrap placement. General `F(phi,X)=0`, a vanishing
coefficient, higher jets, extra fields, and tensor equations lie outside the uniqueness statement.
CSN makes the eikonal zero set compatible; it does not prefer it over Bach, Weyl-speciality, or
other conformally typed zero sets.

## Strongest repeated-curvature counter-derivation

In the inherited conditional four-dimensional Petrov arena, the speciality equation

\[
\Delta_W=I^3-27J^2=0
\]

has a conformally invariant zero set. But its exact root census is

| Type | PND multiplicities | Unique highest-multiplicity line? |
|---|---:|---|
| II | `2,1,1` | yes, locally |
| D | `2,2` | no: two repeated lines |
| III | `3,1` | yes, locally |
| N | `4` | yes, locally |
| O | Weyl zero | no curvature-selected line; null directions still exist geometrically |

Therefore speciality alone cannot force one unique repeated direction. A type-II/III/N branch
selector and a rule aligning that direction with null `d phi` would still be required. Neither
operator occurs in the frozen foundation. No Einstein dynamics or Goldberg–Sachs implication has
been imported.

## Exact conditional-action counterwitness

The audit also challenged the strongest accepted comparison routes. Take the generic exact Kasner
exponents

\[
(p_1,p_2,p_3)=(-2/7,3/7,6/7),\qquad
\sum p_i=\sum p_i^2=1,
\]

with

\[
ds^2=-dt^2+t^{2p_1}dx^2+t^{2p_2}dy^2+t^{2p_3}dz^2.
\]

The independent coordinate calculation gives `R_ab=0`. With

\[
t=(5\tau/7)^{7/5},
\]

the same metric has

\[
g_{\tau\tau}g_{xx}=-1,
\qquad
g_{\tau\tau}=-e^{-2\phi},
\qquad
g_{xx}=e^{2\phi},
\qquad
\phi=-\frac25\log(5\tau/7).
\]

It is therefore an exact nontrivial reciprocal representative, not a conformal rescaling. Yet

\[
(\nabla\phi)^2
=-\frac{4\,5^{1/5}7^{4/5}}{125\,\tau^{14/5}}<0,
\]

so `d phi` is timelike. Its PND quartic is

\[
-\frac{3}{49t^2}(z^2-4z-1)(z^2+4z-1),
\]

with nonzero discriminant

\[
\frac{1194393600}{13841287201t^{12}},
\]

so it is Petrov I with four simple PNDs. Ricci-flatness makes it both an exact conditional
zero-`Lambda` EH vacuum witness and Bach-flat in four dimensions. Thus neither named conditional
action tile forces the requested lightlike or repeated-direction target.

This Kasner metric is a load-bearing **conditional comparison counterwitness**, not a complete UDT
universe. It has no native matter carrier, finite-cell boundary completion, total-density closure,
or physical-selection proof. It refutes automatic implication inside the named action classes; it
does not refute a future complete bootstrap operator.

## Angular sector and global continuation

The angular sector is not decorative. Its trace-free tangent is precisely one of the two directions
left unconstrained by the CSN trace identity. Rounding the angular metric would hide this fact and
would amount to choosing the desired closure. No rounding, torus, section, or transport law was
installed here.

The current static seal authority fixes limited parity/value information for `phi`; it does not fix
the normal derivative, the angular shape, the full boundary action, or the continuation of a Petrov
branch. Likewise, one global density-window statement cannot become a pointwise anisotropic tensor
equation without an explicit functional that maps global closure back into local variation.

## What is genuinely missing

The smallest missing object is not another random metric ansatz. It is one explicit, derived
**bootstrap-to-local map**: either

- a global functional `B` whose variation has a definite `phi`–angular projection;
- a representative section `Sigma` whose normal condition correlates reciprocal and angular shape;
- or a native action/boundary equation that supplies those projections directly.

Until one of those is derived, the eikonal and repeated-PND conditions remain disciplined candidate
equations rather than consequences of the audited post–July-1 C0/C1 plus current CSN/bootstrap
source set.

## Evidence gates and maximum conclusion

1. **Preregistered:** yes, commit `4e5b0ba413d83d9c69c972a11517e42b18b52005` predates algebra.
2. **Full space or bounded scope justified:** bounded twelve-family operator-selection tile, not a
   complete invariant/action/history census; exact omissions and the post-preregistration narrowing
   are in the preregistration, correction layer, and status ledger.
3. **Independently verified:** required before final banking; see `VERIFICATION_RESULT.json` and the
   external adversarial review.
4. **Every premise audited:** yes within this tile; action, fields, locality, derivative order,
   boundary, carrier, and global completion remain explicit.

Maximum conclusion: no local selector for null `d phi` or one uniquely repeated PND is derived from
the frozen post–July-1 C0/C1 plus current CSN/bootstrap source set. This does not establish absence
from every historical record and does not establish that no future UDT bootstrap completion can
supply one. No carrier, complete action, mass, stability, cosmology, or new canon claim follows.
