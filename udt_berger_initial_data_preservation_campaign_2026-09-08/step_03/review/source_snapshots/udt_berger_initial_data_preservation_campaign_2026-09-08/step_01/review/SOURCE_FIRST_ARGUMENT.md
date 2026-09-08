# BI1 independent source-first reconstruction

Pre-author reconstruction, 2026-09-08. Scope and independence disclosures are in
REVIEW_SCOPE.md. This argument uses only the declared sources and standard
differential geometry applied to their hypotheses. Its claims are conditional
mathematics in the G310/G312 owner-provisional arena, not new premises or canon.

## 1. Original data and every component

Fix a,c>0, a!=c, gamma=a^2(sigma1^2+sigma2^2)+c^2 sigma3^2. In the initial
orthonormal frame e1=X1/a,e2=X2/a,e3=X3/c put p=2/c, q=2c/a^2. Thus
[e1,e2]=q e3,[e2,e3]=p e1,[e3,e1]=p e2. Both p,q are strictly positive;
nonround means p!=q. The frame is held fixed under Gaussian identification
when taking the first normal derivative; it is orthonormal only initially.

Write all six arbitrary smooth real entries as

    K = [[x,u,v],[u,y,w],[v,w,z]],    tau=x+y+z.

No entry is initially discarded. The original G315 constraints are

    div(K-tau gamma)=0,
    R+tau^2-|K|^2=2 Lambda,

with constant Lambda. G330 gives

    lambda_h=pq-q^2/2, lambda_v=q^2/2,
    Delta=lambda_v-lambda_h=q(q-p), R=2pq-q^2/2.

The nonzero connection coefficients from Koszul are

    Gamma12^3=q/2, Gamma21^3=-q/2,
    Gamma13^2=-q/2, Gamma23^1=q/2,
    Gamma31^2=p-q/2, Gamma32^1=q/2-p.

Therefore the three full momentum expressions are

    M1=-e1(y+z)+e2(u)+e3(v)+(q-p)w,
    M2= e1(u)-e2(x+z)+e3(w)+(p-q)v,
    M3= e1(v)+e2(w)-e3(x+y).

The scalar constraint retains all six entries:

    xy+xz+yz-u^2-v^2-w^2 = E,       E:=Lambda-R/2.

At fixed gamma and fixed Lambda this is a restriction. When Lambda is to be
determined from general smooth K, the entire Hamiltonian expression must be
spatially constant; determining it independently at each point is not allowed.

## 2. Full first-normal operator for arbitrary smooth K

Let T_ij=dot(Ric3)_ij. Differentiate the Levi-Civita connection using
dot(gamma)=-2K. The tensor connection variation is

    dot(Gamma)^k_ij=-(D_i K_j^k+D_j K_i^k-D^k K_ij).

Using dot(Ric)_ij=D_k dot(Gamma)^k_ij-D_j dot(Gamma)^k_ik gives the uncommuted
G337 identity, independently recovering its sign and derivative ordering:

    T_ij=-D^k D_i K_kj-D^k D_j K_ki+D^k D_k K_ij+D_i D_j tau.

This is the complete smooth differential operator. The momentum equation does
not authorize commuting its first two derivatives without curvature terms.
For an explicit all-entry form, use e_i e_j f to mean e_i(e_j(f)). The two
mixed components, with ordered second derivatives, are

    T13 = 2p e1(u)-e1e2(w)+e1e3(y)
          -(p+q/2)e2(x)+(p-q/2)e2(y)+(3q/2)e2(z)
          +e2e2(v)-e2e3(u)-q e3(w)-(2pq+q^2)v,

    T23 = (-p+q/2)e1(x)+(p+q/2)e1(y)-(3q/2)e1(z)
          +e1e1(w)-e1e2(v)-e1e3(u)-2p e2(u)
          +e2e3(x)+2q e3(v)-(2pq+q^2)w.

The apparent asymmetry is the chosen ordering of noncommuting e_i e_j;
[e_i,e_j]f=C_ij^k e_k(f). The implementation checks tensor symmetry after
these commutators and retains all six functions, first derivatives and second
derivatives. The displayed invariant formula, rather than the expanded
components alone, fixes the operator unambiguously.

## 3. Raising an index, spectral image and projector

Set A=gamma^{-1}Ric3 and P the spectral projector onto the simple vertical
eigenvalue. Differentiate the inverse metric as well:

    dot(A)=gamma^{-1}T+2K^sharp A.

At the initial point A=diag(lambda_h,lambda_h,lambda_v). Differentiate P^2=P
and AP=PA. With Q=I-P, the diagonal blocks of dot(P) vanish and

    dot(P)^alpha_3=(T_alpha3+2lambda_v K_alpha3)/Delta,
    dot(P)^3_alpha=(T_alpha3+2lambda_h K_alpha3)/Delta, alpha=1,2.

This proof uses the isolated eigenvalue and works even when the two horizontal
eigenvalues split under perturbation. The base formula P=(A-lambda_h I)/Delta
must not be differentiated as though the horizontal eigenvalue stayed double.
Smoothness on compact S3 and its initially nonzero uniform gap justify the
first derivative of this projector for any smooth metric curve with the
specified initial velocity. A lawful development, if invoked, is conditional
on the imported Cauchy method; no development theorem is needed to compute it.

For a unit representative V=e3 the horizontal part of dot(V) equals
Q dot(P)V. Its vertical normalization component is z V; it is not line drift.
Changing V to -V changes its representative but not the criterion.

Thus the image line is stationary to first order in the declared normal
identification iff

    T13+q^2 v=0,       T23+q^2 w=0.

The full metric-orthogonal projector is constant to first order iff BOTH
off-diagonal blocks vanish, equivalently

    v=w=0 and T13=T23=0.

Their block difference is 2 K_alpha3, since Delta!=0. Image stationarity by
itself does not imply constancy of the metric-orthogonal complement/projector.
This algebraic distinction is not a claim that a prescribed pair of mixed
jets can always be extended to a globally constraint-compatible smooth K.

## 4. Exhaustive left-invariant constraint stratum

Now restrict x,y,z,u,v,w to constants in this frame. Tensor covariant
derivatives generally remain nonzero. Momentum is exactly

    ((q-p)w,(p-q)v,0).

Since p!=q it forces v=w=0, while u and x-y remain free. Differentiating
the complete left-invariant Koszul curvature for gamma(t)=I-2tK gives

    T13=-(2pq+q^2)v,    T23=-(2pq+q^2)w,
    dot(A)^alpha_3=-2pq K_alpha3,
    dot(A)^3_alpha=-2q^2 K_alpha3.

Because p,q>0, even before imposing momentum the homogeneous first-image
criterion is equivalent to v=w=0. The full-projector criterion is equivalent
there as well. Consequently every constraint-compatible homogeneous K has
zero first image AND projector drift; the first-normal test adds no further
restriction in this declared class. This does not extend to smooth arbitrary K.

For a full branch parametrization set s=x+y, d=(x-y)/2. The remaining scalar
constraint is

    sz+s^2/4-d^2-u^2=E.

All solutions, with no quotienting or hidden diagonalization, are exactly:

* s!=0: choose arbitrary real s,d,u, and put
  x=s/2+d, y=s/2-d, z=(E+d^2+u^2-s^2/4)/s.
* s=0: require d^2+u^2=-E and choose arbitrary real z, with x=d,y=-d.
  If E<0 this is a circle in (d,u) times the free z-line; if E=0 it is
  d=u=0 with arbitrary z; if E>0 this branch is empty.

Necessity follows directly from momentum and the original scalar equation;
sufficiency follows by substitution. The two exhaustive s cases establish the
homogeneous census analytically. Finite samples do not own this quantifier.

The trace/shear description displays both trace signs without imposing roots:
write the trace-free horizontal block as [[alpha,u],[u,beta]] and vertical
entry -alpha-beta. Then

    tau^2=3(E+alpha^2+alpha beta+beta^2+u^2).

Retain both +/- square roots when the right side is positive, its single zero
root when zero, and no real solution when negative. Complete K reversal
preserves both constraints at the SAME Lambda. No sign of shear is selected.
The s parametrization already contains all these branches and avoids artificial
root singularities. For instance tau=0 requires E<=0 and satisfies
3s^2/4+d^2+u^2=-E with z=-s; E=0 then forces K=0.

## 5. Sufficient recipes and concrete lawful controls

Pure trace is only the subcase x=y=z=h,u=0, with 3h^2=E. It need not exist at
a given fixed Lambda (E<0). G332 on this Berger metric covers the axisymmetric
subcase x=y=h,u=0,z=k through C=h+k,b=k-h. Its squared-root equation reduces to

    (b+C)^2=4k^2.

Both root signs and k=0 occur. At k=0 the homogeneous square root is a constant
zero and is smooth; the strict G332 existence recipe need not cover that edge.
Neither G332's axisymmetry nor pure trace is necessary in the full homogeneous
stratum. Horizontal block rotations can diagonalize its shear but cannot turn
a block with distinct eigenvalues into the axisymmetric recipe.

At a=1,c=3/2, R=7/2, the following exact K, and separately -K at the same
Lambda, satisfy all original constraints and have stationary first projector:

* Lambda=3: [[1,1,0],[1,0,0],[0,0,9/4]]. This has unequal horizontal eigenvalues
  and is outside the pure-trace and G332-axisymmetric subfamilies.
* Lambda=3/4: diag(1,-1,2), on the s=0 circle branch.
* Lambda=7/4: diag(0,0,-3), on the s=0 point branch.

The computational mixed v=1 hostile controls deliberately FAIL momentum;
they test formula omissions, not lawful-data departure or preservation.

## 6. Round control and conclusion ceiling

At a=c, p=q, all homogeneous momentum expressions vanish for arbitrary six
entries; only the scalar constraint remains. Ricci is scalar and no intrinsic
simple line/projector exists. Dividing by Delta or assigning a preferred
round Ricci line is invalid. This regular constraint control cannot be used as
a first-normal spectral-line theorem.

Zero first derivative alone does not prove actual time persistence. Nonzero
first derivative alone proves neither nonclosed leaves nor topology change,
physical/energetic instability or a particle interpretation. No such inference
is used. This review derives a full smooth first-jet criterion and a complete
homogeneous algebraic tile, not a smooth inhomogeneous census or a new registry
theorem. Every physical premise, imported theorem and source grade is inherited.

## 7. Exact evidence and limitations

source_first_check.py imports no author code/results. One method differentiates
the invariant Koszul connection and curvature at the fixed metric; another
constructs first and second covariant tensor derivatives and the uncommuted
operator. They share SymPy, the same independently reconstructed connection,
and this reviewer context, so this is method cross-checking, not an additional
independent reviewer. The author-implementation independence axis is assessed
only after seal and exposure. No different-model claim is made.

The saved run has 26 named exact checks passing and four nonzero hostile
discriminators. It used Python 3.10.12, SymPy 1.13.1, 0.724 seconds reported wall
time and 49,600 KiB child max RSS under the dispatch's 512 MiB/60-second limits.
All matrix entries are compared symbolically, not sampled approximately.
The smooth operator's full arbitrary-jet applicability is analytic; numerical
checks do not establish general smooth constraint solvability. No prior source
package, old carrier harness, full358 audit or candidate check was replayed.
No failed computational attempt occurred before this seal. Initial exploratory
formula construction preceded this mathematical candidate freeze, as disclosed.
