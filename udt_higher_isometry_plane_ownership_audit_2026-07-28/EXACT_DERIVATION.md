# Exact derivation — higher-isometry plane ownership

## 1. Bounded descended family

On the chosen stationary `R_t x S3` control, write

```text
u=exp(-2 phi)>0,
g=-u(c_E dt+alpha A)^2+u^-1 A^2+q_B.
```

The Hopf connection `A`, depth `phi`, and positive two-shear base metric `q_B` are invariant under
the registered vertical circle `V`. Add an arbitrary commuting compact Killing generator `Y` and
define

```text
A(V)=1,
A(Y)=f,
H=Y-fV,
b=q_B(H,H)>0
```

on the principal-orbit interior. `f` is the connection moment of the extra circle and `b` is its
horizontal squared norm. At a toric cap `b` can vanish because the orbit rank drops; the complete
metric remains regular there.

No action, equation, carrier, source, density, bootstrap value, boundary law, or dynamics enters.

## 2. Complete three-direction orbit Gram metric

In the fixed global Killing basis `(K,V,Y)`, the complete orbit Gram matrix is

```text
G3 = [ -c_E^2 u        -c_E alpha u       -c_E alpha u f                    ]
     [ -c_E alpha u     Q                  Q f                               ]
     [ -c_E alpha u f   Q f                Q f^2+b                           ],

Q=u^-1-alpha^2 u.
```

The base-dependent replacement `H=Y-fV` gives the congruent form

```text
[ reciprocal (K,V) block ] direct_sum [ b ].
```

Consequently

```text
det G3=-b c_E^2
```

and its principal-orbit inertia is exactly one negative and two positive directions. This result is
independent of `phi`, `alpha`, and the moment `f`.

## 3. Full orbit response versus a restricted plane scan

On the principal-orbit region `b>0`, for a transverse direction `X`, put

```text
chi=X(phi),  df=X(f),  db=X(b),
D3=G3^-1 X(G3).
```

The exact matrix is recorded in `DERIVATION_RESULT.json`. Its trace is

```text
tr D3=db/b,
```

because the reciprocal pair cancels from the full orbit volume and only the horizontal norm
remains. The characteristic polynomial is

```text
p(lambda)=lambda^3-(db/b)lambda^2
 +[alpha^2 df^2 u/b-df^2/(bu)-4chi^2]lambda
 -2alpha^2 df^2 u chi/b+4(db/b)chi^2-2df^2 chi/(bu).
```

In particular,

```text
p(-2chi)=-4 alpha^2 df^2 u chi/b,
p(+2chi)=-4 df^2 chi/(bu).
```

Thus the old reciprocal rates are not generally eigenvalues of the *full* three-direction response
when the extra circle has a varying moment. More directly, the `Y` components of `D3(K)` and
`D3(V)` are

```text
-alpha c_E df u/b,
-df(alpha^2 u^2-1)/(bu).
```

They cannot vanish simultaneously for `df != 0`. The registered plane is a full-response invariant
plane exactly on the `df=0` stratum. When `df=0`, the characteristic polynomial factors as

```text
(lambda+2chi)(lambda-2chi)(lambda-db/b).
```

This does not invalidate the preceding two-plane result. It exposes two different metric
operations:

1. form `D3` on the whole higher-isometry algebra and seek its invariant eigenspaces; or
2. scan every actual `R x S1` symmetry subgroup, restrict the metric to each subgroup, and compute
   its own induced two-dimensional Gram response.

The first operation mixes the registered plane wherever `df!=0`. The second tests a different
property. Conflating them would be a false shortcut. The characteristic polynomial and the
displayed `df=0` factorization do not constitute the preregistered exhaustive rank/eigenline/
invariant-subspace degeneracy atlas; that classification remains open.

For a bundle-preserving extra circle, Cartan's identity gives

```text
0=L_Y A=i_Y F+d(A(Y)),
df=-i_Y F.
```

On the nontrivial Hopf base, `F` is a nondegenerate area form. An independent projected circle
therefore has `df != 0` somewhere. Full-response mixing at such points is exact and is not a
removable coordinate effect.

## 4. Every symmetry plane

Every `R x S1` subgroup of the principal orbit group can be represented by

```text
T=K+rV+sY,
Z=mV+nY,
```

where `Z` is the compact line and the nonzero coefficient of `K` in `T` has been normalized to one.
Put

```text
Delta=rn-ms,
z=m+nf.
```

The exact determinant of the induced plane Gram metric is

```text
det G(T,Z)
 = b Delta^2/u - c_E^2 z^2 - u b(c_E n+alpha Delta)^2.
```

Constancy of this determinant is invariant under every constant basis change inside the plane; it
is the reciprocal two-area part of the previous certificate.

Demanding constancy as an identity under independent variation across the whole free `(u,f,b)`
configuration family gives

```text
d(det G(T,Z))/df=-2c_E^2 n(m+nf)=0,
```

so the independent compact direction must have `n=0`. Then

```text
det G(T,mV)=m^2[-c_E^2+b s^2(u^-1-alpha^2u)].
```

Identity under the free positive screen norm and depth then requires `s=0`. The remaining plane is

```text
span(K+rV,mV)=span(K,V),
```

with constant determinant `-m^2 c_E^2`. Its restricted Gram response is exactly the previous
two-dimensional response and carries the founded rates for nonconstant `phi`.

This proves that `span(K,V)` is the only plane with constant reciprocal area robust under
independent variation across the entire free family. It does **not** prove uniqueness for a fixed
cohomogeneity-one metric. For fixed profiles `u(rho),f(rho),b(rho)`, constancy requires only

```text
F_u u'+F_f f'+F_b b'=0,
```

and cancellations along the one-dimensional profile are possible. Every such profile curve also
has local functional relations, so absence of a relation is not a realizable open-stratum
definition. A fixed-profile necessary-and-sufficient classification or a valid transversality
theorem is missing. Generic fixed-metric uniqueness remains `OPEN`.

## 5. All constant Killing clock candidates

For

```text
W=tK+pV+qY,
s_W=p+qf,
```

the exact norm is

```text
g(W,W)=-u(c_E t+alpha s_W)^2+s_W^2/u+q^2b.
```

The founded clock-rate residual is

```text
R_W=X[g(W,W)]+2chi g(W,W).
```

Its full polynomial is saved and independently reconstructed. Requiring the clock residual to
vanish identically under independent family variation makes the coefficient of `db` equal to
`q^2`, so `q=0`. With `q=0`,

```text
R_W=4chi p^2/u.
```

Requiring identity under an independent nonzero depth jet then gives `p=0`; only the line `K`
survives family-wide. On a fixed cohomogeneity-one profile, cancellations can again occur. This is
a founded-`phi` family-robustness diagnostic, not a fixed-profile uniqueness theorem and not a
substitute for the metric-only plane scan.

## 6. Exact smooth nonconstant-depth countercontrol

Universal plane selection fails inside the admitted family. Use standard Hopf coordinates on
`S3`, with the two torus circles

```text
V=partial_xi1+partial_xi2,
Y=partial_xi1-partial_xi2,
f=A(Y)=cos(2 eta).
```

Both are primitive free circles: the Hopf and anti-Hopf lines. Set

```text
alpha=0,
u=1+epsilon(1-f^2),  epsilon>0,
q_B=u^-1 q_round_base.
```

Then `u` is smooth, positive, and nonconstant, and

```text
b=(1-f^2)/u.
```

The apparent zeros of `b` are exactly the regular toric caps. The radial base coefficient is also
`u^-1`, so no cone defect is introduced. The full spatial metric is `u^-1` times the round `S3`
metric. Both induced planes have exactly

```text
G(K,V)=diag(-c_E^2u,u^-1),
G(K,Y)=diag(-c_E^2u,u^-1).
```

Thus a smooth complete nonconstant-depth metric contains two different free reciprocal ruler
planes. In the displayed even witness an isometry exchanges them, so the metric cannot distinguish
one as the registered plane.

Turning on nonzero `alpha` illustrates rather than erases the strata. The alternative `(K,Y)`
plane still has constant determinant, but its response obeys

```text
det D_KY +4chi^2=alpha^2 u^2 df^2.
```

For `alpha df != 0`, its rates are no longer the founded `plus/minus 2chi` pair, while the
registered `(K,V)` restriction retains them. The twist distinguishes the registered pair in this
specific witness; no equation here selects nonzero `alpha` physically.

## 7. Toric topology does not repair uniqueness

Let primitive cap cycles `(v_minus,v_plus)` be a unimodular basis, as required for the smooth
two-cap `S3` completion. A primitive circle `w` is free exactly when

```text
|det(v_minus,w)|=|det(v_plus,w)|=1.
```

Writing `w=x v_minus+y v_plus`, unimodularity makes these conditions `|x|=|y|=1`.
Modulo overall orientation, there are therefore exactly two free lines:

```text
v_minus+v_plus,
v_minus-v_plus.
```

The production enumeration confirms this for 104 cap bases; the independent implementation uses
232 different bounded bases. Topology supplies two candidates, not one.

## 8. Uncompleted illustrative homogeneous strata

The first draft included Berger-`U(2)` and constant-depth round labels as plausible controls, but
the package supplied neither explicit derivations nor independent checks for them. They are now
classified `UNVERIFIED_ILLUSTRATION_NOT_EVIDENCE` in `HIGHER_ISOMETRY_STRATA.tsv` and carry no
load-bearing weight. Higher-isometry metrics not preserving the registered Hopf bundle also remain
outside this bounded classification.

## 9. Exact classification

```text
UNIVERSAL_SELECTION_REFUTED__FAMILY_IDENTITY_ROBUSTNESS_DERIVED__
GENERIC_FIXED_METRIC_SELECTION_OPEN
```

Universal registered-plane ownership is refuted by the exact smooth nonconstant-depth double-plane
control. The registered plane is the only one robust under coefficientwise variation across the
entire free family, but its uniqueness for a generic fixed metric is open. The full `3 x 3` response
does not carry the registered plane as an invariant eigenspace where the extra circle moment varies,
and the complete response degeneracy atlas remains unfinished.

No physical branch, macro/micro assignment, carrier, action, source, density law, dynamics, or mass
emergence is derived.
