# A — candidate universal vacuum quartic coefficient

Status: exploratory mathematical candidate for fresh adversarial review. This
extends, rather than rewrites, the two-control candidate in CANDIDATE.md. The
parent proposed the natural-jet classification after seeing both controls; this
proof attempt is cross-exposed and does not claim independent origin. GR vacuum
is a supplied mathematical comparison hypothesis, not adopted UDT physics.

## Statement

Let g be a smooth time-oriented Lorentz4 metric with Ric=0 on a neighborhood of
o, and fix a unit future U at o. Use the precise PSW preparation, two independent
first emissions and initial-sphere weighting in WORK_ORDER. Then the candidate
formula is

    M_plus(U,L)=M_minus(U,L)
       = [4 E_ij E^ij-3 B_ij B^ij] L^4/360 + O(L^5),

where equality denotes equality through the displayed order, not equality of
finite records. The tensors E and B are defined in CANDIDATE.md section 3.
The remainder is local for this fixed event/frame, uniform over its compact
preparation sphere. It is not uniform over unbounded observer boosts.

Ricci flatness at just one point is insufficient: its covariant derivatives
must also obey the neighborhood vacuum identities used below. A zero quartic
coefficient leaves the next order and the finite sign open.

## A. Why only fourth metric jets enter

Choose Lorentz orthonormal Riemann normal coordinates at o, with U fixed at the
origin. Under x=L y the rescaled metric g_L(y)=g(Ly) preserves all dimensionless
clock ratios. The protocol becomes preparation length one in g_L. Central and
receiver proper parameters both scale by L, so this scaling cancels in their
arrival derivative. It introduces neither a physical conformal change nor a
new comparison rule; it is the same small experiment in scaled units.

The scaled exponential, parallel transport, geodesic clocks and null boundary
problem have smooth dependence on L. The limiting null endpoint Jacobian is the
flat isomorphism described in CANDIDATE.md section 4. Solving the ODEs and
incidence recursively in L therefore uses only additions, products, integration
of finite parameter polynomials, and the inverse of this curvature-independent
flat Jacobian at each order. The logarithm is expanded at ratio one. No division
by curvature or eigenvalue, no curvature-selected frame and no nonpolynomial
function of a curvature invariant can enter a Taylor coefficient.

The normal metric expansion has schematic homogeneous terms

    g_L = eta + L^2 G2(R) + L^3 G3(nabla R)
                  + L^4[G4a(nabla^2 R)+G4b(R,R)] + O(L^5).

Consequently the averaged quartic coefficient is a universal polynomial
contraction linear in nabla^2 R and quadratic in R; the cubic coefficient is
linear in nabla R, and the quadratic coefficient is linear in R. These statements
follow from the recursive construction, not dimensional analysis alone.

Method source inspected: Leo Brewin, *Riemann Normal Coordinate expansions using
Cadabra*, arXiv:0903.2087v3, sections 2, 3.1–3.2, 5 and equation 11.1 (printed
page 15), https://arxiv.org/pdf/0903.2087v3. Its normal-metric expansion has exactly
the displayed jet types. The v3 correction history was inspected; no numerical
coefficient from its boundary-value formulas is used here. Its method concerns
smooth nondegenerate metrics in a normal neighborhood and is signature-algebraic;
those hypotheses hold here. No Einstein field equation is imported as UDT
dynamics. Vacuum remains a condition on this mathematical theorem.

The construction is covariant and introduces no orientation. In a normal frame
its angular coefficients are finite tensor contractions with g,U,n. Integrating
even products of n replaces them with symmetrized products of
h^{ab}=g^{ab}+U^a U^b; odd products integrate to zero. Thus every averaged term
is a scalar contraction using only g and U. No epsilon tensor occurs in the
underlying protocol. A parity-odd pseudoscalar is excluded even though one can
choose an oriented frame to define B.

## B. Derivative terms vanish in a vacuum neighborhood

Use ordinary Weyl slot convention C_abcd, antisymmetric in (a,b) and (c,d), with
pair exchange symmetry and vanishing traces. Ric=0 on the neighborhood implies
R=C and divergence zero in every Weyl slot, by contracted differential Bianchi.
Metric compatibility permits traces to commute with all the derivatives below.

Consider any complete scalar contraction of nabla_e nabla_f C_abcd using g and U.
Multiplicative contractions among extra U's only give constants, so each tensor
slot can be regarded as either paired with another slot by g or carrying one U.
This exhausts contractions after the angular moment substitution.

* If either antisymmetric Weyl pair has U in both slots, the term is zero.
* If any two Weyl slots are paired by g, a trace of C vanishes, including under
  both derivatives. This includes pairings inside an antisymmetric pair.
* Otherwise all four Weyl slots need external partners. At most two may carry
  U, one in each antisymmetric pair. The only other available slots are the
  two derivatives. Thus exactly two Weyl slots carry U, and each of the other
  two is paired with a derivative slot. In particular the innermost derivative
  f is contracted with a Weyl slot. Its Weyl divergence is identically zero
  on the neighborhood; the remaining outer derivative of that zero tensor is
  zero. There is no derivative commutation and no derivative of U in this
  argument: U is an external vector contracting the resulting tensor at o.

These cases exhaust every possible contraction. For nabla_e C_abcd the same
count is even simpler: avoiding a Weyl trace would require at least three
Weyl slots carrying U, so antisymmetry kills it. Linear C contractions likewise
vanish. This proves that the sphere's vacuum coefficients at orders two and
three vanish and that no independent nabla^2 C scalar remains at order four.

An alternative expression may commute covariant derivatives and display R^2
terms. That is not an omitted independent invariant; the proof above uses the
derivatives in their actual order and their identically vanishing divergence.

## C. The remaining quadratic space has dimension two

At fixed U, a four-dimensional algebraic vacuum curvature tensor is determined
by its electric and magnetic parts E and B. Both are spatial symmetric
trace-free rank-two tensors. This follows directly from the algebraic Weyl
symmetries and Bianchi: C_i0j0 determines E; C_ij0k determines B via the spatial
epsilon isomorphism on antisymmetric pairs; the spatial C_ijkl is then fixed
by E and tracefreeness. It is a linear algebra decomposition, not a field law.

Every invariant quadratic contraction is therefore a quadratic rotational
scalar made from two symmetric trace-free matrices. Contracting their four
spatial indices with Kronecker deltas leaves only tr(E^2), tr(B^2) and tr(EB);
separate traces vanish. Equivalent double-epsilon contractions reduce to these
by the epsilon-delta identity. Under a spatial reflection E is a true tensor
and B a pseudotensor. Hence tr(EB) is parity odd and cannot occur in the
orientation-independent sphere observable. Thus, separately for either first
emission,

    [L^4] M_plus = a_plus E^2+b_plus B^2,
    [L^4] M_minus = a_minus E^2+b_minus B^2,

with universal numerical constants. This is the classification that must hold
before control examples may determine constants; two examples alone could not
supply it.

## D. Exact determination of the universal coefficients

The unchanged two-control calculations in CANDIDATE.md are independent of this
classification attempt. In Kasner at the specified frame,
E=diag(-4/9,2/9,2/9), B=0, so E^2=8/27; both quartic means equal 4/1215.
Therefore a_plus=a_minus=1/90. In the plane-wave control E^2=B^2=1/2 and both
quartic means equal 1/720. Therefore b_plus=b_minus=-1/120. This determines the
formula stated above. These are exact coefficient equations in a proved
two-dimensional invariant space, not an empirical fit or selection of a profile.

The original-metric plane-wave tensor computation checks its electric/magnetic
norms, Ric=0 and nabla R=0. Kasner's B=0 and electric entries also follow directly
from the original diagonal time-dependent metric: R_ijk0=0 and
E_ii=r_i(1-r_i) at t=1. The saved formal series control checks both actual clock
incidences, not an inserted Weyl coefficient.

## E. What this would mean if review sustains it

Strictly negative 4E^2-3B^2 would give negative means for both independent first
emissions at sufficiently small L. Strictly positive gives positive means at
that local scope; equality is unresolved. Thus the proposed AMS condition in a
vacuum comparison regime has a nonautomatic candidate necessary inequality
4E^2>=3B^2 at each tested frame, but an actual Ricci-flat metric/frame realizing
the adverse sign remains to be supplied before claiming a physical GR control.
An arbitrary algebraic Weyl tensor is not yet that realized metric.

AMS, a native vacuum sector and any strengthened positivity/recovery clause are
still UNADOPTED. Even a realized adverse GR control would reject only that
conjunction, not UDT, an additional distant-onset contribution or all direct
clock laws. This candidate does not derive the founding positional assignment.

Fresh review should attack the finite-jet order, polynomiality, full angular
measure, orientation argument, exhaustive derivative contraction classes,
E/B completeness, exact-control coefficients and uniform remainder. Source-code
agreement alone does not establish these hypotheses.
