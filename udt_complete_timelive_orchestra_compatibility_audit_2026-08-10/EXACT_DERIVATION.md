# Exact derivation — complete time-live orchestra compatibility

Date: 2026-08-10

Mode: metric-led, exact analytic/CPU

Preregistration commit: `c86094e1`

Pre-review grade: `VERIFIED-LEAD`

## 1. Result first

The complete pair-adapted coframe has an exact time-live compatibility orchestra, but the currently
owned metric kinematics does not select its music.

The preregistered landing is

```text
EXACT_COMPATIBILITY_ORCHESTRA_BUT_NO_EVOLUTION_LAW.
```

All common-scale, reciprocal, shift, angular-screen, and mixing fields can vary arbitrarily in
time. When they also vary in space, their time and spatial derivatives obey three exact coupled
Maurer–Cartan block identities. The mixing identity contains both reciprocal and angular
connections and is the first clean differential expression of the G59 orchestra. Nevertheless,
every smooth full-rank coframe movie satisfies these identities automatically. Conversely, on a
simply connected local domain the flat compatibility data reconstructs a coframe up to an initial
constant.

Thus current geometry supplies the instrument wiring and lawful smooth-film condition. It supplies
no frequency, phase relation, dispersion relation, characteristic operator, physical trajectory,
or regime map.

## 2. Complete live coframe

Use a regular pair-adapted chart with

```text
E = [[B,   0],
     [Q S, Q]],                                      (1)

B = [[T, T beta],
     [0, L]],

T=exp(kappa-phi),  L=exp(kappa+phi).
```

`B` retains the complete regular pair metric state: common scale `kappa`, reciprocal depth `phi`,
and shift `beta`. `Q` is a general invertible `2 x 2` angular coframe and `S` is a general `2 x 2`
mixing field. Every entry may depend on time and all spatial coordinates. The founded reciprocal
block is recovered at `kappa=beta=0`; it is not used to freeze the complete chart.

The inverse is exact:

```text
E^-1 = [[B^-1,       0],
        [-S B^-1, Q^-1]].                            (2)
```

This chart is conditional on a supplied regular reciprocal/angular split. It is not claimed to be
one universal global coframe section.

Within that regular split it is a complete metric chart. `B` has three entries, `S` has four, and
`Q` has four; the left `O(2)` presentation freedom of `Q` removes one, leaving all ten independent
metric components. Exact multiplication gives

```text
g_base   =B^T eta_(1,1) B+S^T Q^T Q S,
g_cross  =S^T Q^T Q,
g_screen =Q^T Q.                                     (2a)
```

Conversely, a regular metric with positive screen block and Lorentzian base Schur complement has
this local block factorization. Thus the chart does not obtain its result by silently deleting a
metric amplitude; its limitation is the declared regular split and chart domain.

## 3. The three differential instruments

Define the right logarithmic coframe derivative

```text
K=dE E^-1.
```

Direct multiplication of (1)--(2) gives

```text
K = [[P, 0],
     [C, R]],                                        (3)

P=dB B^-1,
R=dQ Q^-1,
C=Q dS B^-1.                                        (4)
```

The cancellation of the two `dQ S` terms in `C` is exact. The base block is

```text
P = [[d kappa-d phi, exp(-2phi)d beta],
     [0,             d kappa+d phi]].                (5)
```

Equation (5) shows why a time-live reciprocal channel cannot be studied honestly with common scale
or shift frozen. The off-diagonal shift derivative is itself modulated by reciprocal depth.

`R` contains angular scale, shear, and frame rotation. `C` contains all four mixing derivatives,
dressed on the left by the live screen and on the right by the live pair block. These are matrix
channels, not positive scalar importance weights.

## 4. Exact time–space harmony

For a right logarithmic derivative the Maurer–Cartan identity has sign

```text
dK-K wedge K=0.                                      (6)
```

Splitting (6) by blocks gives

```text
dP-P wedge P=0,                                      (7)
dR-R wedge R=0,                                      (8)
dC-C wedge P-R wedge C=0.                            (9)
```

For time `t` and any spatial direction `i`, these are

```text
partial_t P_i-partial_i P_t-[P_t,P_i]=0,             (10)

partial_t R_i-partial_i R_t-[R_t,R_i]=0,             (11)

partial_t C_i-partial_i C_t
 -(C_t P_i-C_i P_t+R_t C_i-R_i C_t)=0.               (12)
```

Equation (12) is the exact differential orchestra joint. Mixing cannot change independently of
the reciprocal/common/shift connection `P` and the angular connection `R` while remaining the
derivative of one smooth complete coframe.

The production controller verifies (10)--(12) on a fully nonconstant exact time–space witness with
all blocks active. The independent implementation reconstructs all three equations from arbitrary
rational first and commuting mixed-second jets in 300 exact trials.

## 5. Why this is compatibility, not dynamics

For every smooth full-rank matrix field `E(t,x)`, `K=dE E^-1` satisfies (6) identically. The proof
uses only equality of mixed partial derivatives. Conversely, on a simply connected local domain, a
matrix one-form satisfying (6) integrates to `E` after one initial matrix is supplied. This is the
standard local Frobenius reconstruction statement for the declared `GL(4)` chart.

On a time-only base there are no nonzero two-forms, so (6) imposes zero restriction. Therefore

```text
B(t), Q(t), S(t)
```

may be any smooth functions with `det B det Q != 0`. Frequencies and phases remain arbitrary.
Time-live kinematics alone does not produce oscillators or resonances.

The flatness of `K` is not zero spacetime curvature. `K` records the integrability of the coframe
matrix relative to the selected background chart. The Levi-Civita connection and Riemann curvature
also contain the coframe anholonomy and its derivatives. Their Cartan and Bianchi identities remain
geometric identities for every smooth metric; without a response equation they do not select one
history either.

## 6. Evolution of the G59 matrix orchestra

Let the complete pair Jacobian be partitioned as

```text
V=(X;Y),
H_R=X^T eta_(1,1) X,
H_A=Y^T Y,
h=H_R+H_A.
```

The pair query or immersion may itself move relative to the coframe. Write its independent
contribution as `(J_R;J_A)`. Then (3) gives

```text
dot X=P_t X+J_R,
dot Y=C_t X+R_t Y+J_A.                               (13)
```

Thus

```text
dot H_R
 =X^T(P_t^T eta+eta P_t)X
  +J_R^T eta X+X^T eta J_R,                          (14)

dot H_A
 =X^T C_t^T Y+Y^T C_t X
  +Y^T(R_t^T+R_t)Y
  +J_A^T Y+Y^T J_A.                                  (15)
```

Equation (15) is the time-live form of angular/mixing modulation. It contains the complete angular
strain, the reciprocal-to-angular mixing carry, and independent query motion. Setting `J_R=J_A=0`
is a fixed-query control, not a universal physical rule.

The pair-state readouts consequently obey the exact identities

```text
dot kappa_pair=(1/4)tr(h^-1 dot h),                   (16)

dot phi_pair
 =(1/4)tr(h^-1 dot h)-(1/2)dot h00/h00,              (17)

dot beta_pair
 =(h00 dot h01-h01 dot h00)/h00^2.                   (18)
```

These equations say how any supplied movie is read. They do not say which movie occurs.

## 7. Arbitrary-frequency witnesses

Four constructive families remain admissible:

1. arbitrary reciprocal vibration `phi=a sin(omega t)`;
2. independent angular rotation, breathing, and shear frequencies in `Q(t)`;
3. independent finite Fourier sums in all four entries of `S(t)`;
4. fully coupled nonconstant `kappa`, `phi`, `beta`, `Q`, and `S` with unrelated frequencies.

All are smooth full-rank coframe movies on their regular domains. None is an on-shell mode. Their
survival proves that the current identities impose no kinematic frequency selection, resonance,
or dispersion relation.

## 8. Causality and characteristics remain different types

Every regular induced pair metric has its kinematic null cone and the banked conditional readout

```text
c_eff^(pair)/c_E=exp(-2phi_pair).
```

A field characteristic cone, however, is the zero set of the principal symbol of a differential
equation. No native principal differential operator is selected by (6)--(18). Therefore the metric
cone cannot yet be called the propagation cone of a UDT field, and arbitrary time dependence
cannot be called material signalling.

## 9. Scope and next joint

This result is complete for the declared local full-rank factorized chart. It excludes null/rank
loss, chart overlap, cut loci, topology, boundary, and global completion. R17 remains only a
stationary conditional split owner and does not become a universal time-live branch.

The smallest remaining joint is no longer “turn time on.” Time is now fully live. The missing joint
is a native relation that selects a proper subset of these smooth compatible histories. That could
be a local response/evolution law, a global completion condition, or eventually a bootstrap
self-consistency condition. This audit selects none of them.

No action, source, matter, mass, `X_max`, CMB spectrum, physical regime map, signalling law, or
bootstrap theorem is derived.
