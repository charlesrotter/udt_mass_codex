# Step04 candidate — phase data constrain the local and global domains differently

CANDIDATE, UNPROMOTED; direct separate-context review pending.
IDs SC4-JET, SC4-LOCAL, SC4-COMPACT. No physical phase or recipe is selected.

## 1. Admitted objects and retained distinctions

Take an ACTUAL supplied smooth time-oriented Lorentzian metric and smooth
spacelike slice Sigma. If obtained through G321/G335, the metric development
inherits their conditional imported well-posedness theorem and bounded data
scope; we neither rerun a metric PDE nor assert an embedding of G356 waves
in the compact G321 family. The phase argument below itself only uses
smooth Lorentzian geometry, not an extra field equation.

G352's chosen continuous realization requires a dimensionless real phase
Theta with nonzero future-raised null gradient k=dTheta on its retained
domain. A phase is supplied query data, not automatically physical content.
Work locally first; global real phase coverage of a compact slice is an
OPTIONAL stronger domain request, not a G352 requirement.

## 2. SC4-JET: full initial covector compatibility

Let n be the future unit normal and gamma the induced positive spatial
metric. Supply smooth phi=Theta|Sigma. If a=n(Theta)|Sigma is also proposed,
nullness requires

    -a^2 + |dphi|_gamma^2 = 0.                          (1)

The raised covector is future nonzero precisely when a<0. Consequently

    dphi != 0,
    a = -|dphi|_gamma                                  (2)

are necessary and sufficient for a nonzero future-null INITIAL covector
whose tangential pullback is dphi. With dphi extended to annihilate n, it is

    k|Sigma = dphi + |dphi|_gamma n-flat.                (3)

Thus specifying the tangential initial phase does not leave its normal
derivative freely adjustable if the G352 type is retained. Conversely it
does not require a uniquely metric-selected phi. Formula (3) matches the
FULL ambient covector, not merely its tangential restriction. At dphi=0,
nullness forces a=0 and hence k=0; the nonzero phase domain excludes that
point. A different normal magnitude or the positive root fails the declared
type rather than generating another allowed normalization of fixed data.

## 3. SC4-LOCAL: a conditional local phase extension on the supplied metric

At any point of Sigma where dphi!=0 there is a neighborhood on which these
initial data determine one smooth local phase with nonzero future-null
gradient. Uniqueness is for the fixed phi and supplied metric on a common
sufficiently small neighborhood, not a selected phi or global history.

Choose a local Gaussian-normal presentation

    g=-dt^2+gamma_ij(t,x) dx^i dx^j, Sigma={t=0}.

This is a local coordinate choice, not a change to the metric equation or
a physical duration. Put

    F(t,x,p)=sqrt(gamma^ij(t,x) p_i p_j),  p!=0.

The negative-root eikonal equation is

    Theta_t + F(t,x,d_xTheta)=0, Theta(0,x)=phi(x).       (4)

F is smooth on this nonzero-covector domain, with positive-definite gamma.
It is positively homogeneous of degree1 in p. Use the time-dependent
characteristic equations, a standard mathematical method:

    dot x = F_p(t,x,p), dot p = -F_x(t,x,p),
    x(0,y)=y, p(0,y)=dphi(y).                            (5)

On a small precompact coordinate ball around the chosen initial point,
|dphi| has a positive lower bound. In a buffered neighborhood of its
initial phase-space image, gamma and its inverse remain smooth/positive
and p stays away from0. The vector field in (5) is smooth with bounded
first derivatives on a smaller compact neighborhood. For sufficiently
short |t|, its integral map preserves a closed neighborhood and is a
contraction when the interval length times a Lipschitz bound is less than1.
This gives unique local solutions. Smooth dependence on y follows by the
corresponding bounded variational ODE (and its higher derivatives).
Shrinking t and the initial ball preserves p!=0 throughout.

At t=0, D_y x=I. The inverse-function theorem therefore makes
(t,y)->(t,x(t,y)) a local diffeomorphism. For a small convex initial ball
with a buffer, continuity permits ||D_y x-I||<1/2 uniformly for short time;
the mean-value bound then also gives injectivity on that ball. This is only
a local tube, with no family-wide time or global no-caustic assertion.

Define the phase on that tube by

    Theta(t,x(t,y))=phi(y).                              (6)

It remains to check the FULL gradient, not just constancy on curves.
Let A=D_y x and P=D_y p. Euler homogeneity gives

    p.F_p=F, p^T F_pp=0, p.F_px=F_x.                    (7)

For each initial-label variation, differentiate p.A using (5):

    d_t(p.A)=-F_x.A + p.F_px.A + p.F_pp.P = 0.

Its initial value is dphi. Differentiating (6) in y therefore gives
(d_xTheta)A=dphi=p A; since A is invertible, d_xTheta=p. Differentiating
in t gives Theta_t=-p.F_p=-F. Thus (4) and (3) hold exactly. No field
equation or equation-of-state for carried content was inserted.

Any other smooth solution of the negative-root equation with the same
initial phi generates the same characteristic initial covectors and solves
the same ODE. ODE uniqueness and the local projection inverse make its phase
equal to (6) on their common local tube. This proves the claimed uniqueness.

The gradient is future because Theta_t=-F<0 and null by (4). Moreover its
raised field is affinely geodesic:

    k^a nabla_a k_b = k^a nabla_b k_a
                    = (1/2) nabla_b(g^-1(k,k)) = 0.     (8)

Here Hessian symmetry uses that k=dTheta and the connection is torsion-free;
metric compatibility gives the last equality. The t-parameterized curves
in (5) need not be affine: k#=F(partial_t+dot x^i partial_i), so an affine
parameter changes dt/dlambda accordingly. No normalization is silently lost.

The construction is conditional on the actual supplied metric, its smooth
local domain and the stated nonzero initial phase gradient. It determines
phase geometry from those data; it does NOT select a populated physical
phase. Initial phase origin and positive normalization remain supplied;
the G352 common phase/spacing gauge retains its existing scope.

## 4. Projection and smoothness boundary, not spacetime singularity

The local proof does not extend through a failure of the characteristic
projection inverse or loss of the retained smooth/nonzero domain. A
phase-space characteristic flow can remain smooth while multiple covectors
project to one spacetime event. That is not a singular metric or a proof
that a global single-valued phase exists after the projection fails.

A bounded check illustrating this limit uses Minkowski geometry and initial
phi(y)=-|y| on a patch away from y=0. For short t, the incoming characteristics
are x(t,y)=(1-t/|y|)y with p=-y/|y|, and

    Theta(t,x)=-|x|-t,    det D_y x=(1-t/|y|)^2.         (9)

The radial derivative eigenvalue is1 and both transverse eigenvalues are
1-t/|y|. At t=|y| the projection degenerates and the expression for Theta
is nonsmooth at x=0, although the spacetime is flat. This is a control of the
local-domain limitation, not another physically selected compatibility model
or a claim about generic caustic times. The formulas are used only before
the indicated crossing for the classical phase solution.

## 5. SC4-COMPACT: no everywhere nonzero global real phase on a compact slice

Suppose Theta is smooth and REAL-valued on a neighborhood of an entire
compact boundary-free spacelike slice Sigma, and its gradient is null and
nonzero everywhere on Sigma. Its restriction phi attains a maximum on Sigma.
At such a point dphi=0. Equation (1) forces a=0 and therefore dTheta=0,
contradicting the hypothesis. Thus that optional global domain is impossible.
No field equation, curvature recipe, dynamics approximation or numerical
sampling is used in this compactness argument. Compactness and real-valued
single-phase coverage are load-bearing; a boundary maximum would not imply
the same vanishing tangential derivative.

This applies to the entire compact marked spatial slices in the G321/G322
interface IF one requests that stronger globally real nonzero phase there.
It does not refute their metric developments, local G352 phase queries, or
G355/G356's local charts. It does not require discarding physical critical
points; it only limits where the specific nonzero phase query is defined.
Local patches remain possible by section3. A circle-valued phase or transition
atlas would be a differently typed construction requiring its own explicit
scope; neither is adopted or analyzed here. A new physical premise is not
inferred merely from failure of this optional global query.

## 6. What this does and does not say about a product or curvature recipe

Since phi is locally a submersion in section3, it can be part of initial
coordinates (theta,z1,z2). The characteristic map preserves theta by (6)
and can retain the supplied transverse labels z. This provides local query
coordinates for the existing G352 CHOSEN product. A supplied finite mu(z),
the same on phase slices and preserved on source-free labelled rays, remains
supplied phase-independent data under G351/G352. It is not selected by the
metric or by the eikonal argument, and no absence of phase-label correlation
is derived. Without that supplied product condition, conservation alone
does not create it.

In particular, propagating this free initial phase does not prove equality
to the G355/G356 CHOSEN curvature root/current at later events. Matching
initial data is weaker than maintaining a tensor identity throughout a
neighborhood; G356's fixed-label criterion must still hold wherever that
particular recipe/product is claimed. No compact G321 embedding of its
harmonic examples has been supplied. That recipe-persistence join remains
open, not silently closed by the local phase theorem or a new physical law.

## 7. Evidence and maximum conclusion

The local characteristic/variational proof and compact extremum argument
bear the quantifiers. Exact/symbolic controls check original null residuals,
future sign, full initial covector, homogeneous/variational identities and
the declared projection/critical-point controls. Finite checks do not prove
an ODE/PDE theorem or physical truth. The author developed this argument
before any reviewer finding, using no observations or fitted phase profile.

Maximum claim: conditional local geometric phase compatibility/propagation
from legitimate data, and a precise obstruction to OPTIONAL global real
coverage on compact slices. No uniform duration, global history, actual
instrument interface, physical content/count, recipe selection, source,
matter, scale, Xmax, accepted scientific grade or canon follows.

## 8. Pre-freeze execution history

The first symbolic execution failed after14 guards because Sympy structural
matrix equality distinguished (r0-t)/r0 from 1-t/r0. The frozen diagnostic
plan, original failed script, failed capture and actual diagnostic are retained.
Every entrywise difference was exactly zero. The only correction replaces
structural equality with exact symbolic zero testing; no mathematical formula,
domain, physical assumption or tolerance changed. This is an author pre-freeze
implementation repair, not an independent review or a post-review repair.

The corrected rerun passed18 symbolic/exact guard groups on Python3.10.12 /
Sympy1.13.1. Four actual mutant paths exited1 at their expected guards:
past_root/future-root; omit_spatial_force/variational identity;
wrong_characteristic_sign/phase transport; allow_zero/nonzero-domain.
All outputs, actual commands, durations, return codes and stderr are retained.
The torus and axis controls are finite examples; ODE existence, arbitrary local
smooth dependence, domain inversion and compact extrema remain analytic claims.
Candidate freeze occurs after this history and before reviewer findings.
