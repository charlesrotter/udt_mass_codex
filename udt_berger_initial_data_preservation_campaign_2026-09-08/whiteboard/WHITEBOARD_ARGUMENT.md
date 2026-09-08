# Berger left-invariant constraint census and branch preservation — whiteboard

Status: UNREVIEWED CONDITIONAL CANDIDATE / WHITEBOARD ONLY. No promotion, physical
adoption, canon change, or general stability assertion.

## Provenance, exposure, and scope

This argument was constructed in delegated context `/root/berger_whiteboard` on
2026-09-08 at inspected `grok` HEAD
`8593f11cd96a575be3513d1ec56e92ac4f5811ff`. The parent reported synchronization;
this context independently inspected branch, HEAD, and dirt, but did not repeat
synchronization or the full premise verifier. Unrelated and protected untracked
payloads were left untouched and unread. The parent owns the full premise audit.

The actual model identity was not independently measured; record it UNKNOWN.
This context was exposed from dispatch to the target question and requested
preservation assessment. It read the current premises, AGENTS.md, required
CLAUDE.md sections, the triggered no-shortcuts, completeness-map, and
solution-space-not-imposition protocols, and these two scientific sources:

- `udt_g330_berger_hopf_eigenline_local_persistence_2026-09-02/EXACT_DERIVATION.md`
- `udt_g332_weighted_contact_vacuum_constraint_embedding_2026-09-03/EXACT_DERIVATION.md`

It did not inspect protected work, historical Hopfion payloads, source campaign
implementations, or a proposed new candidate from the parent. Findings were sent
to the parent during construction. The parent subsequently reported agreement
with its own pencil derivation. This is collaborative discovery, NOT independent
adversarial review, different-model review, or formal proof verification.

The question is exhaustive only over LEFT-INVARIANT smooth symmetric K on ONE
supplied nonround Berger metric, at a supplied real constant Lambda. The domain
is compact S3 identified with SU(2), with positive a,c and a != c. The six real
constant components of K start free-and-explored. The metric, topology,
left-invariance restriction, and Lambda are supplied by the work order, not
selected physical data. The admitted original constraints come from G332;
G330 supplies the frame normalization and the explicitly conditional imported
Einstein-Cauchy existence/uniqueness method. No field, action, source, boundary,
physical scale, population, or physical premise is added.

Only three small read-only exact SymPy calculations were run; no numerical
approximation, GPU, PDE solve, fitted ansatz, or finite-search conclusion enters.
Their exact source and captured outputs are in CHECK_TRANSCRIPT.md. At the
parent's stop instruction, exploration ended. Saving this record is the only
file mutation by this context.

## 1. Complete constraint calculation

Use G330's orthonormal left-invariant frame

    e1 = X1/a, e2 = X2/a, e3 = X3/c,
    [e1,e2] = q e3, [e2,e3] = p e1, [e3,e1] = p e2,
    p = 2/c, q = 2c/a^2.

Write every left-invariant symmetric covariant K in that frame as

    K = [[u,z,r], [z,v,t], [r,t,w]].

The trace is constant. Koszul gives Gamma(j,j,l)=0 in this frame. Therefore the
original lower-index momentum constraint, equivalently the lowered version of
G332's upper-index divergence, is

    M_i = sum_j (D_j K)_ij
        = -sum_j,l Gamma(j,i,l) K_lj
        = ((q-p)t, (p-q)r, 0).

For a != c, p != q, so momentum holds if and only if r=t=0. There is NO
constraint here forcing z=0, u=v, or pure trace. Equivalently, K preserves the
initial horizontal plane and vertical Ricci line, or commutes with the initial
Ricci endomorphism. This equivalence is specific to this nonround homogeneous
stratum.

Let

    R = 8/a^2 - 2c^2/a^4,
    D = Lambda - R/2.

The original Hamiltonian constraint is

    R + tau^2 - |K|^2 = 2 Lambda.

Before imposing momentum its quadratic part is exactly

    tau^2 - |K|^2 = 2(uv+uw+vw-z^2-r^2-t^2).

After momentum the necessary and sufficient remaining equation is

    det(B) + w tr(B) = D,
    B = [[u,z],[z,v]].

Set m=(u+v)/2 and d=(u-v)/2. Then

    m^2 + 2mw - d^2 - z^2 = D.

The complete classification, with no division or lost exceptional stratum, is

    K = [[C-w+d,z,0], [z,C-w-d,0], [0,0,w]],
    C^2 - w^2 - d^2 - z^2 = D,
    (C,w,d,z) real.

Necessity follows from the preceding direct original-constraint calculation;
sufficiency follows by substitution. This is an exact algebraic classification
of the declared finite-dimensional class, not an inference from sampled checks.
The solution set is a Lorentz quadratic level set: two sheets for D>0, a double
null cone including its vertex for D=0, and one sheet for D<0. The only singular
point of a level set is the zero tensor on D=0.

For comparison, solving by division gives

    m != 0: w = (D-m^2+d^2+z^2)/(2m);
    m = 0: D = -(d^2+z^2) <= 0, with w arbitrary.

The latter branch must not be omitted. In particular, D=0, m=d=z=0 admits
arbitrary vertical rank-one K. For every real D there are solutions: choose any
nonzero m, take d=z=0, and use the displayed w.

## 2. Relation to the earlier supplied subfamilies

Pure trace is the subfamily d=z=0 and w=m=h. Its condition is D=3h^2,
equivalently R+6h^2=2 Lambda, with both signs retained when real.

The G332 unit-Killing form on this Berger metric has horizontal eigenvalue
m=(C-b)/2 and vertical eigenvalue w=(C+b)/2. Thus C=m+w, b=w-m, and its
horizontal-isotropic subfamily is precisely d=z=0 in the classification.
G332's strict radicand condition on this constant-R metric is C^2>D, or w!=0;
the full algebraic census also retains the w=0 crossing cases whenever allowed.
This comparison concerns that ansatz applied to the Berger metric; it does not
identify arbitrary weighted metrics with the fixed Berger geometry.

Horizontal anisotropy is lawful. At the supplied G330 witness a=1, c=3/2,
Lambda=3, one has R=7/2 and D=5/4. The exact datum

    K = diag(1,2,-1/4)

has zero momentum and zero original Hamiltonian residual. Its unequal
horizontal entries break the initial continuous right-U(1) invariance of the
FULL initial pair. Consequently it defeats any assertion that every lawful
left-invariant K keeps the evolving metric in the two-function Berger family.
In Gaussian gauge, the initial metric derivative is plus or minus 2K depending
on the fixed extrinsic-curvature convention; unequal horizontal entries split
the two equal horizontal metric coefficients for either convention.

## 3. Conditional preservation beyond continuous axial symmetry

The following argument uses exactly the smooth marked Einstein-Cauchy
existence/uniqueness and isometry-extension method admitted conditionally in
G330. This document does not independently prove that imported theorem.

1. An SO(2) rotation of the initial horizontal invariant frame diagonalizes the
   real symmetric B. The Berger metric is unchanged by that rotation, and X3
   is fixed. This is an initial metric isometry/frame choice, not an additional
   restriction on K.
2. In that fixed rotated invariant frame, BOTH initial tensors are diagonal.
   They are invariant under left SU(2) translations and under the three group
   automorphisms whose differentials are

       diag(1,-1,-1), diag(-1,1,-1), diag(-1,-1,1).

   These rotations are Lie algebra automorphisms for the normalized SU(2)
   bracket and integrate to automorphisms of SU(2).
3. Conditional isometry extension carries those initial-data symmetries to the
   marked local development. A common Gaussian neighborhood can be used near
   the compact initial slice. The normal geodesic identification respects the
   extended isometries.
4. Left invariance makes each spatial metric's coefficients spatially
   constant. Invariance under the three fixed sign-flip automorphisms forces
   every off-diagonal coefficient to vanish. Therefore

       gamma(t) = x(t) sigma1'^2 + y(t) sigma2'^2 + zeta(t) sigma3^2,
       x,y,zeta > 0,

   with x(0)=y(0)=a^2 and zeta(0)=c^2. This is in general a three-function
   diagonal homogeneous metric, not a Berger metric.
5. Ricci is invariant under the same isometries and hence diagonal in the same
   fixed invariant axes. In particular, the ORIGINAL line span(X3) is an exact
   Ricci eigenline on every such local slice.

This proves the conditional symmetry-preservation assertion for EVERY datum in
the complete left-invariant constraint census. It requires discrete preserved
symmetry; it does not require a continuously axial initial pair or a Killing
field X3 on later triaxial slices.

## 4. Actual spectral gaps and the retained Hopf branch

Write x1=x, x2=y, x3=zeta and all three positive. A direct Koszul calculation
for the diagonal invariant metric gives the orthonormal Ricci eigenvalues

    r_i = 2[x_i^2-(x_j-x_k)^2]/(x y zeta).

Therefore

    r3-r1 = 4(zeta-x)(zeta+x-y)/(x y zeta),
    r3-r2 = 4(zeta-y)(zeta+y-x)/(x y zeta).

The vertical eigenvalue is simple if and only if BOTH displayed products are
nonzero. It is insufficient to require only zeta!=x,y: a coincidence also
occurs at zeta+x=y or zeta+y=x. At the initial Berger slice both gaps equal
4(c^2-a^2)/a^4, so positivity and continuity give a common nonzero local
interval for every supplied datum. No uniform lifetime over unbounded K is
claimed.

On the gap-open interval the spectral projector onto the continued vertical
branch can be written

    P3 = (Ric-r1 I)(Ric-r2 I)/[(r3-r1)(r3-r2)].

This expression also works when r1=r2. It is a tensorial projector, not a raw
coordinate component. Its image is the original line span(X3).

A generic triaxial slice may have THREE simple Ricci eigenlines. Consequently,
this result preserves the original marked branch by smooth continuation; it
does not preserve the property that there is exactly one simple Ricci line.
The original branch remains the largest eigenvalue when c>a, or the smallest
when c<a, until one of its gaps closes. Selecting which ordered branch is the
continued original one retains information about the supplied initial stratum.

The X3 integral curves are the same closed subgroup orbits on SU(2), independent
of the time-dependent positive diagonal coefficients. They remain the original
Hopf circles even when X3 is no longer Killing. Their metric length is
2 pi sqrt(zeta). With V=+/-X3/sqrt(zeta),

    alpha = gamma(V,.) = +/-sqrt(zeta) sigma3,
    eta = (2 pi / fibre_length) alpha = +/-sigma3.

The smooth circle quotient and the period-normalized form therefore remain
exact. Using G330's orientation and integral convention,

    (1/(4 pi^2)) integral eta wedge d eta = -1,

with absolute value one. No later Killing assumption is needed for this
calculation. At a vertical eigengap closure the fixed subgroup line can still
exist in this presentation, but its extraction as this simple Ricci branch
fails; no continuation-through-degeneracy theorem is asserted.

## 5. Discovery history, boundaries, and return

Initial calculation retained all six constant components and found that
momentum kills only the two vertical-horizontal entries. Hamiltonian was first
written with division by m; the m=0 cases were then made explicit and the
Lorentz-quadric parametrization removed that division entirely. A lawful
horizontal-anisotropic example showed why continuous Berger symmetry is too
strong a general conclusion. The fixed diagonal discrete symmetry supplied
the wider preservation argument. The triaxial curvature calculation exposed
the additional Ricci-degeneracy surfaces. Finally, the claim was narrowed to
continuation of the original branch because triaxial metrics need not have
exactly one simple eigenline. These are exploratory observations and revisions,
not a preregistered confirmation experiment or a claim of adversarial repair.

At a=c the momentum coefficients above vanish and no vertical branch is
intrinsically singled out by the round spatial Ricci tensor; the nonround
classification argument must not be extended through that boundary by division.
No classification of spatially varying K on a fixed Berger metric is supplied.
No generic nonsymmetric metric or K perturbation, weighted-family evolution,
global time interval, nonlinear stability, physical persistence mechanism,
particle, energy, mass, selected size, topology selection, or UDT-wide
Hopf-orbit rigidity follows. This homogeneous result does not overrule G332's
lawful irregular-orbit initial examples on other supplied spatial metrics.

Return: a complete mathematical constraint census in the declared
left-invariant fixed-nonround-Berger stratum, with an unreviewed conditional
local preservation argument for the original gap-open Hopf Ricci branch.
