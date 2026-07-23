# Invariant-Xmax asymptotic-boundary audit

Date: 2026-07-23

Base/preregistration commit:
`4b85bb2d4b17f146585b3f32d9f0f570f9966492`

## Result

Charles's proposed analogy is coherent and improves the boundary picture:

> One universal, unattainable `Xmax` may consistently be treated as UDT's
> positional limiting scale for ordinary observational frames, analogous in
> role—but not physical dimension—to Einsteinian `c`.

This is retained as an owner-proposed `WORKING POSIT`, not a derived value or
canon statement.

The important correction is that an unattainable invariant scale should not
be represented by two regular physical seals. In the declared observer
actions, `+Xmax` and `-Xmax` are excluded directional limits of an oriented
comparison chart. Physical radial separation is nonnegative. On each
oriented ray there is one asymptotic outer limit; how the angular directions
complete or identify globally remains open.

The invariant bound does **not** uniquely derive

```text
X/Xmax = tanh(phi).
```

Nor does it fix the reciprocal/angular normalization `lambda=1`.

Grade: `VERIFIED-WITH-CAVEATS`.

## Complete declared observer-action classification

Let `xi` be an oriented comparison coordinate with `-1<xi<1`. Every smooth,
effective, complete, transitive, orientation-preserving one-parameter action
in the declared class has a flow coordinate `u` in the real line and can be
written

```text
T_beta(xi) = H(H^-1(xi)-beta),
```

where `H:R -> (-1,1)` is an arbitrary smooth increasing bijection.

Conversely, every such `H` defines an exact group action preserving the same
unattainable endpoints. Reversal is obtained with odd `H`.

The statement follows by integrating the nonvanishing complete generator
`v(xi)`:

```text
u = integral dxi/v(xi).
```

Completeness makes both boundary integrals diverge and maps the orbit to the
whole real line. Translation in `u` then gives the displayed action.

This classification is complete for the preregistered one-dimensional
class. It is not a classification of every multidimensional action on an
arbitrary bounded universe.

## Why the bound does not select `tanh`

The following compactifications all have the same open endpoints, reversal,
group structure, neutral point, and unit slope at the neutral point:

```text
H_1(u) = tanh(u),
H_2(u) = u/sqrt(1+u^2),
H_3(u) = (2/pi) atan(pi u/2),
H_epsilon(u)
  = g_epsilon(tanh u),
g_epsilon(x)
  = x + epsilon x^3(1-x^2).
```

For `-1<epsilon<1/2`, the final family is monotone; `epsilon=1/4` is the
exercised exact witness. It is locally calibrated identically to `tanh` but
does not obey the Möbius formula in its displayed coordinate. The
independent exact mismatch is

```text
-38126034/5941291307.
```

Thus invariant `Xmax`, observer composition, reversal, smoothness, and local
calibration do not select the markings inside the interval.

## Where `tanh` is unique

The reciprocal-c pair and CSN supply the positive projective ray

```text
[u:v] = [exp(-phi):exp(+phi)],
r = v/u = exp(2phi).
```

Inside the class of first-degree fractional-linear readouts, requiring

```text
F(0)=-1, F(1)=0, F(infinity)=+1
```

uniquely gives

```text
F(r)=(r-1)/(r+1)=tanh(phi).
```

This theorem remains exact. Its status is
`DERIVED_CONDITIONAL_ON_FIRST_DEGREE_PROJECTIVE_READOUT`. The unresolved
statement is operational:

> Physical positional reach is the first-degree anchored projective readout
> of the reciprocal CSN ray.

The `c` analogy makes that premise intelligible, but does not logically
supply it. In SR, the invariant speed is accompanied by a specific linear
action on spacetime. UDT would analogously need the complete metric to make
this projective ray the operational position observable.

## What the recorded metric actually distinguishes

The recorded conditional WR-L representative has

```text
A = 1-r/X = exp(-2phi),
ds^2 = -A c_E^2 dt^2 + A^-1 dr^2 + angular.
```

It gives three exact, inequivalent radial readings:

```text
coordinate reach: r/X       = 1-exp(-2phi),  maximum X;
proper reach:     ell/(2X)  = 1-exp(-phi),   maximum 2X;
optical depth:    r_*/(2X)  = phi,           unbounded.
```

The temporal coframe factor `exp(-phi)` tends to zero. The boundary has
finite recorded curvature invariants and infinite optical depth. That is
the strongest existing metric realization of the proposed c-like
unattainability:

- finite coordinate room;
- finite proper room;
- vanishing static clock factor; and
- infinite additive/optical depth.

At `phi=log(2)`:

```text
projective tanh display = 3/5,
WR-L coordinate fraction = 3/4,
WR-L proper fraction = 1/2.
```

All approach the same normalized outer limit, but disagree in the interior.
Consequently the phrase “`Xmax` is distance” still requires an operational
choice: coordinate reach, proper path length, projective display, or another
metric observable. The WR-L wall is not yet derived to be the global
terminal `Xmax`.

## Why complete-coframe covariance does not choose the display

For any monotone display

```text
X = Xmax H(phi),
dX = Xmax H'(phi)dphi,
```

the exact coframe and metric relations are

```text
L dphi = L dX/[Xmax H'(phi)],

Q(phi)dphi^2
 = Q(phi)dX^2/[Xmax^2 H'(phi)^2].
```

Keeping the Jacobian gives the same geometry. The conditional full-frame
result therefore selects additive `dphi` in its declared coframe class, but
cannot select which bounded coordinate is painted over it.

Metric regularity can select an operational quantity after its definition
is given. It cannot select a coordinate chart merely because the chart has
a finite endpoint.

## One asymptotic boundary and `lambda`

The parent conditional constant-source flow is

```text
B_phi+B^2-lambda^2 I=0,
t=tanh(lambda Delta_phi).
```

Its exact area and shape diagnostics are

```text
A_rel =
  lambda t (lambda^2-s^2)/(lambda^2-s^2 t^2),

S_shape =
  lambda^4 s^2 (1-t^2)^2/(lambda^2-s^2 t^2)^2.
```

For `0<=s<lambda`, the whole half-flow is nonsingular and approaches

```text
A_rel -> lambda, S_shape -> 0.
```

For `s=lambda`, it instead remains

```text
A_rel=0, S_shape=lambda^2.
```

Merely declaring the outer end unattainable imposes neither behavior and
fixes neither `s` nor `lambda`. If asymptotic area neutrality is added as a
new boundary condition, it selects `s^2=lambda^2`, but still permits every
positive `lambda`. Exact nonunit controls at `lambda=2` and `lambda=3`
survive.

The bounded display `H` never enters the `phi`-normalized transport
equation. Universal `Xmax` therefore does not fix the angular weight unless
the complete metric supplies a new invariant coupling the positional
boundary to angular transport.

## Scale and bootstrap

Once `Xmax` is supplied, the observational anchors form natural scales:

```text
T_scale   = Xmax/c_E,
M_scale   = c_E^2 Xmax/G_obs,
rho_scale = c_E^2/(G_obs Xmax^2).
```

Dimensionless coefficients, total proper mass, realized density, and the
value of `Xmax` remain open. Current bootstrap wording contains no
executable response map or boundary stationarity equation that selects
them—or the dimensionless `lambda`.

## What was learned

The c-like `Xmax` framing is promising in a precise sense:

1. it is compatible with observer reciprocity;
2. it replaces an inappropriate two-regular-seal picture with one
   unattainable radial limit;
3. the WR-L metric already realizes finite room plus infinite depth and
   vanishing clock flow; and
4. it supplies the correct global scale combinations once bootstrap closes.

What remains missing is no longer “does a maximum exist?” for this working
framing. It is:

```text
Which exact metric observable is X/Xmax?
```

If it is the anchored projective reciprocal readout, `tanh` follows. If it
is WR-L coordinate or proper distance, different laws follow. The complete
metric must adjudicate that operational meaning. None of those choices
alone fixes the angular normalization.

## Verification

- preregistered before production algebra: **yes**;
- full space: **complete for the declared smooth one-dimensional action
  class**, bounded controls for metric and angular consequences;
- independent load-bearing implementation: **yes**, standard-library
  rational arithmetic importing no production code;
- premise audit: **yes**;
- production catches: **20/20**;
- independent catches: **20/20**;
- interval-action checks: **13**;
- projective checks: **4**;
- WR-L readout checks: **6**;
- coframe checks: **6**;
- constant-`lambda` checks: **40**;
- source hashes replayed independently: **20**;
- compute: CPU only.

The caveat is the unavailable fresh zero-context semantic verifier:
sub-agent delegation was not authorized for this task. Algebraic
independence is complete; semantic review remains same-context.

No action, carrier, source, mass claim, startup control, canon statement,
GPU solve, or repository reorganization was changed.
