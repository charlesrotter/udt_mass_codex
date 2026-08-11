# Exact derivation — complete-pair instrument mixing solution space

## 1. Landing

The preregistered landing is

`SPLIT_RELATIVE_SIGNED_ORCHESTRA_ATLAS`.

On any regular ordered pair surface with a correctly typed metric-orthogonal reciprocal/angular
`2+2` split, the complete Jacobian has an exact matrix decomposition

```text
V = (X;Y),
H_R = X^T eta_(1,1) X,
H_A = Y^T Y,
h = H_R + H_A.                                      (1)
```

`H_R` is the complete reciprocal contribution and `H_A` is the complete angular contribution to
the induced observer-pair metric. Neither freezes time, angle, shift, nor mixing. On the generic
invertible stratum, the pair `(H_R,H_A)` is a complete set of continuous orbit data for `V` under
the split-preserving frame group `O(1,1) x O(2)`, with proper/time/orientation components retained
as discrete data.

The corresponding area components obey an exact signed orchestra law,

```text
det(h) = -R + A + M_signed,                           (2)
```

where `R>=0` is reciprocal-plane area squared, `A>=0` is angular-plane area squared, and
`M_signed` is an indefinite mixed-sector contribution. This is not a convex mixture. The metric
does not supply a unique positive scalar “importance” for the mixed sector.

The physical curve through this solution space remains `OPEN`: algebra supplies the allowed
states and exact readouts, but not the time-live/on-shell evolution of `X` and `Y`, a branch-scale
map, or physical micro/terrestrial/cosmological labels.

## 2. Complete pair Jacobian and matrix orchestra

Use a local complete orthonormal coframe with

```text
eta = diag(-1,+1,+1,+1).
```

Let the ordered pair map have arbitrary tangent columns

```text
V_0 = (x0,x1,x2,x3)^T,
V_1 = (y0,y1,y2,y3)^T.
```

No component is set to zero. Its induced metric is

```text
h_ij = eta_ab V_i^a V_j^b.                           (3)
```

Relative to the supplied reciprocal/angular split, collect the first two coframe rows in `X` and
the angular rows in `Y`:

```text
X = [[x0,y0],        Y = [[x2,y2],
     [x1,y1]],            [x3,y3]].
```

Expanding (3) proves (1) directly. `H_A=Y^T Y` is positive semidefinite. On `det X != 0`, `H_R`
has Lorentzian inertia and `det(H_R)<0`. The regular pair conditions remain

```text
h00 < 0,
det(h) < 0.                                           (4)
```

This is the precise meaning of the angular orchestra modulating the reciprocal pair relation: it
adds a complete symmetric matrix, not one isolated angular function.

### Generic continuous completeness

Suppose `X,X'` are invertible and have the same reciprocal Gram matrix. Then

```text
Lambda = X' X^-1
```

satisfies

```text
Lambda^T eta_(1,1) Lambda = eta_(1,1).
```

Thus `X'` differs from `X` by `O(1,1)`. Similarly, if invertible `Y,Y'` obey
`Y'^T Y'=Y^T Y`, then `Q=Y'Y^-1` lies in `O(2)`. Therefore `(H_R,H_A)` classifies the generic
continuous split-frame orbit. Determinant signs and time/orientation choices distinguish the
proper connected components. Singular `X` or `Y` requires the lower-rank strata already listed in
`STRATA_ATLAS.tsv`.

This theorem is conditional on the split. It is not an invariant separation under a full ambient
Lorentz transformation that changes which plane is called reciprocal.

## 3. Exact area-volume atlas

Define the simple bivector

```text
B = V_0 wedge V_1,
B_ab = x_a y_b - x_b y_a.
```

Its six components satisfy the four-dimensional Pluecker simplicity relation

```text
B01 B23 - B02 B13 + B03 B12 = 0.                    (5)
```

Set

```text
R        = B01^2,
A        = B23^2,
M_signed = -(B02^2+B03^2) + (B12^2+B13^2).          (6)
```

Exact expansion of the Gram determinant gives (2). Equivalently,

```text
det(H_R) = -R,
det(H_A) = +A,
det(h)-det(H_R)-det(H_A) = M_signed.                 (7)
```

If the mixed components are arranged as

```text
M = [[B02,B03],
     [B12,B13]],
```

then (5) is

```text
det(M)=B01 B23.                                      (8)
```

This is a genuine coupling law among the instruments. Whenever both oriented pure-sector areas
are nonzero, the mixed matrix must be full rank with their product as its determinant. The
reciprocal, angular, and mixed sectors cannot be varied as three independent sliders.

For a regular Lorentzian pair define

```text
Omega = -det(h) = R-A-M_signed > 0.                  (9)
```

The common-scale-free signed coordinates

```text
r = R/Omega,  a = A/Omega,  m = M_signed/Omega
```

obey

```text
r-a-m=1.                                             (10)
```

They are not barycentric weights: `m` may have either sign, and `r,a,m` may be arbitrarily large
through Lorentzian cancellations.

## 4. Covariance and scaling

Under the split-preserving proper frame group

```text
G = SO^+(1,1) x SO(2),
X -> Lambda X,
Y -> Q Y,
```

both matrices in (1) are exactly invariant. `B01`, `B23`, and `M_signed` are invariant under the
proper oriented group; their squares survive orientation reversals as recorded in the atlas.

Under a common rescaling of the two pair tangents,

```text
V_i -> sigma V_i,
```

the matrix channels and `h` scale as `sigma^2`; the bivector, its signed area components, and
`Omega` scale as `sigma^2` and `sigma^4`, respectively. Therefore `(r,a,m)` is common-scale
neutral as an algebraic diagnostic even though strong local CSN is inactive and `kappa` remains
physical pair-state data.

Under a general change of pair coordinates `V -> V C`, both matrix channels transform by
congruence, while `R,A,M_signed,Omega` scale by `det(C)^2`. Hence `(r,a,m)` also describes the
oriented pair plane independently of its coordinate-area normalization. The calibrated pair-state
variables `(kappa,phi,beta)` retain the ordered observer query and are not erased by this plane
atlas.

## 5. Exact modulation of the banked pair state

On (4), the already-banked regular coordinates are

```text
kappa    = (1/4) log[-det(h)],
phi_pair = (1/4) log[(-det(h))/h00^2],
beta     = h01/h00.                                  (11)
```

Hold `H_R` fixed and vary the full angular orchestra by a symmetric `dH_A`. Since `h=H_R+H_A`,
exact differentiation gives

```text
d kappa = (1/4) tr(h^-1 dH_A),                       (12)

d phi_pair
  = (1/4) tr(h^-1 dH_A) - (1/2) dH_A00/h00,          (13)

d beta
  = (h00 dH_A01 - h01 dH_A00)/h00^2.                (14)
```

Equations (12)-(14) are the requested orchestra effect in exact local form. The angular sector can
change common scale, reciprocal opening, and cone tilt together. Because `H_A=Y^T Y`, its three
entries arise collectively from all active angular components of both pair tangents.

The conditional causal readout remains

```text
c_eff^(pair)/c_E = exp(-2 phi_pair).                 (15)
```

`c_E` calibrates (15); it does not select `H_R`, `H_A`, a positive sector weighting, or a curve
through their solution space.

## 6. Why the intrinsic pair metric alone is insufficient

Take

```text
V_0=e0,                 V_1=e1,
V'_0=cosh(a)e0+sinh(a)e2,  V'_1=e1.
```

Both have

```text
h=h'=diag(-1,+1).
```

The first has

```text
(R,A,M_signed)=(1,0,0),
H_A=0.
```

The second has

```text
(R,A,M_signed)=(cosh(a)^2,0,sinh(a)^2),
H_A=diag(sinh(a)^2,0).
```

Equation (2) still gives `det(h)=-1`. Thus `(kappa,phi,beta)` completely describes the intrinsic
pair metric but does not describe how that pair plane sits relative to a fixed reciprocal/angular
split. This does not add a new terminal scalar to the reciprocal readout; it exposes additional
split-relative geometric state upstream.

## 7. Full signed region and boundary strata

For `R>0` and `A>0`, every real `M_signed` has a simple-bivector witness. Choose

```text
B01=sqrt(R),  B23=sqrt(A),
B02=p,        B13=sqrt(RA)/p,
B03=B12=0,
```

with

```text
p^2 = [-M_signed + sqrt(M_signed^2+4RA)]/2.           (16)
```

Then (5) holds and the mixed norm is exactly `M_signed`. The Lorentzian subset is precisely

```text
M_signed < R-A.                                      (17)
```

The deterministic atlas supplies 27 witnesses throughout this open region. Cases `RA=0` are
realized by rank-one mixed matrices and include pure reciprocal, pure mixed, reciprocal-area-zero,
null, and rank-loss examples. No physical regime label is attached to any stratum.

## 8. No unique positive instrument weighting

The mixed channels transform as two copies of the standard `SO^+(1,1)` doublet. If a symmetric
quadratic form

```text
Q=[[a,b],[b,d]]
```

were positive definite and boost invariant, infinitesimal invariance with
`K=[[0,1],[1,0]]` would require

```text
K^T Q+QK=0  =>  b=0, d=-a.
```

Its determinant is `-a^2`, so it cannot be positive definite unless it is the zero form. More
generally, the exact invariant data permit infinitely many positive diagnostics, for example

```text
Q_lambda=sqrt(M_signed^2+lambda(R+A)^2), lambda>0.   (18)
```

Different `lambda` give different normalized positive triples while respecting the same
split-frame covariance and common scaling. No active metric premise selects `lambda`. Absolute
values produce still more conventions and are nonsmooth at zero.

Therefore the signed atlas is derived in its bounded arena, while a positive scalar mixing law is
`OPEN`.

## 9. What a time-live regime law would be

A time-live or scale-live solution is a curve

```text
s -> (H_R(s),H_A(s))
```

inside the allowed matrix cone, or equivalently a complete Jacobian curve `V(s)`. Equations
(1)-(18) determine its admissible state space and exact readouts. They do not determine its tangent
`dH_R/ds,dH_A/ds`. That requires the still-unowned physical pair-family construction, an on-shell
equation, or a global-completion/bootstrap rule.

Consequently it is mathematically reasonable that different sectors contribute differently in
different regimes. What is now derived is the native stage on which that can happen and the exact
way angular data modulate the pair state. What is not yet derived is which physical trajectory the
universe follows across that stage.

## 10. Status ledger

- `DERIVED`, conditional pointwise arena: equations (1)-(14), split-frame covariance, generic orbit
  completeness, the signed solution region, and boundary identities.
- `BANKED CONDITIONAL`: equation (15), inherited from the calibrated pair metric.
- `OBSERVED and independently reproduced`: 27 constructive region witnesses, 600 exact random
  pair checks, 200 exact split-covariance checks, and five boundary witnesses.
- `CONDITIONAL`: ownership and universality of the reciprocal/angular split.
- `OPEN`: positive instrument weights, time-live/on-shell evolution, global branch selection,
  background-density dependence, and physical regime assignments.
- `NOT CLAIMED`: action, source, matter, carrier, `X_max` value, CMB spectrum, or signalling law.
