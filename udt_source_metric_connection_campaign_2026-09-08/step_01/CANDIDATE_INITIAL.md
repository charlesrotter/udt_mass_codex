# SM1 initial candidate — regular spacetime-current correspondence

Explored then frozen for review,2026-09-08. CONDITIONAL CANDIDATE, not accepted.
General argument below is distinct from finite symbolic regression anchors.
Sources/pins: ../SOURCE_LEDGER.tsv. No curvature recipe or source equation.

## Question, domain and supplied inputs

For every smooth oriented/time-oriented Lorentzian four-dimensional regular
flow tube of signature(-+++), suppose a supplied smooth phase Theta has
nonzero future-raised null gradient, and Delta>0 is a supplied CONSTANT phase
spacing. Write phi=Theta/Delta and ell=grad(phi). Supply compatible flow and
cross-phase label data: two labels y=(y1,y2), constant along ell, identified
across phase sheets, with each (phi,y) identifying a ray. Restrict to a local
flow box with affine parameter r, ell=partial_r, and rank-two regular cuts.
This is a FOUR-dimensional family of three-dimensional null phase sheets,
not a current reconstructed from a single two-dimensional cut or null sheet.
Given full metric/phase data, local flow-box existence follows from nonzero
ell and dphi; it does not construct that phase from the metric or promise a
global extension. Labels across sheets and their product identification remain
supplied. No caustics, singular measures, atomic counts or global claims.

Use the G351 smooth absolutely continuous subdomain dmu=s(y)|dy1dy2|,
s smooth positive on the patch, finite on the chosen label domain. Smooth
nonnegative s, including zero, also satisfies the formulas without divisions
by s. G352's CHOSEN continuous product is |dphi| tensor mu; s is independent
of phi in these supplied cross-phase labels. The spacetime metric may be an
admitted vacuum development, but the geometric argument itself needs no field
equation. Metric, phase/spacing, populated measure, labels, queries and local
domain are not selected. They are free-and-explored/supplied, not hidden laws.

## General construction and proof

Null exact gradient implies ell^a nabla_a ell_b = (1/2)nabla_b(ell^2)=0.
Choose r along this affine field and a transverse section on which (phi,y)
are coordinates. Since ell(phi)=0, the resulting adapted chart satisfies
g_{rr}=0, g_{rA}=0, g_{r phi}=1. Consequently

    g = 2 dr dphi + H dphi^2 + 2 A_A dphi dy^A + q_AB dy^A dy^B,
    det(g) = -det(q),                  J = sqrt(det(q)) > 0.

q is the positive screen metric. No claim that arbitrary H,A,q satisfy the
vacuum equation is needed. On a fixed-phi graph cut r=R(y), terms added to
tangents are multiples of ell; their inner products vanish in the screen.
Thus its area density is J evaluated on that cut (G348/G349).

Choose compatible local orientation epsilon=J dr wedge dphi wedge dy1 wedge
dy2 and eta=s dphi wedge dy1 wedge dy2. Eta is the oriented representative
of the supplied quotient product, pulled back along the ray projection. Set

    i_j epsilon = eta,           j = n ell,             n = s/J.       (SM1.1)

Contraction with a nonvanishing four-volume is an isomorphism from vectors
to three-forms, so this current is unique at these fixed inputs. Since

    nabla_a j^a = J^(-1) partial_r(J n) = J^(-1) partial_r(s) = 0,     (SM1.2)

the current is conserved. Equivalently d eta=0. Future direction is fixed by
ell and s>=0, not by an arbitrary chart orientation. For an orientation-
reversing relabel, transform BOTH volume and product representatives with
their consistent orientation; the vector does not reverse. Ratios s/J are
ratios of positive densities and hence label-coordinate scalars.

For every supplied future unit timelike observer U, with G352 omega=-U(Theta),

    -g(U,j) = (s/J)(-U(phi)) = (omega/Delta)(s/J) = Gamma.             (SM1.3)

This is equality to the admitted local continuous readout. It does not derive
an instrument, a detector area, energy, physical counting, or flux across an
arbitrary detector surface. Current flux across a specified transverse
three-surface is eta pulled back there; a separate measurement interpretation
is not supplied by writing a spacetime current. Equality for ALL future unit
timelike U would also uniquely determine j: the difference covector vanishes
on that hyperboloid and, by positive homogeneity, on the open timelike cone,
so vanishes identically. A single observer query alone is not such uniqueness.

## Exact converse, gauges and remaining freedom

For any smooth aligned current j=f ell in the same tube,

    div(j)=0 iff J f = S(phi,y), independent of r.                    (SM1.4)

The chosen G352 product further requires S independent of phi in the supplied
cross-phase label identification. Conservation alone does NOT impose this.
For example on a flat adapted tube with J=1, f=2+sin(phi) is positive and
conserved but is not the fixed phase-independent product. It is not a failure
of the metric equation or a source/sink along a ray.

Under the admitted simultaneous affine gauge Theta -> a Theta+b,
Delta -> a Delta (a>0), dphi and ell stay fixed, so j and Gamma stay fixed.
Consistent label relabeling transforms s and J by the same absolute Jacobian;
the current is unchanged. Ray-origin shifts r -> r+b(phi,y) leave ell and the
screen density unchanged at the same event. Rescaling mu changes j and Gamma;
it is not a gauge. Arbitrary nonlinear phase reparameterization is not claimed
as a G352 fixed-spacing symmetry. No phase-independent product is inferred by
changing labels after the fact.

The full metric/phase extension off a cut, cross-phase label/product choice,
mu normalization/profile and observer queries remain supplied. Current
conservation does not choose them. Conversely their being supplied does not
by itself make each an additional physical law. A spacetime representation
does not promote any of them into independent gravitational degrees of freedom.

## Maximum conclusion and verification separation

SM1 proposes a GENERAL LOCAL CONDITIONAL correspondence, not another example
of the old recipe: in this smooth regular class the chosen product has a
unique aligned conserved current with exactly the G352 readout. Conservation
alone permits more phase dependence. Nothing here connects j to metric
evolution, adopts stress-energy, sums families, or establishes physical content.
Finite checks test algebra and deliberately defective substitutes only; the
general proof is what requires fresh separate-context review. Original
candidate/check history is retained even if narrowed or repaired.
