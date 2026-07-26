# Exact derivation

## 1. What founded `phi` already is

The foundation supplies the real group coordinate of the reciprocal pair:

```text
D(phi)=exp(phi X),
X=-P_u+P_n+lambda(I-P_u-P_n).
```

This fixes the meaning of `phi` and the exponential response. It does not automatically provide a
map from every spacetime event or observer-pair path arrow into that real group.

If a global founded section `phi(x)` is supplied, then

```text
D(phi)^-1 dD(phi)=X dphi,
tr[X D^-1 dD]/tr[X^2]=dphi.
```

Thus the local current and endpoint depth are exact:

```text
delta_gamma=integral_gamma dphi=phi(B)-phi(A).
```

The unresolved issue is the physical section, not the algebra of `phi`.

## 2. Endpoint theorem

Let a real endpoint assignment satisfy

```text
delta(A,B)+delta(B,C)=delta(A,C),
delta(B,A)=-delta(A,B).
```

Choose a bookkeeping base event `O` and define `phi(A)=delta(O,A)`. Then the triangle `(O,A,B)`
gives

```text
delta(A,B)=phi(B)-phi(A).
```

The base event fixes only the additive zero. Therefore every exact endpoint-only real cocycle is a
potential difference. This theorem does not establish that a globally valid physical potential is
selected.

## 3. Why Levi-Civita transport cannot create the dilation component

In an orthonormal frame, a Levi-Civita connection form `Omega` is metric-skew:

```text
Omega^dagger=-Omega.
```

The founded reciprocal generator is metric-self-adjoint:

```text
X^dagger=X.
```

The trace pairing therefore obeys

```text
tr(X Omega)
 =tr((X Omega)^dagger)
 =tr(Omega^dagger X^dagger)
 =-tr(Omega X)
 =-tr(X Omega),
```

so

```text
tr(X Omega)=0.
```

This is the infinitesimal version of the prior result that metric parallel transport is isometric,
whereas nonzero aligned reciprocal dilation is self-adjoint and changes the metric readout. The
complete metric supplies pair transport along a path, but its metric-compatible connection supplies
no nonzero reciprocal depth component.

## 4. Why raw coframe differentiation seems to work

Write a physical coframe relative to a chosen reference coframe as

```text
e=D(phi) theta.
```

Direct component differentiation recovers `dphi`. But choose another reciprocal reference

```text
theta'=D(chi) theta.
```

The same physical coframe is now represented by `D(phi-chi) theta'`, and the extracted current is

```text
dphi-dchi.
```

A constant reference shift cancels in endpoint differences. A nonconstant reference change does not.
The raw expression is therefore exact relative to a selected reference and transition law; it is not
by itself a reference-free consequence of the metric. Replacing the raw derivative by the tensorial
Levi-Civita covariant derivative returns the zero result above.

## 5. Relative coframe logarithm

If a supplied endpoint comparison map lies in the positive founded pair subgroup,

```text
A=diag(q^-1,q), q>0,
```

then its depth is uniquely

```text
delta=1/2 log(A_rr/A_tt)=log q.
```

Products inside one common subgroup multiply `q`, so their depths add. This is a derived readout from
a supplied relative map. It does not derive that map from the metric.

The construction does not extend as a scalar homomorphism to arbitrary complete coframe maps. For

```text
A=diag(1/2,2),
B=[[5/4,3/4],[3/4,5/4]],
```

`A` and `B` do not commute. Projecting the principal logarithm of `BA` onto the reciprocal generator
gives

```text
15 acosh(25/16)/sqrt(369)=0.7936345282...,
```

while the sum of the separate projections is

```text
log 2=0.6931471806....
```

Angular/mixing information therefore cannot generally be discarded before composition.

## 6. Bilocal magnitude and observer charts

A nonnegative metric separation is symmetric. A signed depth is reversal odd. If one scalar were
both, then

```text
rho(A,B)=rho(B,A)=-rho(A,B),
```

which forces `rho=0`. Generic metric distances also do not add on triangles; they add only on special
ordered geodesic subsegments.

An observer-indexed chart `rho_p(q)=F(d(p,q))` remains a viable relational magnitude type. To become
the real arrow label used by the reciprocal character it needs a signed lift, profile, overlap law,
and—in general—angular composition data. The present audit does not reject that wider construction.

## 7. Two exact but unselected cocycle factories

For any globally supplied one-form `alpha`,

```text
delta_gamma=integral_gamma alpha
```

is signed and additive on path-labelled arrows. Endpoint collapse additionally requires zero loop
periods. Because the positive real reciprocal character is faithful, a nonzero real period remains a
visible reciprocal holonomy.

Likewise, any selected dimensionless scalar metric invariant `I(g)` gives

```text
delta(A,B)=I(B)-I(A).
```

But `I`, `2I`, `I^3`, and many other choices all work algebraically. Current UDT structure selects no
formula, normalization, or identification with founded depth, and nontriviality is not guaranteed.

These examples prevent an overbroad no-go claim: a complete global solution may yet select a depth.
They do not close the current foundation.

## 8. Clock-frequency control

With endpoint observers, events, a signal covector, and a matched common path supplied,

```text
delta_Q=log(omega_B/omega_A)
```

adds and reverses exactly. Prior work correctly labels this a derived clock-ratio cocycle given typed
data. Its identity with the founded reciprocal depth is conditional; the signal/readout data do not
follow merely from the pair character.

## 9. Bounded conclusion

None of the eight registered routes is simultaneously metric-native, signed, additive,
frame-covariant, nontrivial, and founded-aligned without an extra physical choice. The missing item is
not a definition of `phi`: it is a metric-native normalized map from typed pair-path arrows to the
already founded real reciprocal coordinate. Equivalently, it could appear as a selected reference
section with transition law or as a selected reciprocal connection/current.

No such new connection is adopted here.
