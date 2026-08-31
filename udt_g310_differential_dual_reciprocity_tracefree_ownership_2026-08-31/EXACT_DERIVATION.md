# G310 exact derivation — differential Dual Reciprocity and trace-free ownership

Date: 2026-08-31
Grade: `EXTERNALLY_VERIFIED_AFTER_PREREGISTERED_EVIDENCE_REPAIRS`

## 1. Bounded landing

```text
ONE_NEW_DIFFERENTIAL_DUAL_RECIPROCITY_POSTULATE_SELECTS_G301_TRACEFREE_CLASS
__NOT_DERIVED_OR_ADOPTED
```

The wording “one new postulate” means one compound, explicitly typed law premise inside G301's
already conditional local operator arena. It does not mean F1--F4 or W1--W6 have now been shown to
imply that arena or the postulate.

## 2. The candidate postulate

Let `(V,g)` be one regular four-dimensional Lorentz tangent space. For every orthonormal ordered
timelike-spacelike pair `(u,n)`, define the infinitesimal reciprocal metric tangent

\[
H(u,n)=2\bigl(u^\flat\!\otimes u^\flat+n^\flat\!\otimes n^\flat\bigr).
\]

Directly differentiating the founded pair block gives

\[
\left.\frac{d}{ds}\right|_{s=0}
\left[D(s)^T\operatorname{diag}(-1,1)D(s)\right]
=2\operatorname{diag}(1,1),
\]

so this is exactly the reciprocal shape tangent embedded in the chosen pair plane. Its metric trace
is

\[
\operatorname{tr}_gH=2\bigl(g(u,u)+g(n,n)\bigr)=2(-1+1)=0.
\]

The proposed differential Dual Reciprocity statement (`DDR`) is:

> The first local natural complete-metric curvature response `E_ab` has zero contraction with every
> reciprocal pair-shape tangent on a physical solution:
> \[
> \langle E,H(u,n)\rangle_g=0
> \quad\text{for all orthonormal }(u,n).
> \]

This is a new law-level balance statement. Algebraic Dual Reciprocity supplies `H`; it does not
state the displayed stationarity condition. “First local natural curvature response” also places
the candidate inside G301's conditional smooth, scale-free, local metric-only symmetric rank-two
curvature class. Those typing clauses remain part of the proposed premise rather than hidden
theorems of W4.

## 3. All reciprocal planes span the nine shape directions

Choose an orthonormal frame `(e0,e1,e2,e3)`. The three tangents

\[
H(e_0,e_i),\qquad i=1,2,3,
\]

span the diagonal trace-free subspace.

For two spatial basis vectors, choose rational `c,s` with `c^2+s^2=1` and set
`n=c e_i+s e_j`. The exact combination

\[
\frac12H(e_0,n)
-c^2\frac12H(e_0,e_i)
-s^2\frac12H(e_0,e_j)
=cs\,(e_i^\flat\!\odot e_j^\flat)
\]

produces each of the three spatial off-diagonal directions.

For each `i`, choose rational hyperbolic data `C^2-S^2=1` and set

\[
u'=Ce_0+Se_i,\qquad n'=Se_0+Ce_i.
\]

Then

\[
\frac12H(u',n')-(C^2+S^2)\frac12H(e_0,e_i)
=-2CS\,(e_0^\flat\!\odot e_i^\flat),
\]

which produces the three time-space off-diagonal directions. Therefore

\[
\boxed{
\operatorname{span}\{H(u,n)\}=S^2_0(V^*),\qquad \dim S^2_0(V^*)=9.
}
\]

The production certificate independently builds 133 exact rational Lorentz transforms of one seed
plane. Their orbit has rank nine; the uncomposed generators have rank eight, and the first exact
greedy basis occurs at indices `0,1,3,4,5,6,7,9,38`. Adding `g_ab` raises the rank to ten. The
separate verifier uses different rational rotation and boost data and constructs the nine standard
directions explicitly. After external review, both certificates retain the full displayed
factor-two normalization rather than using the span-equivalent half-tangent.

## 4. The annihilator is exactly the common trace line

The metric pairing on symmetric tensors is nondegenerate, and

\[
S^2(V^*)=S^2_0(V^*)\oplus\mathbb Rg.
\]

Consequently

\[
\boxed{
\langle E,H(u,n)\rangle_g=0\ \forall(u,n)
\iff E\in\mathbb Rg.
}
\]

The constructive proof makes this elementary. The three diagonal planes give
`E_ii=-E_00`; rotated spatial planes give `E_ij=0`; boosted planes give `E_0i=0`. Hence `E` is a
multiple of `g`. The exact balance matrix has rank nine and one-dimensional nullspace `span(g_ab)`.
The repaired separate verifier now independently builds the Lorentz-pairing rows, row-reduces them,
computes their nullspace, and reads these component equations from that computed vector.

This already proves that DDR constrains shape but cannot fix the common trace magnitude. Replacing
the conclusion by `E=0` would be an overconstraint not contained in DDR.

## 5. Conditional insertion of the G301 response

G301 proves, inside its frozen smooth scale-free natural rank-two curvature lane,

\[
E_{ab}=aR_{ab}+bR g_{ab}.
\]

Every reciprocal tangent is traceless, so

\[
\langle E,H\rangle_g
=a\langle\operatorname{Ric},H\rangle_g
+bR\langle g,H\rangle_g
=a\langle\operatorname{Ric},H\rangle_g.
\]

Equivalently,

\[
\operatorname{TF}(E)=a\left(R_{ab}-\frac14Rg_{ab}\right)=aS_{ab}.
\]

Thus on the nondegenerate G301 principal stratum `a!=0`,

\[
\boxed{
\mathrm{DDR}\iff S_{ab}=R_{ab}-\frac14Rg_{ab}=0.
}
\]

The coefficient `b` cancels, so DDR selects the trace-free zero set without choosing a
representative response formula. When `a=0`, `E=bRg` lies in the trace line for every metric and DDR
is vacuous. This is why G301's nonzero Ricci/principal gate is load-bearing.

No action is used. If one later describes DDR as restricted virtual work or determinant-preserving
variation, that is an interpretation of the displayed balance, not an independent derivation of it.

## 6. What remains after the conditional closure

The contracted Bianchi identity gives

\[
\nabla^aS_{ab}=\frac14\nabla_bR.
\]

Therefore a connected DDR/G301 solution has

\[
R=R_0=\text{constant},
\qquad
R_{ab}=\frac{R_0}{4}g_{ab}.
\]

DDR leaves one scalar datum rather than a free local function. It does not choose its value or sign.
This precisely matches the nine reciprocal shape directions plus one retained common metric-scale
direction found in G302.

In the primary static-spherical chart, the covariant residual reduces to

\[
r^2f''-2f+2=0,
\qquad
f(r)=1+\frac br-\frac{R_0}{12}r^2.
\]

In the positive round time-live arena, it reduces to

\[
aa''-a'^2-1=0,
\]

whose positive standard complete family is

\[
a(T)=X\cosh\left(\frac{T-T_0}{X}\right).
\]

These are downstream regression checks. They did not enter the covariant derivation. Smooth-center
and the active working finite-ceiling condition may subsequently remove `b` and distinguish the
positive sign in their already bounded G304 scope; neither fixes `X`.

## 7. Countermodels and exact boundary

The result survives its preregistered controls:

- one radial pair plane has rank one and cannot determine the response;
- the uncomposed finite generator family has rank eight, not nine;
- scalar-only `a=0` satisfies every balance identically and is not a shape law;
- nonzero multiples of `g` satisfy every balance, so the trace magnitude remains free;
- G309's smooth time-live deformation remains admitted by the old postulates and is rejected only
  after DDR is supplied.

G309 therefore still refutes landing 4: the founding chain does not already imply DDR. G310 lands
on preregistered candidate 1 with its stated ownership qualification.

## 8. Completeness and ownership ledger

The covariant algebra acts on the full four-dimensional metric and drops no metric component or
angular/screen direction. However, it chooses a local, second-order, smooth, scale-free,
metric-only, symmetric rank-two response architecture and an all-pair balance condition. Higher
order, nonlocal, auxiliary-state, parity-odd, source-coupled, and global relation laws are outside
this tile and remain logically possible.

Accordingly, G310 establishes a sharply typed candidate missing premise:

```text
DIFFERENTIAL_DUAL_RECIPROCITY_ALL_PAIR_CURVATURE_BALANCE
```

It does not establish that F1--F4/W1--W6 own that premise, adopt it as UDT physics, select its scalar
datum, or derive a realized global history, source, matter, mass, observation, scale, or physical
`X_max`.
