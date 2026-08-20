# G184 exact derivation — regular branch equivalence

Date: 2026-08-19

## 1. Typed realization groupoid

Fix a supplied smooth Lorentzian four-manifold `(M,g)` and a fully typed ordered observer-pair query
`Q`. A regular realization is

```text
R=(Sigma,q,F),
F:Sigma -> M,
h=F^*g,
h00<0, det(h)<0,
```

where `q` contains the query structures that are actually declared: source and target incidence,
marked boundaries, clock/ruler calibration, ordering, and orientations.

Define a strict arrow `psi:R_1 -> R_2` to be a diffeomorphism

```text
psi:Sigma_1 -> Sigma_2
```

such that

```text
q_1=psi^*q_2,
F_1=F_2 o psi.
```

Identity maps are arrows. If `psi` is an arrow, `psi^-1` preserves the inverse typing and makes the
inverse diagram commute. If `psi_12:R_1->R_2` and `psi_23:R_2->R_3`, then

```text
F_1=F_2 o psi_12=F_3 o psi_23 o psi_12.
```

Thus these objects and arrows form a groupoid. It is generally an infinite-dimensional groupoid of
maps and is not claimed to be a finite-dimensional Lie action groupoid.

If the query separately supplies a group `Aut_g(Q)` of ambient isometries preserving all of its
typing, an extended arrow is a pair `(psi,A)` satisfying

```text
A^*g=g,
A o F_1=F_2 o psi.
```

Composition is

```text
(psi_23,A_23) o (psi_12,A_12)
=(psi_23 o psi_12, A_23 o A_12).
```

The same diagram proves closure and inversion. The strict quotient and this query-symmetry quotient
are different mathematical questions. No reflection, screen flip, or observer swap enters unless it
is in the supplied query automorphism group.

## 2. The completed kernel descends

For a strict arrow,

\[
h_1=F_1^*g=(F_2\circ\psi)^*g=\psi^*h_2.
\]

For an extended arrow,

\[
\psi^*h_2=(F_2\circ\psi)^*g=(A\circ F_1)^*g=F_1^*(A^*g)=h_1.
\]

Thus the pair metric descends in both cases.

The invariant statement carries the declared clock vector and ruler orientation with `q`. In a
clock-preserving calibrated chart with

```text
psi(t,u)=(t,f(u)),  f'(u)>0,
```

the explicit transformation is

\[
h_{00}\mapsto h_{00},\qquad
h_{01}\mapsto f'h_{01},\qquad
h_{11}\mapsto (f')^2h_{11}.
\]

Therefore

\[
\det h\mapsto(f')^2\det h,
\qquad
\widetilde m=f'm,
\qquad
\widetilde m\,du=\psi^*(m\,d\sigma).
\]

The completed depth

\[
\Phi=-\frac12\log(-h_{00})
\]

is unchanged after pullback in the carried clock calibration. For `f'<0`, the positive density uses
`|f'|` while the oriented ruler one-form changes sign, exactly as classified in G180. Hence the
accepted completed kernel is well defined on realization-isomorphism classes.

For the fixed nonlinear control

\[
f(u)=\frac{u+u^2}{2},\qquad f'(u)=\frac{1+2u}{2}>0,
\]

the realization

\[
F(t,s)=(t,s,s^2,0)
\]

has spatial metric coefficient `1+4s^2`. The reparameterized coefficient is exactly

\[
(f')^2(1+4f^2)=(f')^2+(2ff')^2,
\]

which is the direct pullback from `F(t,f(u))`. Both marked ends are fixed.

## 3. The evaluator hierarchy is not reversible

Typed realization isomorphism implies pair-metric equivalence, which implies equality of completed
scalar outputs after pullback. The converses fail. Endpoint, scalar, tape, pair metric, and image set
are progressively incomplete summaries of the full map `F`.

This is a statement about separation of **objects up to isomorphism**. It is not the categorical
claim that an evaluation functor fails injectivity on every morphism set; the terminology correction
is frozen separately.

## 4. Same endpoints and metric, inequivalent immersion

In flat `1+3`, let `0<=s<=pi R` and define

\[
c_1(s)=\left(R\sin\frac{s}{R},\ R\left(1-\cos\frac{s}{R}\right),\ 0\right),
\]

\[
c_2(s)=\left(a\sin\frac{2s}{R},\ \frac{2s}{\pi},\
a\left(1-\cos\frac{2s}{R}\right)\right),
\qquad
a=\frac R2\sqrt{1-\frac4{\pi^2}}.
\]

Both join `(0,0,0)` to `(0,2R,0)`. Their speeds satisfy

\[
|c_1'|^2=1,
\]

and

\[
|c_2'|^2=\frac{4a^2}{R^2}+\frac4{\pi^2}
=1-\frac4{\pi^2}+\frac4{\pi^2}=1.
\]

Therefore the two product immersions `F_i(t,s)=(t,c_i(s))` have exactly the same marked endpoints
and pair metric

\[
h_1=h_2=-dt^2+ds^2.
\]

For a unit-speed curve product, the squared norm of the spatial second fundamental form is
`|c_i''|^2`. Here

\[
|c_1''|^2=\frac1{R^2},
\qquad
|c_2''|^2=\frac4{R^2}\left(1-\frac4{\pi^2}\right).
\]

Equality would require `pi^2=16/3`, impossible already from `pi>3`. Second-fundamental-form norms
are preserved by domain and ambient isometries. The two realizations therefore cannot be related by
a query-preserving reparameterization or an ambient isometry, despite identical endpoints, `h`,
completed tape, shift, and `Phi`.

Thus the completed kernel is not a complete invariant of the pair realization.

## 5. Same image does not erase degree

On `R x S^1`, consider

\[
F_n(t,u)=(t,\cos(nu),\sin(nu),0).
\]

Every nonzero `n` has the same image cylinder. Its restriction to the circle has degree `n`. A
circle diffeomorphism has degree `+1` or `-1`, and

\[
\deg(F_n\circ\psi)=n\deg(\psi).
\]

Consequently precomposition preserves `|n|`. In particular, `F_1` and `F_2` are not realization
isomorphic even though their image sets agree.

## 6. Reflections and windings are query-conditional

For the G183 polynomial branches

\[
F_\pm(t,s)=(t,s,\pm s(1-s)),
\]

the calibrated ambient `s` coordinate forces any strict commuting reparameterization to have the
same spatial parameter. The two maps then disagree for `0<s<1`, so they are strict-distinct.

The ambient reflection

\[
A(t,x,y)=(t,x,-y)
\]

is an isometry, fixes the endpoint observer lines, and maps `F_+` to `F_-`. Therefore the two are
equivalent in the extended quotient exactly when this reflection is admitted by `Aut_g(Q)`. If the
query fixes transverse screen orientation, the reflection is excluded and the branches remain
distinct.

For the flat product winding family with lifted displacement

\[
\ell_n=1+2n,
\]

a strict endpoint-preserving domain diffeomorphism cannot change the lift: differentiating a lifted
commuting diagram and integrating from `0` to `1` gives `ell_n=ell_m`. Circle reflection sends

\[
\ell_n\mapsto-\ell_n=\ell_{-n-1}.
\]

Thus `n` and `-n-1` become equivalent only when the reflection is admitted. Distinct `|ell_n|`
remain distinct under the endpoint-stabilizing circle isometries. Ordered observer reversal is not
being quotient out here.

## 7. Non-scalar transport remains separate

If a query also supplies a path, connection, Jacobi propagator, or screen transport, a realization
isomorphism carries that object by its own functorial law. This does not make it a real scalar and
does not infer nontrivial holonomy from a winding label. The completed scalar kernel remains
unchanged; the quotient only removes duplicate descriptions allowed by the typed query.

## 8. Classification theorem

On the supplied regular arena:

| Comparison | Sufficient for same realization class? | Exact qualification |
|---|---:|---|
| strict query-preserving commuting diffeomorphism | yes | same realization, different pair coordinates |
| commuting diffeomorphism plus admitted query isometry | yes in extended quotient | only if the symmetry is explicitly typed |
| equal endpoints | no | branch tangents and embeddings may differ |
| equal completed scalar or tape | no | scalar evaluator is many-to-one |
| equal completed pair metric | no | extrinsic data may differ |
| equal image set | no | covering degree/multiplicity may differ |
| reflected branch | conditional | depends on transverse-orientation/symmetry policy |
| opposite winding lift | conditional | reflection may identify sign; absolute lift survives |

Primary landing:

```text
TYPED_REALIZATION_ISOMORPHISM_CLASSIFIES_REGULAR_BRANCH_EQUIVALENCE__KERNEL_IS_NOT_A_COMPLETE_REALIZATION_INVARIANT
```

The first clause is the exact typed quotient definition and descent theorem. The second is the
substantive counterexample result. Neither clause selects a physical branch or query symmetry
policy, and neither scalarizes transport or globalizes beyond the supplied regular arena.
