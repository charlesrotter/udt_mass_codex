# Exact operator-algebra derivation

Let `S` be a real oriented positive two-dimensional screen with metric `q`. Every real endomorphism
`K:S->S` has the unique metric decomposition

```text
K = a I + W + J,
a = tr(K)/2,
W = (K-K^dagger)/2,
J = (K+K^dagger)/2 - a I.
```

Here `a I` is the isotropic trace/area response, `W` is the one-dimensional skew rotation sector,
and `J` is the two-dimensional self-adjoint trace-free shape sector. Hence

```text
End(S) = R I direct-sum so(S,q) direct-sum Sym_0(S,q),
dim End(S) = 1+1+2 = 4.
```

In a positively oriented orthonormal basis choose

```text
R  = [[0,-1],[1,0]],
S1 = [[1,0],[0,-1]],
S2 = [[0,1],[1,0]].
```

Direct multiplication gives

```text
[R,S1]=2S2,  [R,S2]=-2S1,  [S1,S2]=-2R.
```

Thus the trace-free sector is closed and is the split real algebra `sl(2,R)`. Its trace-form inertia
in this basis is `(2 positive, 1 negative, 0 zero)`, so it is not the compact algebra `su(2)`.

For general real dimension `n`, write a traceless endomorphism as the sum of a skew matrix and a
symmetric trace-free matrix. The dimensions are

```text
dim so(n)     = n(n-1)/2,
dim Sym_0(n)  = n(n+1)/2 - 1,
sum           = n^2 - 1.
```

The commutators obey

```text
[skew,skew] subset skew,
[skew,symmetric] subset symmetric trace-free,
[symmetric,symmetric] subset skew,
```

and the constructed basis has rank `n^2-1`; therefore it closes `sl(n,R)`. The production script
checks this exactly for `n=2,...,6`.

For `n=3`, the dimensions are `3+5=8`. With real matrices the trace form has inertia `(5,3,0)`, the
signature of the split real form used here. Multiplying the five symmetric generators by `i` and
using anti-Hermitian matrices yields a positive `-Re tr(XY)` form and the compact real algebra
`su(3)`. That multiplication is an additional complex/Hermitian choice. It is not supplied merely
by a real three-dimensional angular metric.

The spherical-tensor dimension check gives the same generic result: on a spin-`ell` representation
of dimension `2ell+1`, tensor ranks `1,...,2ell` have total dimension

```text
sum_(k=1)^(2ell) (2k+1) = (2ell+1)^2 - 1.
```

Consequently the old rank-one plus rank-two `3+5=8` observation is the `ell=1`, `n=3` instance of a
general endomorphism identity. No particle label is required, and no particle conclusion follows.
