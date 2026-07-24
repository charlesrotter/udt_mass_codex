# Exact observer-pair clock-operator derivation

## 1. The founding ordered-pair operator is already present

The current C0/C1 foundation starts with the dimension-matched reciprocal
conversion pair and the positive comparison

```text
S(delta)=diag(u(delta),v(delta)).
```

Dual UDT Reciprocity gives

```text
S(delta)^T K S(delta)=K,
K=[[0,1],[1,0]],
```

and therefore `u v=1`. Difference, regular additive composition, reversal,
and the registered sign/unit convention give

```text
S(delta)=diag(exp(-delta),exp(delta)),
S(delta1)S(delta2)=S(delta1+delta2),
S(-delta)=S(delta)^-1.
```

This is the abstract ordered reciprocal comparison operator. It is not a new
ansatz and does not require selecting a metric path once `delta` is supplied.

The status is:

```text
DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS.
```

The stamps are the named Reciprocal-c channels, dual Reciprocity, regular
composition, nontriviality for the realized universe, and the chosen
sign/unit of depth.

## 2. The same operator is exactly a boost in the balanced basis

With

```text
H=(1/sqrt(2))[[1,1],[1,-1]],
```

the dual pairing becomes

```text
H^T K H=diag(1,-1).
```

The comparison becomes

```text
H^T S(delta) H
 =[[ cosh(delta),-sinh(delta)],
   [-sinh(delta), cosh(delta)]].
```

It has determinant one, preserves `diag(1,-1)`, composes by addition, and
reverses by inversion. Thus the founding reciprocal comparison is
algebraically an exact `O(1,1)` boost after the balanced change of basis.

This does not silently make `K` the physical observer interval. The current
foundation first registers `K` as a faithful dual-evaluation pairing. Using
the balanced timelike axis as the physical observer clock is a distinct
readout premise.

## 3. Channel character and observer invariant are different objects

The named time-per-length channel remains

```text
T(rho)=exp(-rho),  rho>=0,
```

with

```text
T(rho1+rho2)=T(rho1)T(rho2).
```

The reversal-even half trace is instead

```text
Gamma(delta)=Tr S(delta)/2=cosh(delta).
```

It obeys

```text
Gamma(-delta)=Gamma(delta),
```

but it is not a character. At `delta=log 2`,

```text
Gamma(2 delta)-Gamma(delta)^2=9/16.
```

Therefore `sech(delta)` cannot replace the named exponential clock channel.
It may be interpreted as a reciprocal observer slow factor only if the
balanced `K` readout and endpoint observer frames are physically supplied.
That interpretation is `CONDITIONAL`, not a second channel derivation.

This resolves an apparent contradiction in the prior record:

- the exponential is the multiplicative weight on the named clock channel;
- `cosh` or `sech` is a possible reversal-even scalar extracted from the
  complete operator;
- a scalar extracted from an operator need not itself compose as a channel.

## 4. Endpoint local-field realization is an exact identity with an open join

If a common reciprocal section

```text
S(p)=S(phi(p))
```

is supplied, then

```text
U_phi(p,q)=S(p)^-1 S(q)
          =S(phi(q)-phi(p)).
```

It obeys exact reversal and composition:

```text
U_phi(p,q)U_phi(q,r)=U_phi(p,r).
```

The algebra is derived. Its physical use remains conditional because the
current ontology ledger explicitly marks

```text
delta(p,q)=phi(q)-phi(p)
```

as `OPEN_RELATION`. The founding additive depth and the signed local field
are both present, but their global observer map has not been identified.

The factorized formula also presupposes a common trivialization and a flat,
path-independent reciprocal section. Generic complete-metric holonomy need
not admit that factorization globally.

## 5. Exact metric-transport control

Use the supplied static diagonal reciprocal metric

```text
ds^2=-c^2 exp(-2phi(x))dt^2+exp(2phi(x))dx^2.
```

Its nonzero Christoffel symbols in the `(t,x)` chart are

```text
Gamma^t_tx=Gamma^t_xt=-phi',
Gamma^x_tt=-c^2 phi' exp(-4phi),
Gamma^x_xx=+phi'.
```

Along a `t=constant` spatial comparison curve from `p` to `q`, coordinate
vector transport is

```text
V(p->q)=diag(exp(Delta phi),exp(-Delta phi))
       =S(-Delta phi),
```

while coordinate covector transport is

```text
C(p->q)=diag(exp(-Delta phi),exp(Delta phi))
       =S(Delta phi).
```

The second equality is a genuine type-matched realization of the founding
matrix in this exact control: the founding object acts on the reciprocal
coframe/covector pair.

But the physical orthonormal coframe is

```text
theta^0=c exp(-phi)dt,
theta^1=exp(phi)dx.
```

Transporting `theta(p)` with `C(p->q)` gives exactly `theta(q)`. Equivalently,
the orthonormal spin connection has no pullback along the spatial curve.
The relative orthonormal-frame transformation on that curve is therefore
the identity.

This is the decisive type distinction:

```text
coordinate covector scaling = reciprocal matrix;
physical orthonormal spatial-frame boost = identity.
```

Consequently the coordinate match does not by itself prove that two
observers mutually measure clock slowdown.

## 6. The stationary lapse ratio is another separate readout

For static coordinate observers using one supplied stationary slicing,

```text
d tau=exp(-phi)dt
```

gives

```text
d tau_q/d tau_p=exp(-(phi_q-phi_p)).
```

This is the named temporal entry of the endpoint matrix. It reverses to its
inverse when `p` and `q` are swapped. It is an ordered lapse ratio relative
to a common slicing, not a mutual symmetric slowdown. A mutual frame
statement requires the observer/event-pairing structure that produces the
reversal-even readout.

## 7. Endpoint-frame covariance gate

A path transporter represented in endpoint frames transforms as

```text
U -> Lambda_q U Lambda_p^-1.
```

Its trace is invariant under a common conjugation `Lambda_p=Lambda_q`, but
not under independent endpoint refactorizations. Even `U=I` becomes

```text
Lambda_q Lambda_p^-1
```

and has half trace `cosh(beta_q-beta_p)` for independent balanced boosts.

Therefore the half trace is a physical pair scalar only after the endpoint
observer frames are physically specified or a genuinely gauge-invariant
construction is supplied.

## 8. Correct role of paths

A path is not required for the abstract `S(delta)` operator. Paths enter
when the complete geometry must provide:

1. the additive depth assigned to an actual observer pair;
2. the complete angular/shift transport;
3. a comparison through regions with curvature or holonomy; and
4. a rule at multiple minimizing paths or a cut locus.

For each supplied metric and path, Levi-Civita transport exists and reversal
gives the inverse. Current UDT does not yet identify that full transporter
with the founding scalar reciprocal comparison or select a global
path-independent projection.

## 9. Exact status

Derived with explicit founding stamps:

- the ordered reciprocal operator;
- its determinant, composition, and inverse;
- its exact balanced `O(1,1)` boost form;
- the named exponential temporal channel;
- the reversal-even half-trace diagnostic;
- the endpoint-field factorization as an algebraic identity;
- coordinate vector/covector and orthonormal transport in the exact static
  control.

Conditional or open:

- identifying pair depth with a local-field difference;
- treating `K` as the physical observer interval;
- choosing physical endpoint observer frames and event pairing;
- extracting a unique mutual clock scalar;
- extending the reciprocal sector through the complete angular/shift
  geometry;
- path independence and cut-locus adjudication;
- physical `X_max`, mass response, density, or CMB interpretation.

The missing object has therefore become smaller:

```text
not the abstract clock/ruler comparison operator,
but the metric-native realization that assigns its depth and physical
observer readout to a complete global pair.
```
