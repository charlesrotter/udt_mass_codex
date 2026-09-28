# Kernel peer critique of horizon HR1/HR2

Verdict: **the stated static radial restrictions survive this scoped check**.
No algebraic defect was found in HR1's tape/affine bridge, its convergence
counterexamples, or HR2's acceleration/curvature relation. Three integration
clarifications below are needed when combining this note with ordered-pair kernel
claims. They do not select a physical lapse law, admit these metrics as native UDT,
or complete the campaign's fresh adversarial review.

Target: horizons/INITIAL_NOTE.md, SHA-256
`f01a54ae65ea3c6a1c107c0e2b8cc24632f6d83eb5ba333134f28ee1717d1b13`,
principally sections 3–4. My initial kernel note was sealed first, hash
`3a50ac98902b6323f24c7bd68e406d3a93945c58a8713f1cfef8625bf53bc9b0`.
I then read the horizon note, seal and check contract. I did not read or reuse the
horizon author's implementation. This is a distinct construction context reused
from OFS1 empirical work, with its numerical outcomes already exposed; neither a
fresh-context nor different-model claim is made. No coefficients enter this check.
The parent reports its sole full 406-row premise audit passed. Actual runtime model
identity is not independently attested. HEAD remains the launch's
`be806b1830b24328caf47d99328fc1ecf992e6fe`; no git mutation was performed here.

## 1. Original-metric derivation of the bridge

For the supplied static sector `g=-N(l)^2 dt^2+dl^2`, with positive smooth N,
the nonzero connection coefficients are

    Gamma^t_tl=Gamma^t_lt=N'/N,    Gamma^l_tt=N N'.

The static unit observer is `U=N^-1 partial_t`. For each affinely parameterized
radial null ray with positive conserved Killing energy E, both tangents

    k=(E/N^2) partial_t ± (E/N) partial_l

satisfy the original null constraint and both original affine geodesic equations.
The measured frequency is `omega=-g(U,k)=E/N`. Taking the reference observer at
N=1, its received interval factor for a source at l is `R=1/N(l)`.

This exact pullback has G176's T=N, L_sigma=1, beta=0 for sigma=l. Its uniquely
positive working reciprocal density is m=N. Since N is time independent here,
`s(l)=integral N(l) dl` is a valid coordinate on every connected open N>0 interval.
The transformed metric has determinant -1 and radial entry N^-2, and

    ds/dlambda=±E,       Delta lambda=|Delta s|/E.

Thus the asserted finite/infinite equivalence holds for these radial null rays.
It uses Killing conservation in addition to calibration. G176 alone supplies no
affine completeness theorem. It also supplies no physical event/path selector.
For a time-dependent m, `m dl` need not be an exact spacetime coordinate differential;
for a shifted/full metric, the original null equation and conserved quantities must
be recomputed. Transverse contributions cannot simply be dropped when forming the
actual pair pullback. These are correctly excluded by the horizon note.

**Clarification C1 — normalization across a family.** The equivalence is about a
single extended ray with fixed nonzero affine normalization, or rays compared at a
common reference energy. Finite versus infinite extent of one ray is unchanged by
any fixed positive affine rescaling. However, a different rescaling for each member
of a source family can change the limit of its finite interval lengths. For example,
fixing unit emitter frequency gives `E_l=N(l)`, so a source-to-reference length is
`[integral_0^l N(u) du]/N(l)` rather than the common-reference-normalized integral.
That quantity can diverge even when the maximal ray has finite affine extent.
Smallest repair: add “for a fixed ray normalization, or common reference-clock
normalization across the source family” when reporting HR1's affine limit.

## 2. Ordered depth must retain its sign and query

The horizon note explicitly defines its delta as `-log N`, and its check contract
already calls it a source-to-reference redshift depth. Its formulas are internally
consistent. To join G220, however, label this quantity `delta_z=log(1+z)`:

    R_emitter,reference=1/N,
    delta_G220(emitter,reference)=-log R=log N=-delta_z.

At the exact anchor N=1/2, R=2, delta_z=log 2, while the ordered emitter-to-reference
depth is -log 2. In the common static time chart, the local G176 coefficient
Phi(source)=-log N(source) equals delta_z only because Phi(reference)=0. The
G220 ordered difference is Phi(reference)-Phi(source). The source-proper-time pair
chart's target clock T_B=R is yet another explicitly normalized statement of the
same ordered received comparison; it is not T=N_source.

**Clarification C2 — typed notation.** Use delta_z or state this minus sign next to
HR1 when integrating the lanes. The current definition is not an algebraic error;
silently substituting it for the ordered pair depth would be one. Neither a local
static clock coefficient nor this received factor identifies an arbitrary full
kernel pair without its actual comparison data.

## 3. Endpoint, extreme-factor and extension checks

For N_p=(1+k l/p)^(-p), positive k,p, differentiation verifies both quoted
primitives. At large l the lapse is a positive constant times l^-p, so comparison
with the p-integral proves the full p<=1 versus p>1 classification, beyond the
three explicit symbolic limit anchors p=1/2,1,2. All profiles have the same first
depth slope k at l=0, and p=1/2 and p=1 both satisfy infinite affine extent. That
is an actual counterexample to uniqueness under the listed endpoint and first-slope
conditions, not evidence about a larger unsampled class.

For exponential N=e^-kl, the affine integral is finite, 1/(E k), whereas static
proper and optical extents are infinite. In the Eddington chart the metric is

    g=-(1-k s)^2 dv^2+2 dv ds.

I recomputed determinant -1 and scalar curvature -2 k^2 from this metric. The
constant tangent `(dv/dlambda, ds/dlambda)=(0,-E)` is an exactly affine null
geodesic through s=1/k, with Killing energy E. It provides a concrete regular
crossing; no appeal to a redshift plot is needed. This ingoing chart regularizes
one horizon direction; the retarded chart analog covers the opposite direction.
The check establishes a local extension and crossing, not a maximal extension or
complete classification of all causal geodesics.

**Clarification C3 — metric versus clock-pair regularity.** At N=0 the extended
metric is regular but the selected static Killing vector is null. The normalized
static observer U=N^-1 partial_t and the positive regular static G176 comparison
do not extend through that locus as those same objects. A divergence of their
depth is compatible with regular crossing clocks from another congruence. Smallest
repair: make this type boundary explicit whenever the extension is combined with
the native kernel's regular-pair restriction.

The reciprocal-coordinate power-law endpoint test also survives: proper length
uses integral f^-1/2 ds, optical time integral f^-1 ds, while radial affine length
uses ds/E. Leading positive asymptotics give the q<2 and q<1 thresholds by direct
comparison. Those asymptotics alone do not control derivatives or extension;
the author's explicit caution is necessary. Exact linear/quadratic f have smooth
Eddington metrics, while arbitrary powers do not inherit this automatically.

## 4. HR2, local extrema and the native gap

The original connection gives a_l/c_E^2=N'/N. Direct curvature contraction gives
R=-2N''/N in the stated convention. Substitution of delta_z=-log N then gives
K=(delta_z')^2-delta_z''. A local depth extremum has zero static acceleration,
but can retain nonzero curvature through `K=-delta_z''`; a vanishing first-order
clock slope is not flatness or absence of finite-separation shifts.

The finite-distance acceleration bound is valid without requiring monotonicity:
if |a_l|<=a_max on the interval, integrating |delta_z'| proves the Lipschitz bound.
Removing monotonicity broadens a mathematical survivor, but no physical history is
thereby admitted. Continuous supplied K and two initial data determine N locally
through the original linear ODE until positivity fails. A lapse law may equivalently
be characterized by other native relations; HR2 does not prove those particular
data must be separately observed or that every imaginable boundary condition fails
to select a profile. The defensible nonselection statement is the explicit one:
the endpoint tests and common initial slope examined here leave multiple profiles.

Nothing here closes G312 membership. Even a fully verified four-dimensional product
metric would remain a supplied comparison absent the native realization argument.
Staticity, radial symmetry and the positive-lapse interval are substantial class
restrictions, not consequences of the primary scalar tanh readout. Native progress
would be a source-supported restriction on realized clock/congruence/curvature
data with the correct pair assignment, not rebranding this useful evaluator as a
selector.

## 5. Actual checks and limits

PEER_CHECK_FREEZE.md preceded computation. The independent script
peer_check_horizons.py ran once under the command

```bash
timeout 600s python3 udt_common_geometry_whiteboard_2026-09-28/kernel/peer_check_horizons.py > udt_common_geometry_whiteboard_2026-09-28/kernel/peer_check.stdout.txt 2> udt_common_geometry_whiteboard_2026-09-28/kernel/peer_check.stderr.txt
```

Exit 0; Python 3.10.12, SymPy 1.13.1; 0.2673 seconds; peak RSS 52,212 KiB.
All 37 assertions passed: 32 exact zero residuals, three explicit tail limits and
two negative controls. The latter reject the wrong ordered-depth sign and an
optical/affine density identification at N=1/2. No failed execution occurred;
stderr is empty. Script, outputs, freeze and target hashes are in
PEER_REVIEW_SEAL.json. Exact computation checks the displayed mathematics; it
does not establish source admission, chronology, truth of a physical model, or
independence merely by possessing hashes.

I did not replay the author's boost, accelerated-observer or Schwarzschild
calculations, audit the external reading/download history, classify global
extensions, test general full-metric pair construction, run observations/fits, or
repeat the parent's premise census. Existing initial artifacts were preserved.
The substantive analytic checks plus separate implementation support HR1/HR2 in
their exact stated class. Fresh adversarial review remains the parent's next gate.
