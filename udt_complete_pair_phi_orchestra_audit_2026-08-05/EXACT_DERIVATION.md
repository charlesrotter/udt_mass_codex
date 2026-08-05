# Exact derivation — complete-pair phi and the angular orchestra

## 1. The framing correction

The preceding distance-identification audit used an equal-pointwise-`phi`, nonzero-angular-arc
control to prove that

```text
abs(phi(q)-phi(p))
```

cannot by itself be the complete spatial separation while the angular sector remains live. That
statement is correct but narrower than one possible reading of its prose. It does not prove that an
angular contribution must be calculated separately and attached afterward. It does not test a
signed pair depth already extracted from the complete A-to-B comparison.

This audit therefore asks whether the complete comparison can itself carry the angular and mixing
modulation.

## 2. A frame-covariant complete-arrow strain

Let

```text
A:(V_p,g_p) -> (V_q,g_q)
```

be a typed invertible comparison arrow. Its metric adjoint and source strain are

```text
A^dagger = g_p^-1 A^T g_q,
C_A       = A^dagger A.
```

In orthonormal endpoint coframes, independent Lorentz changes act as

```text
A -> L_q A L_p^-1.
```

Exact substitution gives

```text
C_A -> L_p C_A L_p^-1.
```

Therefore the conjugacy data of `C_A`—its characteristic polynomial, eigenvalues together with
the causal signatures of regular eigenspaces, and trace invariants—are independent of the endpoint
coframe presentations. This is a genuine complete-arrow object. It is not the trace of `A`, which
fails under independent endpoint frame changes.

The primary exact calculation uses distinct rational Lorentz boosts at the two endpoints and a
nontrivial lower-mixing arrow. The covariance identity and characteristic polynomial invariance
hold exactly.

## 3. Pure reciprocal reduction and a regular signed extractor

Write `r=exp(delta)>0`. On the pure founded four-slot control,

```text
D_r=diag(r^-1,r,1,1),
C_D=diag(r^-2,r^2,1,1).
```

The eigenline with eigenvalue `r^-2` is timelike, whereas the `r^2` eigenline is spacelike. The
ordinary unordered spectrum loses the sign by itself, but the Lorentzian causal label restores it:

```text
delta_t(D_r) = -(1/2) log(lambda_timelike) = log r = delta.
```

Consequently, on the regular stratum where `C_A` is real diagonalizable with positive eigenvalues
and exactly one distinguished timelike eigenline, define

```text
delta_t(A)=-(1/2) log(lambda_t(A)).
```

This is endpoint-frame invariant and reduces exactly to the founded signed depth.

For the reversed arrow,

```text
C_(A^-1) = A C_A^-1 A^-1.
```

Its corresponding eigenvalue is `lambda_t^-1`. If `C_A v=lambda_t v`, then

```text
g_q(Av,Av)=g_p(v,C_A v)=lambda_t g_p(v,v),
```

so positive `lambda_t` preserves the causal signature of that eigenline. Therefore

```text
delta_t(A^-1)=-delta_t(A)
```

on this regular stratum.

This construction can fail or become multivalued when strain eigenvalues cease to be positive and
real, when Jordan degeneracy occurs, or when a unique timelike eigenline is lost. It is a derived
regular-stratum extractor, not a theorem covering every complete comparison.

## 4. Exact mixing modulation in one A-to-B comparison

Use the registered lower-triangular form with founded upper block and one clock-to-screen mixing:

```text
A = [[1/2, 0,   0, 0],
     [0,   2,   0, 0],
     [1/4, 0,   1, 0],
     [0,   0,   0, 1]].
```

The quotient/founded upper block has

```text
delta_quotient=log 2.
```

The clock-screen part of `C_A` instead has characteristic polynomial

```text
lambda^2-(19/16)lambda+1/4,
```

with positive eigenvalues

```text
lambda_-= (19-sqrt(105))/32,
lambda_+= (19+sqrt(105))/32.
```

The `lambda_-` eigenline is timelike. Thus

```text
delta_t=-(1/2)log[(19-sqrt(105))/32]
       approximately 0.6481668896,

delta_quotient=log 2
              approximately 0.6931471806.
```

They differ exactly. The complete mixing sector has therefore changed the frame-invariant
timelike-strain depth of this single A-to-B arrow. This is a constructive witness for the user's
orchestra framing.

It simultaneously proves nonuniqueness: the same triangular arrow has a founded quotient character
and a complete-strain character, and current premises do not identify them.

## 5. Complete magnitudes exist but are not unique

On a diagonal regular control with logarithmic strains

```text
log spectrum(C_A)=(-2d,2d,2a,2b),
```

two normalized reversal-even, endpoint-frame invariant magnitudes are

```text
rho_2^2 = Tr[(log C_A)^2]/8
        = d^2+(a^2+b^2)/2,

rho_4^4 = Tr[(log C_A)^4]/32
        = d^4+(a^4+b^4)/2.
```

Both reduce to `abs(d)` when `a=b=0`. They differ when the screen strains are live. For
`(d,a,b)=(1,1,0)`, their defining powers are both `3/2`, but

```text
rho_2=sqrt(3/2),
rho_4=(3/2)^(1/4).
```

Neither endpoint-frame covariance nor pure reciprocal reduction selects one.

Moreover, signing either norm with the reciprocal orientation does not make it additive. Two
diagonal legs `(1,1,0)` and `(1,-1,0)` each have signed `rho_2=sqrt(3/2)`, while their product has
logarithmic vector `(2,0,0)` and signed `rho_2=2`, not `2sqrt(3/2)`.

Thus a complete strain norm can describe “how much the orchestra changed,” but arbitrary norms are
not automatically the founded reciprocal depth.

## 6. Exact composition identifies the mathematical home

A signed reciprocal depth on typed paths must obey

```text
delta(beta o gamma)=delta(beta)+delta(gamma),
delta(gamma^-1)=-delta(gamma),
delta(identity)=0.
```

This is precisely a real-valued `1`-cocycle on the observer/path comparison groupoid.

If such a cocycle is locally represented by a one-form `alpha` on the appropriate observer/query
bundle, then

```text
delta(gamma)=integral_gamma alpha.
```

Concatenation and reversal follow automatically. Endpoint-only descent requires zero integral on
every admissible loop. Locally this is `d alpha=0`; globally all periods must also vanish. When that
condition holds, `alpha=dPhi` locally and the depth is a potential difference. When it does not,
the path label is physical comparison data rather than an algebraic error.

The one-form representation here is conditional on a local first-order linear path generator. The
general groupoid-cocycle statement does not assume every possible path functional is a one-form.

An exact triangle control demonstrates the descent gate. Assign depths `d01,d12,d20` to its three
oriented edges. A point potential exists exactly when

```text
d01+d12+d20=0.
```

The loop sum is the obstruction.

## 7. An exact angular-modulated reciprocal cocycle family

Consider the bounded stationary integrable `2+2` warped branch with intrinsic timelike Killing norm
`N` and screen area radius `R`. On this branch both are metric readouts after the Killing line,
screen split, and fixed screen identification are supplied.

For every real constant `a`, define

```text
alpha_a = -d log N + a d log R,

delta_a(p,q)
  = log[N(p)/N(q)] + a log[R(q)/R(p)].
```

Exactly,

```text
delta_a(p,q)+delta_a(q,r)=delta_a(p,r),
delta_a(q,p)=-delta_a(p,q).
```

At constant screen radius—or at `a=0`—this reduces to the already audited stationary Killing
depth. When `R(q)/R(p)` is nontrivial and `a` is nonzero, the angular screen modulates the signed
depth even for one A-to-B comparison. Nothing is appended afterward.

The same result appears as a character of the split-preserving block-triangular comparison group:

```text
delta_a(A)=delta_quotient(A)+a log det Q_A,
```

up to the convention relating `R` to screen area. Lower unipotent mixing does not enter this
ordinary character, while screen area does. More general path cocycles could depend on twist or
mixing through connection/curvature data, but none is selected here.

This family is a positive existence theorem and an exact nonuniqueness theorem. The active premises
do not select `a`. `c_E` fixes an ordinary clock/length calibration and `X_max` fixes required
limiting behavior; neither alone supplies the missing coefficient or the complete cocycle.

## 8. What survives and what is corrected

The previous one-arrow/two-readout theorem survives unchanged once a signed arrow is supplied.
The new audit sharpens what can supply that arrow:

- `DERIVED`: complete-arrow strain conjugacy data are endpoint-frame invariant.
- `DERIVED ON A REGULAR STRATUM`: the causal timelike strain eigenvalue produces a signed extractor
  that reduces to founded `delta` and reverses correctly.
- `DERIVED EXISTENCE`: complete mixing can modulate that strain depth for one pair.
- `DERIVED STRUCTURAL TYPE`: exact compositional depth is a real groupoid cocycle.
- `DERIVED CONDITIONAL FAMILY`: stationary screen geometry can modulate an exact reciprocal cocycle.
- `OPEN`: which strain/cocycle, if any, is the physical UDT pair depth on the complete solution
  space.

The equal-pointwise-`phi` angular control is now scoped only as follows:

```text
It refutes complete distance = abs(pointwise phi(q)-pointwise phi(p))
when the angular sector is held outside that scalar.
```

It does not refute a complete relational `phi_AB` whose defining cocycle already depends on the
angular or mixing geometry.

## 9. Sharpened missing object

The missing object is not an angular correction term. It is a metric-natural rule

```text
Alpha:
  (complete global metric/coframe,
   ordered observer/event query,
   admissible path data)
  -> real groupoid 1-cocycle delta,
```

or a more general local path functional with the same exact composition and reversal laws.

That rule must state:

1. whether the depth is extracted from full strain, integrated from a connection-like object, or
   obtained by another metric-native construction;
2. how angular, mixing, twist, and global completion enter;
3. where the regular strain branch changes type or degenerates;
4. whether paths are retained or all loop periods vanish;
5. how `c_E` and `X_max` calibrate the resulting physical readout; and
6. which complete configurations realize it.

Current metric structure makes this object possible and tightly typed. It does not yet select it.
No action, source, carrier, boundary, bootstrap return, matter, mass, dynamics, signal law, or
observational prediction follows from this audit.
