# Exact and numerical derivation — intrinsic-to-optical transport

## 1. Metric and transported frame

The calculation uses the frozen quaternion/Maurer–Cartan coframe in all six C01–C06 candidates.
At each preregistered event, the initial transported tetrad is the local intrinsic frame

```text
(U,N,S2,S3)=(E0,E1,E2,E3),
```

and the two launch directions are `k=E0+E1` and `k=E0-E1`.  The tetrad is parallel transported
along the affine null geodesic.  Its screen columns remain an orthonormal optical screen by metric
compatibility; they need not remain equal to the endpoint's locally reconstructed intrinsic screen.

The production geometry uses the exact anholonomic structure coefficients of the coframe, the
Koszul connection, and complex-step derivatives of that connection.  The Riemann tensor is

```text
R^a_bcd = E_c(Gamma^a_db)-E_d(Gamma^a_cb)
          +Gamma^e_db Gamma^a_ce-Gamma^e_cb Gamma^a_de
          -C^e_cd Gamma^a_eb.
```

An independently written coordinate-metric/autodiff implementation transforms its coordinate
Riemann tensor into the orthonormal frame.  All 144 checkpoint tensors agree with maximum scaled
error `2.114538917956446e-10`.

## 2. Exact local connection anchor

At P00, the frozen profile gives

```text
(E1 phi,E2 phi,E3 phi)=(3/50,1/50,2/50).
```

The parent Cartan theorem says

```text
nabla_(E0 plus_or_minus E1)(E0 plus_or_minus E1)
  = longitudinal -2(E2 phi)E2-2(E3 phi)E3.
```

An affine geodesic initially tangent to that local null field must therefore acquire frame-component
slopes

```text
dv2/ds=2/50=0.04,
dv3/ds=4/50=0.08.
```

The production right-hand side reproduces those values with zero stored floating discrepancy for
all six `lambda` values.  This independently anchors the sign and the meaning of the observed
screen leakage.

## 3. Full Jacobi transport

The parallel screen defines

```text
F_AB=g(S_A,R(k,S_B)k).
```

The integrated first-order system is

```text
dM/ds = [[0,I],[F,0]]M,
M(0)=I.
```

`F` is symmetric to a maximum residual `3.438948431577771e-10`.  Consequently the saved full
propagators remain symplectic: maximum residual `7.529826947025403e-11`, maximum `|det M-1|`
`6.661338147750939e-16`, and direct-versus-two-half composition error
`4.996003610813204e-16`.

The vertex block `B=M[:2,2:]` has positive determinant at every one of the 144 checkpoints:

```text
min det B = 0.003898252561966846,
max det B = 0.061842552692987725.
```

Thus no sampled short segment reaches a projected caustic.  This says nothing about longer paths or
the complete cut locus.

## 4. Connection-induced screen mixing

The orientation-independent screen leakage is

```text
sum over A=2,3 of [g(S_A,u)^2+g(S_A,n)^2].
```

It vanishes exactly when the transported optical screen equals the local intrinsic screen.  Every
one of the 36 endpoints is positive:

```text
minimum = 0.00016557276449080205,
maximum = 0.006112492570157176.
```

The corresponding transported-pair leakage ranges from `0.00016251144641506274` to
`0.006251153977065438`.  These values realize the exact parent obstruction: nontrivial depth in the
twisted contact geometry produces actual pathwise clock/ruler/screen mixing.  Their magnitudes are
dimensionless configuration diagnostics, not energies or observed effects.

## 5. Clock law and numerical certification

For every path and checkpoint,

```text
Q=omega(s)/omega(0)=exp[phi(s)-phi(0)]
```

holds with maximum residual `6.661338147750939e-16`.  The maximum relative Killing-energy drift is
also `6.661338147750939e-16`.  Other maxima are:

```text
null                         2.0928354535487692e-15,
screen Gram                  1.4432899320127035e-15,
k-screen                     6.938893903907228e-17,
fine/coarse endpoint state   1.1102230246251565e-15.
```

All are far inside the preregistered gates.  The six independent fixed-step RK4 endpoints agree
with DOP853 to `2.9620750296999176e-13` maximum absolute difference.

## 6. WR-L readout comparison

Across the atlas,

```text
D_A(L) ranges 0.24545722715760046 to 0.2486816291827519,
W(L)=abs[1-exp(-2 Delta phi)] ranges 0.009430374794554108 to 0.05640878922911219.
```

The raw scales are not physically comparable because this off-shell family retains `R=1` and no
macro branch calibration.  The preregistered endpoint-normalized four-checkpoint shape RMS ranges
from `0.024381290173091336` to `0.13924125182995242`; no path gives equality.

The apparent best sampled `lambda` is not consistent across path direction:

```text
lambda=+2 has the smallest shape RMS in four event-direction groups,
lambda=-2 has the smallest shape RMS in two event-direction groups.
```

Both are endpoints of the sampled `lambda` set, so the atlas does not even exhibit a bounded
interior optimum.  No `lambda` is selected.

For `lambda=-2`,

```text
abs[1-exp(lambda Delta phi)] = W
```

at all 24 associated checkpoints with zero stored discrepancy.  This is the preregistered algebraic
tautology.  It does not make the independently integrated `D_A` equal to `W` and therefore supplies
no SNe derivation.

## 7. Exact status boundary

Derived exactly:

- the local connection anchor;
- the metric endpoint clock law in these stationary branches; and
- the geometric definitions and conservation identities used by the transport.

Observed and independently certified in the bounded atlas:

- nonzero screen mixing on all 36 sampled paths;
- smooth, noncaustic short-path Jacobi transport;
- path-dependent optical readouts and conflicting `lambda` shape rankings.

Not derived: an on-shell profile, physical path ensemble, global holonomy reduction, physical
`lambda`, SNe prediction, action, source, carrier, boundary, density/bootstrap closure, mass,
`X_max`, dynamics, or operational signalling.
