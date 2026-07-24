# Exact dual-systole derivation

## 1. Complete local metric chart

For

```text
D = [[exp(-phi), shear],
     [0,        exp(phi)]],
H = D^T D,
Q = H^-1,
```

`H` is positive definite and `det(H)=1`. Conversely, every positive
determinant-one symmetric two-metric has a unique positive triangular
Cholesky factor of this form. Thus real `(phi,shear)` covers the full local
shape space; it is not a selected physical branch.

Set

```text
x = shear exp(phi),       y = exp(2 phi) > 0,
tau = x + i y.
```

Then

```text
H = (1/y) [[1, x], [x, x^2+y^2]]
L_(p,q) = (p,q) Q (p,q)^T
        = |p tau-q|^2 / Im(tau).
```

The inverse is `phi=log(y)/2`, `shear=x/sqrt(y)`, so this is the entire
upper half-plane, not a truncated sample.

## 2. Equality curves and admissible walls

For primitive characters `w=(p,q)` and `v=(r,u)`, their equality locus is

```text
(p^2-r^2)(x^2+y^2) - 2x(pq-ru) + (q^2-u^2) = 0.
```

Only the portions on which no other primitive character is shorter are
actual shortest-character walls.

Suppose two distinct unoriented primitive characters `w,v` are co-shortest,
with common squared norm `L`. They are independent. The following
determinant argument makes the classification complete.

First derive the two-dimensional Hermite bound without importing a physical
theory. Choose a shortest primitive `w` and complete it to a unimodular
basis `(w,z)`. Replace `z` by `z+n w` so its inner product `B` with `w`
satisfies `|B|<=L/2`. Minimality gives `||z||^2>=L`; determinant one gives

```text
1 = L ||z||^2 - B^2 >= L^2-B^2 >= 3 L^2/4,
```

and therefore `L<=2/sqrt(3)<2`.

For the co-shortest pair, its metric area satisfies

```text
|det(w,v)| <= ||w|| ||v|| = L < 2.
```

The left side is a nonzero integer, hence `|det(w,v)|=1`. Every independent
co-shortest pair is therefore unimodular.

## 3. One standard wall and its vertices

In the unimodular basis `(w,v)`, the dual metric is

```text
Q_basis = [[L,B],[B,L]],
L^2-B^2 = 1.
```

The competitors `w+v` and `w-v` imply `|B|<=L/2`. Write `r=B/L`. Every wall
is consequently a `GL(2,Z)` image of

```text
-1/2 <= r <= 1/2,
L = 1/sqrt(1-r^2).
```

For the standard pair `(1,0),(0,1)`, the wall in upper-half-plane
coordinates is

```text
x^2+y^2=1,  |x|<=1/2,  y>0.
```

Interior points have exactly the two shortest unoriented lines. At `r=-1/2`,
`w+v` joins the tie; at `r=+1/2`, `w-v` joins it. The vertices are

```text
x=+/-1/2, y=sqrt(3)/2,
phi=(1/2) log(sqrt(3)/2),
|shear|=1/sqrt(2 sqrt(3)).
```

The reduced quadratic form shows that no fourth primitive line can have the
same minimum. Thus the continuous chamber complex has two-way walls,
three-way vertices, and no higher tie.

## 4. Covariance and transport

For a torus basis change `M in GL(2,Z)`,

```text
Q' = M Q M^T,       w' = M^(-T) w.
```

Therefore `w'^T Q' w'=w^T Q w`; the full shortest set is covariant. If the
two shift rows transform as `S'=M S`, then

```text
b_w = w^T S = w'^T S'
```

is also covariant for a supplied character.

Off the wall set a unique unoriented shortest line is locally constant in a
lattice trivialization. At a transverse wall crossing, the metric says
which line is shortest on either side and gives the tied set on the wall,
but supplies no sign, phase, or rule selecting one continuation.

On the exact shear-free reciprocal path:

```text
phi<0 : W_min={(1,0)}
phi=0 : W_min={(1,0),(0,1)}
phi>0 : W_min={(0,1)}.
```

The exchange therefore necessarily passes through a tie. This is a derived
geometric obstruction to a single metric-only phase direction across that
path, not a failure of the set-valued invariant.

## 5. Authority boundary

The metric and a supplied integral torus lattice derive the chamber complex,
the set-valued shortest-character invariant, and a projected connection for
each supplied line. They do not derive:

- an integral torus lattice on every completion;
- a globally unique line on a branch crossing a wall;
- sign or orientation;
- a phase section;
- physical use of the shortest line;
- the round `S^2` carrier or its action;
- density-to-geometry, matter, mass, or bootstrap closure.

Those statements remain separately classified in `GLOBAL_TRANSPORT_ATLAS.tsv`
and `STATUS_LEDGER.tsv`.
