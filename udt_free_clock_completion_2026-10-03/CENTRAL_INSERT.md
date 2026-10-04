<a id="r16fcl"></a>

#### Free-clock endpoint control in nonuniform completion geometry — FCL1

FCL1 answers CPW1's specified pointwise question conditionally. Supply C3
Lorentz4 gbar and defining function x=Omega, with g=x^-2 gbar, x>0 inside,
nondegenerate gbar and nonzero timelike dx at a future spacelike boundary.
Supply one future unit timelike g-geodesic from finite interior data that
approaches a point p of that boundary. RG remains UNADOPTED. No field equation,
homogeneity, constant lapse or bound on T=u/x is assumed.

Flow along grad_bar x/gbar(grad_bar x,grad_bar x) supplies a local normal chart,
not an ansatz restricting the metric:

    gbar=-N² dx²+h_ij dy^i dy^j,  N>0, h positive,
    n=-N^-1 partial_x,  w_i=h_ij T^j,
    gamma=sqrt(1+h^ij w_i w_j),
    T^x=-gamma/N, T^i=h^ij w_j, dx/dtau=-x gamma/N.

The given endpoint ensures a final tail in a relatively compact subchart.
Metric regularity then bounds N,h, their inverses and first derivatives, without
bounding the receiver velocity. The normal chart has at least the C1 metric
coefficients needed for these estimates. The physical covector P_i=w_i/x obeys
the exact lowered geodesic equation dP_i/dtau=(partial_i g_ab)u^a u^b/2. Hence

    dw_i/dx=w_i/x+F_i,
    F_i=(partial_i N)gamma
        -N(partial_i h_jk)T^j T^k/(2gamma).

Spatial variation remains present. The compact metric bounds give
|F|<=C(1+|w|) for a finite local C. With s=log(x0/x), r=|w|, the upper norm
derivative satisfies

    D^+r<=(-1+C x0 exp(-s))r+C x0 exp(-s),
    r<=exp(C x0) exp(-s)[r(0)+C x0 s].

The second line follows by an integrating factor on each finite s interval;
boundedness is obtained rather than presumed. Therefore w=O(x[1+log(x0/x)]),
gamma->1, and **u/Omega->n_p**. Arbitrarily large finite initial velocity is
allowed for each receiver; constants are not uniform over a population.
The spatial equation gives y-y(p)=O(x²[1+log(x0/x)]). Consequently
N=N(p)+O(x), gamma-1=O(x²[1+log(x0/x)]²), and

    tau=-N(p)log(x/x_ref)+O(1).

The remainder after the logarithm has a finite limit. Physical future proper
time is infinite; the boundary is not a finite-time reception or material wall.
The two fresh source-first reviewers independently supplied another route:
for E=-gbar(T,n), a compact-tensor bound first bounds log E in the decreasing-x
direction; the forced equation for E²-1 then drives it to zero. That weaker
rate also proves the endpoint claim without a clock-velocity assumption.

For the clock conclusion, additionally supply the exact CPW1 interior-emitter
preparation: one regular emitter's compact proper-time interval away from x=0,
emissions approaching a regular interior limit, and a smooth unique conformal-null
family with regular nonzero endpoint tangents and affine data. Its physical
emission frequency has a finite positive limit before normalization. Scaling
each entire ray to omega_e=1 therefore preserves a finite nonzero limiting
conformal tangent K at reception. R6/R16CPW and the derived receiver limit give

    B_o=-gbar(kbar_o,T_o)->B*=-gbar_p(K,n_p)>0,
    omega_o=x_o B_o->0,
    Omega_o Z->1/B*>0,   Z=omega_e/omega_o->infinity.

The positive finite limit is the **rescaled** received frequency B, not the
physical received frequency. The regular ray family is supplied, not proved
to exist from RG alone. C3 geometry and its stipulated C2-or-better ray variation
cover the derivatives in R6: moving affine endpoints add only null-tangent
terms, which vanish on contraction. No C-infinity premise is needed. Conformal gauges x->a x,gbar->a²gbar with smooth finite
positive a preserve Z and rescale its x-residue by a(p). No numerical distance
scale, monotonic full-history curve or physical X_max follows.

One short exact control script checks six nonuniform metric/velocity cases by
original Christoffels and two actual ray/clock families in supplied g=x^-2 eta.
All pass, with a deliberately omitted force detected. The moving free receiver
has xZ->1. An accelerated unit receiver with rapidity log x instead has Z->1
and proper acceleration squared x^-2. That example lies outside the geodesic
quantifier; it strengthens CPW1's warning against using normalization alone.
These finite controls audit identities, not the general theorem by sampling.

FCW1's beta2/zero-gradient example remains outside RG, and its interior-bump
freedom still prevents unique history/scale selection. Physical RG admission,
native event/path assignment, positional attribution, global branch existence,
uniform populations, fixed-emission distance curves and echo availability remain
separate questions. Neither an Einstein equation nor a microscopic light theory
has been imported. The supplied geometry's normal is not an imposed finite-time
preferred observer population.

[FCL1 proof](udt_free_clock_completion_2026-10-03/INITIAL_CANDIDATE.md),
[reviewed scope](udt_free_clock_completion_2026-10-03/REVIEWED_RESULT.md), and
[descendant review](udt_free_clock_completion_2026-10-03/DESCENDANT_REVIEW.md)
retain the argument, independent routes, controls and hypothesis limits.
