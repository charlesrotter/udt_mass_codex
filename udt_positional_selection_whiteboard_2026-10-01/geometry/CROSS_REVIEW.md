# PSW1 geometry cross-review

Reviewer: `/root/psw_geometry`, inherited model, actual separate context from the
parent and other two specialists. Review date2026-10-01. Verdict:
**VERIFIED-WITH-CAVEATS on the local mathematics; one control-domain precision
repair requested before final integration.** Physical join J1 remains OPEN and
explicitly UNADOPTED. No scientific grade or physical adoption follows.

Candidate independently hashed:
`INITIAL_CANDIDATE.md` SHA256
`95ed91cca818cd6f1b7de819396f61ad2a24dc741f763334ed52e7bf769ad1b1`.
The parent freeze and the three source-first notes were visible for this review.
`PRIMARY_METHOD_REFERENCES.md` was read as the parent's source-inspection report;
this reviewer did not independently browse or attest those external inspections.
NCI1's original criterion and its two precision repairs were read directly.
Exact cross-review input hashes are in `CROSS_REVIEW_HASHES.json`.

Exposure/independence: I authored Route A's original one-leg source-first note,
so I am **not independent of its discovery or code**. I fixed that note before
seeing peer proposals. This pass read both peer notes and the parent synthesis.
The following small-loop holonomy argument is an additional analytic method
relative to the Fermi arrival calculation, not a different-model review or a
new independent implementation. I used no scientific CPU slot in this pass.
My previously captured14 symbolic controls are attributed regression evidence;
they are not relabeled as newly independent checks of the general4D theorem.

## 1. Actual future return: coefficient3/2 survives

The reciprocal return would be wrong, but that is not what the candidate uses.
In a static signed-lapse control write `N=1+eL^2/2+O(L^3)` at first relay.
The released receiver's physical radial speed there is
`v=-eL^2+O(L^3)`, so `gamma=1+O(L^4)`. Photon Killing energy and the actual
endpoint clock contractions give

    p=N/[gamma(1-v)]=1-eL^2/2+O(L^3),
    q=gamma(1+v)/N=1-3eL^2/2+O(L^3).

The return clock is the central clock at a later event. This verifies the factor
three by endpoint frequency, without replacing `q` by `1/p`, holding the receiver
fixed, or differentiating a single flight duration. The branch emitted near zero
always uses the same released receiver worldline; re-preparing it on every tick
would change the problem. The candidate expressly excludes that change.

## 2. General4D check through a different geometric argument

The general4D concern is real: a radial pair surface need not be totally geodesic.
The claimed coefficient nevertheless survives, as can be seen without assuming
a two-dimensional metric restriction. Use the exact R6 endpoint-frequency law
and compare the endpoint unit clock vectors by Levi-Civita transport.

At leading order the outgoing geometry is the small triangle with tangent-plane
vertices `o=0`, `B0=Ln`, and relay `b=L(n+U)`. The broken path `o→B0→b` transports
U to the receiver's actual velocity: first by its physical preparation and then
by its geodesic evolution. The path `o→b` transports the emitter velocity along
the actual outgoing null ray. Close the loop by reversing the null leg. The
loop has oriented `(n,U)` area `L^2/2` to leading order.

For the candidate curvature convention, the leading transport difference around
this loop is `-L^2 R(n,U)/2`. This follows from the defining curvature commutator,
or by expanding the connection integral around a small loop; variations of
curvature contribute O(L^3). Thus the difference of the two transported clock
vectors at b is `-(L^2/2)R(n,U)U+O(L^3)`. Its contraction with the leading
future outgoing ray `U+n` picks out
`g(R(n,U)U,n)=e`, while the U contraction vanishes by metricity. Consequently
`omega_b/omega_o=1+eL^2/2+O(L^3)` and `log p=-eL^2/2+O(L^3)`.

For the future return compare the broken preparation/receiver/null-return path
`o→B0→b→a` with the emitter's central geodesic `o→a`, where
`a=2LU+O(L^3)`. Its quadrilateral has leading `(n,U)` area `3L^2/2`.
The transported receiver velocity differs from the central final velocity by
`-(3L^2/2)R(n,U)U+O(L^3)`. Contracting with the leading incoming ray `U-n`
now gives `omega_b/omega_a=1-3eL^2/2+O(L^3)`. Hence
`log q=-3eL^2/2+O(L^3)`, in agreement with the arrival calculation.

Curvature also sends vectors transverse to n. Those changes have zero leading
contraction with U±n; no transverse-curvature vanishing or totally geodesic plane
is imposed. Actual clock/ray positions differ from their tangent-plane segments
at higher order. Smooth fixed geometry makes the holonomy remainder O(L^3).
This argument uses full4D parallel transport; it supports the general coefficient
more directly than only checking a radial product metric.

The Fermi proof is consistent with this check. Its quadratic `g_0n` and
`g_nn-1` contractions vanish by Riemann antisymmetry along a radial initial line.
The parallel-prepared initial velocity can have transverse O(L^2) components,
but has no radial O(L^2) correction. Its transverse displacement during the
O(L) flight is O(L^3); it changes the leading radial metric/frequency contraction
only at higher order. The central receiver and emitter proper times remain
ordinary. No unaccounted O(L^2) scalar survives from those transverse terms.

## 3. C1 remainder and local scope

An O(L^4) arrival-value remainder alone cannot be differentiated without control.
The candidate explicitly claims C1 Taylor control rather than taking that step
silently. A precise justification is to put `t=L tau`, `x=L y`, and `s=L sigma`
for a fixed compact range of sigma. The rescaled metric and clock/branch problem
have a smooth L→0 limit given by a fixed Minkowski laboratory. In that limit
each arrival is transverse. Applying smooth geodesic dependence and the implicit
function theorem to the **rescaled** incidence problem yields a smooth arrival
map jointly in `(L,sigma,n)` for small L. Differentiating in physical s removes
one factor L, so a C1 controlled cubic-jet error in the rescaled arrival gives
the required O(L^3) clock-ratio remainder. The direction sphere is compact;
uniformity in direction is local to the fixed bounded metric neighborhood.

The unrescaled coincidence problem at L=0 would have a degenerate null endpoint
condition; using a bare implicit-function assertion there would be a gap. The
rescaling resolves that issue. I recommend making this reasoning explicit in
the controlling precision record, but do not find a false coefficient. The
independent holonomy/endpoint derivation above also obtains the ratio remainder
without differentiating an uncontrolled flight-time error.

There is no finite-size numerical bound, universal metric-independent radius,
late-time asymptote, global ray guarantee or solar precision result. The candidate
retains these limits. Higher-order signs remain undecided when the displayed
coefficient vanishes.

## 4. Actual defect: complete control domain must include every scale factor

**Location:** INITIAL_CANDIDATE section3 gives the axial positive-kappa condition
`2kL<pi/2` and mentions degeneracy for the negative-kappa formula, but does not
explicitly require positivity of all three `a_j` along both flights.

**Reason/counterexample:** set `(kappa_1,kappa_2,kappa_3)=(1,-100,0)` and take
the axis1 experiment with `L=1/20`. Its displayed condition `2L=1/10<pi/2`
holds. The formal axis1 return time is `tan(1/10)>1/10`, while `a_2` vanishes
at `t=1/10`. Thus that axial bound alone does not ensure a regular Lorentz4
return history. The problem is control-domain completeness, not the axial
integral or the main local theorem. The generic smooth-Lorentz hypothesis should
not be left to repair an apparently sufficient explicit control bound.

**Smallest repair:** add: "All three positive representatives `a_j(t)>0` must
remain positive on an open neighborhood containing preparation and both null
legs and clock histories; in particular every negative kappa_j imposes
`t_return<1/sqrt(-kappa_j)` for these s=0 controls. Restrict nearby emissions as
well. The displayed tan/tanh formulas require this common-domain condition."
For isotropic negative controls the tanh arrival automatically obeys its common
bound; for anisotropic controls the other directions can impose the first stop.

**Survivor:** both exact axial formulas, their1:3 expansion, the shared initial
preparation, and the sign/anisotropy controls survive on the stated common
regular domain. Their `kappa_i` are supplied off-equation controls. These are
not Ricci-flat alternatives or native-admitted UDT countermodels.

## 5. Endpoint factorization, signs and ownership

Direct reading of NCI1 plus REPAIR confirms the stated criterion:
`-log Z=Delta Psi` on **every short future null segment** iff
`exp(-Psi)U` is conformal Killing. The local condition is neighborhood-wide
zero shear and closed `alpha=a_flat-H U_flat`; global exactness also requires
zero periods. Vanishing at one event is insufficient. The all-null quantifier
belongs to the tested property, not a claim that every direction is populated.

For equal positive representatives `a=1+kappa t^2`, the vector `aU` is conformal
Killing and `Psi=-log a`. Either sign of kappa is allowed on a regular domain.
For unequal kappa_i the quantities
`H_i=2kappa_i t/(1+kappa_i t^2)` differ at nonzero sufficiently small t; equality
of two on an interval would algebraically force equal kappa_i. Initial shear
zero therefore does not extend to a neighborhood. The synthesis is correct on
this point. It reuses a known optional restriction, not a native-derived selector.

The trace statements also survive: a triad recovers `Ric(U,U)` at leading order;
it does not establish an all-direction sign test. Nonzero trace-free T has
positive and negative directions. Negative Ric(U,U) gives a positive mean,
not negative-definite T. Ric=0 suppresses the leading mean but does not suppress
all finite/directional clock shifts. The Einstein Lambda example is conditional.

The strongest physical objection remains **J1**. These are ordinary geometric
tidal effects of a deliberately specified clock experiment. No inspected premise
identifies their net or comparator-excess coefficient as the positional effect,
or demands a positive L^2 term. The candidate states that gap at the correct
place and does not turn it into a refutation of UDT, a proof of postulate
insufficiency, a new response identification or a demand to select one universe.
DDR still constrains a specified E_response; it does not supply that E_response.

## 6. Return

Accept the conditional local coefficients and diagnostic interpretation, subject
to the explicit common-domain repair and preservation of J1. Prefer adding the
rescaled-arrival or small-loop explanation to the precision record because it
makes the general4D and derivative claims auditable. No second scientific
repair, new physical premise or computation campaign is needed on this review.
The fixed initial source notes and initial candidate must remain preserved.
Final review must bind the controlling repair and actual integrated bytes.
