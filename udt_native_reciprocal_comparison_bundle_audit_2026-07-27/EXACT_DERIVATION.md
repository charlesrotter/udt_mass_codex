# Exact derivation — native reciprocal comparison bundle

## 1. Fixed-metric coframe freedom versus metric response

For a supplied Lorentz metric `g` with matrix `eta=diag(-1,+1,+1,+1)`, an infinitesimal coframe
endomorphism `X` changes the metric by

```text
R_g(X)=X^T eta+eta X.
```

The exact linear map `End(R^4) -> Sym^2(R^4*)` has rank ten and a six-dimensional kernel. The
kernel is exactly `so(1,3)`: infinitesimal fixed-metric Lorentz coframe changes. Every `X` splits
uniquely as

```text
X=A+Omega,
A=(X+X^dagger)/2,
Omega=(X-X^dagger)/2,
```

where `A` is metric-self-adjoint, `Omega` is metric-skew, and `R_g(X)=R_g(A)`. This is the exact
representative/physical-response separation that the prior seven-parameter chart lacked globally.

## 2. Coordinate-free seven-dimensional affine response fiber

At an ordered regular pair `(u,n)` with `g(u,u)=-1`, `g(n,n)=+1`, and `g(u,n)=0`, let

```text
B=span(u,n),  S=B^perp.
```

The founded generator acts as `-1` on `u` and `+1` on `n`. Its metric response fixes the three
components on `B x B`:

```text
r(u,u)=2,  r(u,n)=0,  r(n,n)=2.
```

A symmetric four-dimensional response has ten components. Fixing these three leaves the affine
fiber

```text
R_(u,n)={r in Sym^2(T*M): r|_(B x B)=2(u_flat^2+n_flat^2)|_(B x B)},
dim R_(u,n)=10-3=7.
```

In an adapted basis its general member is

```text
r = [[2,0,a,b],
     [0,2,c,d],
     [a,c,e,f],
     [b,d,f,h]].
```

The four cross components and three screen-symmetric components are exactly the metric responses
of the four mixing and three angular parameters in the registered triangular extension chart. The
restricted response map has exact rank seven. Thus none of those seven directions is an
infinitesimal Lorentz presentation artifact.

As `(u,n)` transforms, `B`, `S`, and `r` transform tensorially. Consequently these fibers form an
exact seven-dimensional affine **metric-response query bundle** over the ordered pair-frame bundle.
No global physical pair section is required for this query bundle to exist, and no physical pair
section is derived by its existence.

## 3. Stabilizer strata do not select a universal member

The connected stabilizer of an ordered pair is screen `SO(2)`. Requiring `r` to be invariant under
that stabilizer forces

```text
a=b=c=d=f=0,  e=h,
```

leaving one free screen-trace parameter. This is the coordinate-free `lambda` family; pair symmetry
alone does not select `lambda`.

If a global timelike observer line is supplied but no ruler is distinguished, spatial `SO(3)`
invariance uniquely forces `e=h=2`, the conditional `lambda=+1` response. If a global ruler is
supplied but no observer is distinguished, complementary `SO+(1,2)` invariance uniquely forces
`e=h=-2`, the conditional `lambda=-1` response. Full Lorentz invariance is inconsistent with the
fixed founded `-1/+1` pair. These are different supplied reductions and cannot be combined into a
universal selection.

## 4. Metric-canonical connection and path transport

A regular pseudo-Riemannian metric canonically determines its torsion-free metric-compatible
Levi-Civita connection as mathematics. That connection induces transport on the orthonormal frame
bundle, the ordered pair query bundle, and the affine response bundle. Under endpoint coframe
changes `L_p,L_q`,

```text
U_gamma -> L_q U_gamma L_p^-1,
X_p     -> L_p X_p L_p^-1.
```

Therefore

```text
X_q=U_gamma X_p U_gamma^-1
```

transforms covariantly, adjacent endpoint factors cancel, path composition is exact, and reversal
is inversion. Exact rational Lorentz controls verify each identity.

This is `METRIC_CANONICAL_MATHEMATICS`. Current UDT sources do not identify every physical
observer comparison with Levi-Civita parallel transport, choose a path family, or supply the
founded signed depth on those paths. The earlier conditional functor therefore remains conditional.

## 5. Holonomy and descent

The bundle survives nontrivial holonomy as a path-labelled object. Endpoint collapse of a chosen
generator or response requires the loop holonomy to stabilize it. Full `SO+(1,3)` holonomy cannot
stabilize the founded pair; the full commutant is scalar while the founded pair has unequal
`-1/+1` actions. Reduced `SO(2)`, `SO(3)`, or `SO+(1,2)` strata give the conditional families above,
but current UDT premises select none of those global reductions.

The reciprocal clock/ruler swap is not an ordinary Lorentz transition (`F^T eta F != eta`). It may
only enter as a separately supplied twisted transition and cannot be silently merged with
fixed-metric coframe equivalence.

## 6. The finite-lift obstruction

The affine response bundle is infinitesimal. It does not automatically integrate to one finite
constant-generator complete-coframe action.

Take the registered mixing control

```text
X = diag(-1,+1,0,0),  X_20=q,
```

and its unique metric-self-adjoint representative `A=(X+X^dagger)/2`. They have exactly the same
first metric jet:

```text
X^T eta+eta X=A^T eta+eta A.
```

But the second derivatives at `phi=0` of

```text
g_X(phi)=exp(phi X)^T eta exp(phi X)
```

and `g_A(phi)` differ by

```text
[[q^2,0,q,0],
 [0,  0,0,0],
 [q,  0,q^2,0],
 [0,  0,0,0]].
```

For nonzero mixing, equal infinitesimal physical response therefore does not determine the finite
complete-coframe continuation. The registered positive-triangular generator is one lift; the
self-adjoint representative is another. Selecting a finite lift requires an additional UDT-native
integration/reduction law.

## 7. Exact ruling

Derived:

- fixed-metric Lorentz coframe equivalence and its six-dimensional kernel;
- the seven-dimensional affine reciprocal metric-response query bundle;
- its tensorial transition law over regular ordered pair frames;
- metric-canonical induced connection and path-labelled transport for supplied paths; and
- the exact `SO(2)`, `SO(3)`, `SO+(1,2)`, and full-Lorentz stabilizer classification.

Still open:

- physical observer/ruler section and event pairing;
- physical path family and signed depth assignment;
- finite lift integrating the response into the complete `exp(phi X)` action;
- global reduced-holonomy/finite-cell section;
- physical comparison functor and variation domain; and
- action, source, carrier, boundary, bootstrap equation, `X_max`, mass, and dynamics.
