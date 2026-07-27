# Exact reduced-holonomy derivation

## 1. Object and variables

For the registered coframe write

```text
dphi=p1 theta1+p2 theta2+p3 theta3
A=a kappa exp[-(1+2lambda)phi]
B=kappa exp[(1-2lambda)phi]
C=kappa exp[-phi]
X_lambda=diag(-1,+1,lambda,lambda).
```

Here `A` carries the clock twist, `B` and `C` carry the angular Maurer–Cartan coupling, and
`kappa=-2`.  At every regular finite point of the `S3` coframe, `B` and `C` are nonzero.

Since `X_lambda` has constant adapted-frame entries,

```text
(nabla_c X)^a_b=Gamma^a_cb(x_b-x_a).
```

The exact Cartan construction has 30 nonzero connection components.  `C` cancels from every
off-eigenspace component of `nabla X`; this does not mean it leaves the connection or curvature.

## 2. Generic angular weight

For `lambda != +/-1`, the full nonzero system contains the decisive factors

```text
2p1,
(lambda+1)p2, (lambda-1)p2,
(lambda+1)p3, (lambda-1)p3,
(lambda+1)A,
(lambda-1)B,
```

plus redundant multiples.  Therefore

```text
nabla X_lambda=0
iff p1=p2=p3=A=B=0.
```

Stationarity and `p1=p2=p3=0` give `dphi=0`.  On regular `S3`, however,

```text
B=kappa exp[(1-2lambda)phi] != 0.
```

Thus no regular generic-`lambda` branch in this family admits the strong intrinsic parallel lift.

## 3. Clock-democratic stratum, lambda=+1

At `lambda=+1`, ruler and screen share the `+1` eigenvalue.  All ruler–screen connection terms now
belong to the stabilizer `so(3)`.  The remaining exact system is

```text
nabla X_+1=0
iff p1=p2=p3=A=0.
```

Hence

```text
phi=phi0 constant,
a=0,
B=C=kappa exp(-phi0) != 0.
```

The surviving metric is

```text
g=-exp(-2phi0)dt^2
  +exp(2phi0)(sigma1^2+sigma2^2+sigma3^2).
```

It is the complete product of a flat time line and round `S3`.  Its only nonzero curvature
endomorphisms are

```text
R_12=(k^2/4)J_12,
R_13=(k^2/4)J_13,
R_23=(k^2/4)J_23,
k=kappa exp(-phi0),
```

so the holonomy algebra is exactly spatial `so(3)` and commutes with
`X_+1=diag(-1,+1,+1,+1)`.

This is a genuine regular complete metric, but it is not a nontrivial reciprocal clock/ruler
completion:

- constant `phi` makes the stationary endpoint clock ratio `Q=1`;
- `a=0` removes the clock twist used to identify the ruler; and
- spatial isotropy makes the former ruler indistinguishable from the screen.

What survives is the clock-versus-all-space grading, not the founded distinguished clock/ruler pair.

## 4. Ruler-democratic stratum, lambda=-1

At `lambda=-1`, clock and screen share eigenvalue `-1`; twist mixing inside that block is allowed.
The full system becomes

```text
nabla X_-1=0
iff p1=p2=p3=B=0.
```

Again `dphi=0`, but now

```text
B=kappa exp(3phi0) != 0
```

on regular `S3`.  Therefore no regular `lambda=-1` strong reduction exists in this family, with or
without clock twist.

## 5. Why B is the decisive angular joint

For a distinguished ruler eigenline, the `S3` Maurer–Cartan structure continually connects that
line to the two-plane.  Algebraically this is the nonzero `B` term.  There are only two ways to hide
it from `nabla X`:

1. set `B=0`, which requires leaving regular finite `S3` geometry (`kappa=0` or a singular limit); or
2. set `lambda=+1`, which puts ruler and screen in the same eigenspace, so the mixing is internal—but
   also removes the distinguished ruler from `X`.

Thus the complete angular sector supplies a sharp metric statement:

> on this regular contact `S3` family, a globally parallel reciprocal grading cannot retain both a
> nontrivial depth and a metric-distinguished ruler.

This is not a claim about every UDT topology or time-dependent coframe.

## 6. Curvature versus parallelism

If `nabla X=0`, then `[R_cd,X]=0` automatically.  The surviving product branch was checked directly
and has exactly the predicted rank-three stabilizer curvature.

The converse was not substituted: pointwise or accidental curvature centralization without
`nabla X=0` does not make the intrinsic field endpoint-independent.  The audit therefore classifies
the strong intrinsic lift, not every accidental curvature-only metric.

## 7. Registered-premise comparison

- Reciprocity supplies the local opposed clock/ruler weights; it does not state `nabla X=0`.
- The regular finite-cell `S3` angular structure supplies `B!=0`, which obstructs a separately
  parallel ruler rather than selecting one.
- The registered seal conditions do not impose `phi=constant` or `a=0`.
- Bootstrap is currently a working on-shell admissibility principle, not a local connection
  equation.
- Strong local CSN is challenged/inactive and cannot be used as a selector.

No current premise selects the sole regular parallel survivor or demands strong endpoint closure.

## 8. Exact boundary

Derived here: the complete necessary-and-sufficient `nabla X=0` conditions in all three eigenvalue
strata of the registered stationary twisted-`S3` coframe, their regularity consequences, and the
survivor's curvature algebra.

Still open: whether the founding observer-frame reciprocity requires a global parallel grading at
all, rather than local Lorentz-equivalent copies and path-groupoid comparison; other coframes and
topologies; time dependence; and all physical selection, action, source, carrier, boundary,
bootstrap realization, density, mass, `X_max`, dynamics, and operational access.
