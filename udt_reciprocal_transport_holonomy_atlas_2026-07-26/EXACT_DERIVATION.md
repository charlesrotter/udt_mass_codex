# Exact derivation

## 1. One path is not the problem

For a supplied complete metric, its Levi-Civita connection gives parallel
transport `U_gamma` along any supplied regular curve `gamma`. Because the
connection is metric compatible, `U_gamma` is a Lorentz isometry. Starting
with

```text
X_lambda=diag(-1,+1,lambda,lambda)
```

in an adapted orthonormal frame, define

```text
X_B=U_gamma X_A U_gamma^-1.
```

Conjugation preserves the characteristic polynomial

```text
(z+1)(z-1)(z-lambda)^2,
```

the causal character of the transported eigenspaces, metric
self-adjointness, and reversal/composition. Thus metric-native pathwise
transport exists for every `lambda`. It requires a complete metric, an
initial lift, and a path; it selects none of them.

## 2. Multiple paths introduce holonomy

If `U_gamma` and `U_sigma` connect the same endpoints, their outputs agree
exactly when the loop map

```text
H=U_sigma^-1 U_gamma
```

satisfies

```text
H X H^-1=X.
```

Therefore an ordinary globally parallel lift exists precisely when the
holonomy group lies in the stabilizer/centralizer of `X`.

In an adapted frame,

```text
nabla X=dX+[omega,X].
```

For constant eigenvalues, connection components joining unequal eigenspaces
must vanish in an `X`-parallel frame. This yields the complete connected
stabilizer atlas:

| Lift | Allowed Lorentz connection algebra |
|---|---|
| generic `lambda` (including zero) | screen `so(2)` only |
| `lambda=+1` | spatial `so(3)` |
| `lambda=-1` | `so(1,2)` on the clock-plus-screen complement |

The founded clock and ruler eigenvalues remain `-1` and `+1`, so a base boost
mixing them never commutes. Full `SO+(1,3)`, `SO+(1,1)xSO(2)`, and the null
stabilizer preserve no member of this regular semisimple family.

This gives three ordinary cases:

- trivial or screen-only holonomy leaves every `lambda` possible;
- full timelike-line `SO(3)` reduction forces `lambda=+1`;
- full spacelike-line `SO+(1,2)` reduction forces `lambda=-1`.

They are properties of supplied holonomy reductions, not a selection of the
physical reduction.

## 3. Reciprocal inversion is a different global question

The prior reciprocal transition algebra contains an inverting map `F` that
swaps the founded clock/ruler pair. Extend it by an arbitrary action on the
two-dimensional screen. For the scalar screen response,

```text
F X_lambda F^-1 + X_lambda
  = diag(0,0,2lambda,2lambda).
```

Hence

```text
F X_lambda F^-1=-X_lambda
```

if and only if `lambda=0`.

This conclusion does not depend on choosing the block swap. Conjugate
matrices have equal trace and characteristic polynomial, whereas

```text
tr(X_lambda)-tr(-X_lambda)=4lambda,
char_X-char_-X=-4lambda z(z-1)(z+1).
```

Thus no invertible change of frame can conjugate `X_lambda` to `-X_lambda`
for nonzero `lambda`.

The finite character confirms the same result. With

```text
D_lambda(phi)=diag(exp(-phi),exp(phi),
                     exp(lambda phi),exp(lambda phi)),
```

the complete inversion identity

```text
F D_lambda(phi) F^-1=D_lambda(-phi)
```

holds for all real `phi` exactly at `lambda=0`. At `phi=0`, every character
is the identity and the test is vacuous; a nonzero-depth stratum is required.

The inverting `F` is not a Lorentz transformation of the diagonal physical
`eta` readout because it swaps a timelike and spacelike line. It belongs to
the reciprocal normalizer. Calling it physical metric holonomy would require
the still-conditional compatible readout/solder. The result is therefore a
twisted reciprocal-bundle theorem, not ordinary Levi-Civita holonomy.

## 4. The three exceptional values have distinct meanings

```text
lambda=+1  clock-democratic 1+3 lift; ordinary timelike-line holonomy
lambda=-1  ruler-democratic 3+1 lift; ordinary spacelike-line holonomy
lambda= 0  spectator screen; odd reciprocal-inversion descent
```

The current premises do not select among these global structures. Their
different answers are not a contradiction; they prove that “transport
consistency” is incomplete until the global object and holonomy class are
specified.

## 5. Why a corrected connection does not select

On a chosen smooth fixed-rank reduction, the recorded Kato correction can
modify the Levi-Civita connection so the chosen spectral projectors are
parallel. The construction starts from the projector it preserves. It
therefore proves existence of a preserving mathematical connection after a
choice, not a native selection of `lambda`, a physical force, or evolution.

## 6. Finite cells

All twelve registered completion families admit pathwise transport on their
regular supplied regions. Ordinary global descent additionally requires
restricted curvature holonomy and every discrete/global monodromy to
centralize `X`. Twisted descent requires an explicit reciprocal grading whose
transitions normalize the line spanned by `X`. Singular, stratified, mirror,
quotient, and nonorientable rows add the exact gates recorded in
`FINITE_CELL_HOLONOMY_CROSS.tsv`.

No row supplies a complete on-shell metric/`phi` field, actual holonomy, and
full reciprocal-angular solder. No row selects a `lambda`.
