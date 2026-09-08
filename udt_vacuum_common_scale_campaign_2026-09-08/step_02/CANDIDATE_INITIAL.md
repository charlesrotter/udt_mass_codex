# VS2 initial conditional candidate: the four-dimensional local boundary

Explored then frozen for fresh review; NOT_BANKED. No literature-novelty,
physical identification or selected-universe claim. The argument applies
known differential geometry to the admitted bounded UDT vacuum arena.

## Inputs and precise claim

Use exactly reviewed VS1, including its premise stamps, curvature convention,
source scope and limitations. Let B be a connected contractible sufficiently
small chart of a supplied smooth four-dimensional Lorentzian metric g with
Ric(g)=Lambda g. Lambda is constant; k=Lambda/3. No analyticity, genericity,
symmetry, non-null gradient or completeness is assumed. Define V(B) as the
REAL LINEAR space of smooth real u satisfying

    Hess(u)=(c-ku)g, with c a constant depending on u.                 (1)

It is the positive functions u in this space that give the actual second
vacuum metric g_hat=u^-2 g. Positivity may require a smaller neighborhood.
The dimension claims concern V(B), or local germs with these hypotheses,
not a vector space of positive factors or physical moduli. Fixed target
Lambda_hat is an extra query restriction, considered separately below.

The proposed exact local trichotomy is:

| Supplied base sector | V(B) | Dimension |
|---|---|---|
| W identically zero on B (constant sectional curvature k) | All solutions of the flat VS1 rank-six connection | 6 |
| W not identically zero; Lambda=0; a nonzero parallel null one-form dv exists on B | u=a+bv | 2 |
| All other Einstein bases with W not identically zero on B | Constants u=a | 1 |

The second row uses local exactness on the stated contractible B. It does
not assert that every Ricci-flat base has such a one-form. The third row
includes nonzero Lambda with nonzero Weyl curvature and Ricci-flat bases
without parallel null one-forms. Constant-curvature metrics with k nonzero
are not called flat metrics; it is the prolonged connection that is flat.

## Algebraic lemma that makes dimension four consequential

At a point of a four-dimensional nondegenerate metric space, suppose an
algebraic Weyl tensor W annihilates a NON-NULL vector V in one slot. By its
pair symmetries it annihilates V in every slot. The orthogonal complement
E=V-perp is a nondegenerate three-dimensional space. W is then supported
entirely on E. Its Ricci contraction on E vanishes, because the full trace
vanishes and all components involving V vanish. In three dimensions an
algebraic curvature tensor is determined by its Ricci contraction: the
metric-wedge-Ricci formula with the scalar term reconstructs it (valid in
either signature). Thus W=0. Consequently, where W is nonzero, every
nonzero vector annihilated by W must be null. This is not a statement that
the Weyl tensor, viewed as a bivector map, must be invertible.

The Lorentzian qualification is also consequential: a totally null vector
subspace has dimension at most one. The proof below uses this only for the
number of parallel one-forms, not to discard a nonzero null gradient.

## Necessity on a non-conformally-flat neighborhood

Write mu=du and f=c-ku. VS1 gives throughout B

    nabla(mu)=f g,       df=-k mu,       W(...,mu-sharp)=0.           (2)

Assume W is nonzero at some point p and u is not constant on B. First,
mu_p cannot be zero. If it were zero, differentiate the last equation in
(2) at p. The derivative of W times mu vanishes, while nabla(mu-sharp)
is f times the identity, giving f_p W_p=0. Hence f_p=0, and the six
initial data (u_p,mu_p,c) coincide with those of the constant solution
u=u_p (since c=k*u_p). The VS1 path-ODE uniqueness on connected B would
make u constant everywhere, a contradiction.

Therefore mu_p is nonzero. In an open neighborhood of p both W and mu
stay nonzero, and the algebraic lemma makes q=|mu|^2 zero there. Taking
its differential gives 0=dq=2f mu, so f=0 there. Then df=-k mu forces
k=0. Since k=Lambda/3 is constant on B, Lambda=0 globally on this
connected comparison domain. Since c=f+ku is also constant, c=0.
Equation (2) now gives nabla(mu)=0 everywhere on B. Parallel transport
preserves its nonzero character and its zero norm: mu is a nonzero
parallel null one-form throughout B.

This argument does not require W to be nonzero everywhere, does not divide
by q, and does not discard zeros of curvature. It establishes a necessary
condition for a nonconstant scale profile on any B with W not identically
zero, rather than merely a condition on a symmetry-restricted example.

## Sufficiency, dimension and actual realization

If Ric(g)=0 and a nonzero parallel null one-form alpha exists, it is closed
by torsion-freeness and is alpha=dv on contractible B. For every constants
a,b, u=a+bv satisfies Hess(u)=0, c=0, hence (1). Choosing u(p)>0 and
shrinking produces actual smooth positive conformal vacuum metrics. This
is sufficiency on a supplied metric, not a formal curvature-jet realization.

On a nonflat Ricci-flat B, there cannot be two independent parallel
one-forms. Any non-null parallel one-form would annihilate the curvature
and, since Ric=0, the Weyl tensor, contradicting the algebraic lemma at a
point where W is nonzero. If two parallel one-forms were independent,
their values would be independent at every point by parallel uniqueness;
all their real linear combinations would likewise be parallel and hence
null. Their span would be a two-dimensional totally null space, impossible
in Lorentz signature. Thus there is at most one parallel one-form direction,
with proportionality by a constant. By the necessity result every derivative
of a solution of (1) lies in that direction, so all u=a+bv. Constants and
v are independent, proving dimension exactly two. If no such direction
exists, only constants survive, proving dimension one.

If W identically vanishes instead, the VS1 connection has zero curvature.
On a contractible sufficiently small neighborhood, smooth linear parallel
transport for a flat connection is path-independent: the transport variation
across a path homotopy is the curvature integral, which vanishes. Therefore
every six-component initial datum yields an actual smooth parallel section.
Projection to u is injective by VS1; there are exactly six real independent
solutions. Positive u_p again gives a positive solution after shrinking.
This establishes local existence, not global positivity on a prescribed
complete manifold. The k=0 polynomial family in VS1 is an explicit sharp
control, not the only constant-curvature case covered by this argument.

## Scalar conditions and what is freely supplied

The VS1 first integral Q=|du|^2+ku^2-2cu fixes Lambda_hat=-3Q.
In the genuinely curved two-dimensional sector, k=c=|du|^2=0, so EVERY
admissible factor gives Lambda_hat=0. In the one-dimensional sector,
u=a>0 gives Lambda_hat=a^2 Lambda. In the six-dimensional sector,
an independently specified Lambda_hat restricts the six data by this
quadratic equation; no claim of six free data after that restriction.

The base geometry, its initial/boundary data within its admitted class,
and identified query embeddings remain supplied. The vacuum equation
constrains comparison profiles; it does not select those legitimate inputs.
No law choosing a,b, six initial numbers, a parallel direction, geometry or
physical content has been added. Conformal relatedness is a stated comparison
question, not a claim that all admitted metrics are conformally related.

## Actual developments and a pointwise false pass to check

These are diagnostic metric choices, not physical recipes or new premises.

1. On coordinates (r,v,x,y), the Lorentzian metric

       g=2 dr dv+dx^2+dy^2+r(x^2-y^2) dr^2                      (3)

   has Ric(g)=0, parallel null dr and R_rxrx=-r. On a small positive
   domain u=1+r gives another Ricci-flat metric. This realizes the second
   row with genuine curvature arbitrarily close to r=0, not only a flat
   example or a formal jet.
2. At the origin of (3), W_p=0 and Gamma_p=0. Thus the single-point
   Weyl annihilation check accepts every covector, including mu_p=dx
   with u_p=1. But partial_r W_rxrx=-1 there. Differentiating the required
   W(...,mu-sharp)=0 would give -1=0, independently of c because W_p=0.
   Hence these pointwise-passing data have NO neighborhood extension.
   The trial u=1+x provides an additional direct residual check, but the
   differentiated compatibility obstruction excludes every extension with
   those initial data, not merely that particular trial function.
3. The local product metric

       g=-dt^2+cosh(t)^2 dx^2+dtheta^2+sin(theta)^2 dphi^2        (4)

   for 0<theta<pi has Ric(g)=g and W_tx tx nonzero. It is a genuine
   Einstein development in the constant-only sector. The general proof,
   not this single example, establishes the nonzero-Lambda/nonzero-Weyl
   exclusion. No product symmetry is imposed on the theorem's base class.

Exact algebraic and original coordinate-Ricci checks will corroborate signs,
the exceptional null sector and the pointwise false pass. They do not prove
the universal trichotomy, and a finite example does not establish genericity.

## UDT consequence and limits

Under the inherited owner-provisional admitted vacuum premises, common-scale
freedom invisible to the REDUCED G131 control is constrained by the response
equation. It is not arbitrary profile freedom once g is fixed. This sharpens
VS1 by showing why nontrivial scale variation is exceptional in a precise
structural sense, WITHOUT a measure/topology-based genericity claim: outside
constant curvature it requires Ricci-flatness and a parallel null covector.
G176/G180 completed tape/depth remain scale-sensitive as in VS1; no new
readout/instrument/particle identification follows. This is a connection
between admitted structures, not replacement by another chosen recipe.

No whole-metric uniqueness, source law, carried-content identification,
global completeness, stability, smooth Cauchy well-posedness, calibration,
observational distinction, new premise, accepted grade or canon is claimed.
All-loop VS1 compatibility remains the general formulation; VS2 supplies a
four-dimensional local sector characterization, not a finite curvature-jet
algorithm for recognizing a parallel null one-form in arbitrary input data.
