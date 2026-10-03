# ESR1 initial conditional candidate — scalar echo rigidity

UNREVIEWED at freeze. Mathematical discovery precedes this candidate. The parent
worked out the eigen-direction/Q-jet and boost-plane/polarization route before
receiving a brief concordant fidelity-review preview; that preview was received
before this written freeze. No peer proof, code or output was opened. This is
not a blind independent parent reconstruction. Reviewers' source-first work is
sealed separately, and this candidate still requires adversarial review.

## Statement with all quantifiers

Let (M,g) be a connected smooth time-oriented Lorentz4 region with ∇Riemann=0.
Use IEC1/PSW ordinary proper free clocks, parallel spacelike preparation, and
actual regular first/immediate future-return legs. For every event o, future
unit U, unit n⊥U, and all sufficiently small L>0, suppose one smooth Q defined
near1 obeys q(o,U,n,L)=Q(p(o,U,n,L)). The small interval may depend on the fixed
preparation; no uniform unbounded-boost radius is stipulated. This is the
explicit UNADOPTED physical trial FC, assumed here only as a mathematical
condition. Smooth may be weakened to C² for necessity.

Candidate conclusion: g has constant sectional curvature κ on the region.
Conversely every such local constant-curvature metric satisfies this preparation
rule with Q0(p)=p/(2−p²), wherever the short actual branches are regular.
This is a local geometric equivalence within the stipulated ∇R=0 class, not a
global topology/completeness classification. κ can be positive, negative or zero
and its magnitude is free. No Einstein equation or physical geometry is adopted.

If κ≠0, Q is forced to equal Q0 on the attained one-sided interval near1.
It need not equal Q0 on an unobserved side or farther outside that interval.
For κ=0, only Q(1)=1 is constrained. Do not describe the degenerate branch as
determining Q's derivatives. The result concerns net clock records, not an
unprovided subtraction or attribution to an additional positional component.

## 1. A nonflat tensor supplies a nonzero tidal eigenvalue

At o and future unit U, define E_U:n↦R(n,U)U on the positive-definite U⊥.
Curvature symmetries make E_U self-adjoint, so it has an orthonormal eigenbasis.
If R is nonzero somewhere, some E_U is nonzero. Indeed if all E_U vanish,
R(X,u,u,X)=0 for every timelike u and every X (extend from U⊥ by the U component
and scaling). For each X this is a polynomial identity in u on an open cone,
so it holds for all u. The polarization argument in section4 then gives R=0.
Thus a nonzero E_U has an eigen-direction n with eigenvalue T≠0.

Use IEC1's definitions T=g(R(n,U)U,n), V=R(n,U)U−Tn,
W=R(n,U)n−TU. In the chosen eigen-direction V=0. This choice exploits a
self-adjoint operator on Euclidean U⊥, not an unjustified diagonalization on
an indefinite vector space; nilpotent full Lorentzian curvature is not excluded.

## 2. That direction fixes the first two derivatives of any admissible Q

Let P=log p, Z=log q and H(P)=log Q(exp P). Continuity gives Q(1)=1,
so H is real and C² near0. The reviewed IEC1 expansion gives

    P=−T L²/2+O(L⁴),
    Z−H0(P)=d4 L⁴+O(L⁶),
    H0(P)=log[exp P/(2−exp(2P))]=3P+4P²+O(P³),
    d4=2|V|²+<V,W>.

In the chosen eigen-direction T≠0,V=0, hence d4=0. First divide
H(P)−H0(P)=O(L⁶) by L², then by L⁴ after removing the first-order term.
The nonzero limits P/L²=−T/2 and P²/L⁴=T²/4 give

    H'(0)=3, H''(0)=8,
    equivalently Q'(1)=3, Q''(1)=14.

No chosen constant-curvature comparison is used to prescribe these derivatives;
they follow from the supposed Q in an actual tidal eigen-direction. The argument
uses one-sided attained P values and the assumed C² germ, not analyticity.

## 3. Opposite physical directions force every tidal operator to be scalar

The same H applies to all preparations. Since H−H0=o(P²), and P=O(L²) in
each fixed preparation, Z=H(P) implies d4=0 in every direction, including
T=0 directions. If P starts at higher order or vanishes identically, the
remainder is still o(L⁴); there is no division by that direction's T.

Apply IEC1's physical n and−n identity at the same o,U:

    0=d4(n)+d4(−n)=4|V|².

The complement of span(U,n) is positive definite, so V=0 for every n. Therefore
every vector of U⊥ is an eigenvector of E_U. Linearity, applied to independent
vectors and their sum, forces E_U=λ(U)Id. This step needs both actual future
directions; it cannot be replaced by formal signed-L continuation or by one
restricted clock sheet. The flat case, for which step2 is unavailable, is kept
separate rather than excluded.

## 4. Scalar timelike Jacobi operators force a space-form tensor

Fix an event. Any two distinct future unit timelike U,U' span a Lorentzian
plane. Write U'=coshθ U+sinhθ n and n'=sinhθ U+coshθ n for unit n⊥U.
The determinant-one basis change preserves its sectional contraction:

    λ(U')=R(n',U',U',n')=R(n,U,U,n)=λ(U).

Thus λ is independent of U at that event. Put κ=−λ and define

    Rκ(X,Y)Z=κ[g(Y,Z)X−g(X,Z)Y].

This tensor has the same R(X,U)U as R for every unit timelike U and arbitrary
X (decompose X into U and U⊥). S=R−Rκ therefore obeys S(X,u,u,Z)=0 for all
timelike u, all X,Z. Polynomial continuation in u extends the identity to all u.
For completeness, even sectional vanishing S(X,u,u,X)=0 would suffice:
polarizing X gives S(X,Y,Y,Z)=0; polarizing Y gives

    S(X,Y,W,Z)=−S(X,W,Y,Z).

With the first Bianchi identity, the three cyclic terms in X,Y,W are then
equal, so 3S(X,Y,W,Z)=0. Consequently S=0. This proves the full tensor claim,
not just its Ricci contraction, and uses no external classification theorem.

Now R=κ(o)R1. Here κ is smooth (for example κ=Scal/12), ∇g=0 and ∇R=0.
Therefore dκ⊗R1=0, hence dκ=0. Connectedness makes κ constant on the region.
No extra field equation, matter assumption or global model identification enters.

## 5. Local sufficiency and the actual return

In a constant-curvature metric, the plane P=span(U,n) is a local totally
geodesic clock surface. One direct justification uses IEC1's normal metric
g_o(S_XY,S_XZ): the tangent isometry +Id on P and−Id on P⊥ preserves Rκ,
and therefore preserves that normal metric. Its local fixed surface exp_o(P)
is totally geodesic by uniqueness of geodesics fixed by an isometry. The
preparation, free clocks and unique short connecting null geodesics remain
there. This local construction needs no global space-form classification.

Define the real analytic functions Cκ,Sκ by Cκ(0)=1,Sκ(0)=0,
Cκ'=−κSκ,Sκ'=Cκ; Cκ²+κSκ²=1. Write c=Cκ(L). On the constant-curvature
clock surface an original quadric construction gives null incidence

    F(s,b)=c C_{−κ}(s)C_{−κ}(b)−κ S_{−κ}(s)S_{−κ}(b)−1=0.

This is the same conditional original-geometry incidence as the signed ECS/
FCW controls. It is not generated by Q. For κ≠0 and small positive L, first
reception has c C_{−κ}(b)=1 and b~L. Direct implicit differentiation gives
p=−F_s/F_b=1/c. Set h=S_{−κ}(b), z=κh²=1/c²−1.
The actual later return F(a,b)=0 becomes C_{−κ}(a)−κh S_{−κ}(a)=1.
Its nonzero future branch has

    C_{−κ}(a)=(1+z)/(1−z), S_{−κ}(a)=2h/(1−z).

This is a~2L, not the inverse/past outgoing branch. Differentiating at(a,b),

    q=−F_b/F_s=1/[c(1−z)]=c/(2c²−1)=p/(2−p²).

The identity is regular for all sufficiently small positive L; we claim no
global echo domain beyond the local normal tube. At κ=0 use original flat
incidence (b−s)²−L²=0 and its future return, giving b=L,a=2L,p=q=1.
The κ=0 calculation is separate because the displayed unscaled F vanishes
identically when κ=0. It is not legitimate to divide by κ there.

For κ>0, Cκ(L)=cos(sqrtκ L), hence attained p>1 near1. For κ<0,
Cκ(L)=cosh(sqrt(−κ)L), hence p<1. As L varies these cover a one-sided
interval; Q must equal Q0 on that interval. A smooth flat-at1 modification
supported on the unused side preserves every attained record, so a two-sided
uniqueness claim for smooth Q would be false. No global continuation follows.

## Interpretation and pending gates

If reviewed, this closes the all-frame scalar-selectivity question within the
declared locally symmetric class. Its selectivity is strong: it removes the
anisotropic curvature structures that survive a single aligned clock sheet.
The theorem does not show that the founding positional interpretation or ULC1
implies FC. It fixes neither κ's sign/magnitude nor X_max, topology, boundary,
physical response or additional-effect attribution. The result concerns total
geometry in this class. It is not PCC1's curvature-difference condition, and
does not extend to generic ∇R≠0 gravity or certify an empirical SR/GR filter.

Parent short exact/actual-incidence checks and two fresh source-first/exposed
reviews remain to be completed. Universal necessity is the argument above;
finite controls cannot replace it. The original candidate stays fixed through
any source-preserving repair. No scientific adoption or successor is authorized
by a conditional theorem alone.
