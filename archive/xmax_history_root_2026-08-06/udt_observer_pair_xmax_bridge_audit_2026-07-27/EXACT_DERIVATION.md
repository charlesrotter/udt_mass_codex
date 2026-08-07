# Exact derivation — observer-pair / X_max operational bridge

## 1. Registered stationary comparison metric

Use only the preregistered conditional comparison family

```text
tau = c_E dt + a sigma_3,
g = -exp(-2phi) tau^2 + q,
q = A(sigma_1^2+sigma_2^2)+C sigma_3^2,
A = R^2 exp(2lambda phi),
C = R^2 exp(2phi).
```

The unique timelike Killing line makes `q` an intrinsic metric on the stationary orbit space in
this branch. This does not select stationarity, this topology, or this realization as the physical
UDT universe.

## 2. Killing clock depth

For the registered generator `K=partial_t`,

```text
g(K,K) = -c_E^2 exp(-2phi),
N = sqrt[-g(K,K)] = c_E exp(-phi).
```

Hence

```text
N_B/N_A = exp[-(phi_B-phi_A)].
```

A constant rescaling of `K` multiplies both endpoint lapses and cancels from the ratio. The signed
depth is an endpoint cocycle:

```text
rho_AB = phi_B-phi_A,
rho_AC = rho_AB+rho_BC,
rho_BA = -rho_AB.
```

It is not a symmetric nonnegative distance. Its first variation is the endpoint distribution

```text
delta rho_AB = delta phi(B)-delta phi(A).
```

On a compact smooth comparison configuration it is bounded and attains its extrema. More
importantly, one scalar endpoint difference cannot encode all angular pair geometry on a
centerless three-space, as the earlier exact three-direction result already proves.

## 3. Null-path functional derived directly from the metric

Let a spatial orbit-space path have tangent `v`, and put

```text
ds_q = sqrt[q(v,v)] ds.
```

The null equation, with the future sign chosen by `tau(dot gamma)>0`, is

```text
0 = -exp(-2phi)(c_E dt+a sigma_3)^2 + ds_q^2,
c_E dt = exp(phi) ds_q-a sigma_3.
```

Thus the metric itself derives the directed path functional

```text
F_+(v) = [exp(phi)sqrt(q(v,v))-a sigma_3(v)]/c_E.
```

For the reversed spatial tangent,

```text
F_+(-v) = [exp(phi)sqrt(q(v,v))+a sigma_3(v)]/c_E.
```

Consequently, on the same underlying spatial tangent/path,

```text
[F_+(v)+F_+(-v)]/2 = exp(phi)sqrt(q(v,v))/c_E,
[F_+(v)-F_+(-v)]/2 = -a sigma_3(v)/c_E.
```

The reciprocal/angular sector therefore does not enter as one scalar instrument. The local
reversible norm, and a round trip constrained to retrace the same spatial path, see the full
`phi`-weighted angular metric

```text
exp(2phi) q
= R^2 exp(2(lambda+1)phi) (sigma_1^2+sigma_2^2)
  + R^2 exp(4phi)sigma_3^2,
```

while the orientation-odd part sees the twist connection. Independently minimizing the forward and
reverse directed functionals can select different paths; their optimized sum is not silently
identified with the geodesic distance of this reversible metric.

The functional is positive and strongly convex exactly under the registered strict slice
condition

```text
a^2 < R^2 exp(4phi)
```

pointwise. A time-section change `t'=t+f(x)` adds the exact endpoint term `df` to the directed
functional. Closed-loop data, the reversible round-trip part, and the twist curvature are not
changed by that section shift.

This is a derived geometric null-path/readout object. Under the working co-presence framing, the
extra statement that it is literal physical signal propagation is `OPEN`; the metric algebra does
not settle that ontology.

## 4. Exact angular obstruction to a positive-distance clock/path identity

At a regular point of a three-dimensional orbit space, a nonzero one-form `dphi` has a
two-dimensional kernel. Choose any nonzero tangent `v` in that kernel. Then

```text
dphi(v)=0,
q(v,v)>0,
exp(phi)sqrt(q(v,v))/c_E>0.
```

So the differential clock-depth rate vanishes along a `phi` level while reversible optical length
does not. Closed angular loops give the global version: endpoint depth is zero, positive path
length remains, and twist holonomy can remain nonzero.

Therefore no universal identity can make the signed clock cocycle itself a positive nondegenerate
complete path length across the full angular space. This does not obstruct the signed all-pairs
cocycle as an object. For a supplied physical pair domain,

```text
T_phi(A,B)=phi(B)-phi(A)
```

has linearization `T_h(A,B)=h(B)-h(A)`. Its kernel consists of constant `h`, so on a continuum
domain its image has infinite functional rank modulo constants. A native cocycle-compatible
all-pairs target/equality could therefore become field-valued. None is currently selected.

The obstruction also does not forbid a future coframe-valued or path-family join. It proves that
such a join cannot be obtained by silently setting signed depth equal to positive path length or by
restricting to a preferred radial curve.

## 5. First response of the path functional

For a fixed tangent with

```text
U=sigma_1(v)^2+sigma_2(v)^2,
W=sigma_3(v)^2,
q(v,v)=A U+C W,
```

variation of the reversible numerator with respect to `phi` is

```text
delta_phi[exp(phi)sqrt(q(v,v))]
= exp(phi)[(1+lambda)A U+2C W] delta phi / sqrt(q(v,v)).
```

The two angular sectors have different response weights. At an isolated extremal path, variation
of the optimized path value is the integral of this local response plus the corresponding
variations of the other coframe data. At multiple minimizing paths, the right derivative is the
minimum of those active path responses. A directed-diameter right derivative then takes the
maximum over the active maximizing ordered pairs. The envelope need not be two-sided
differentiable.

This maps a field variation to one path or pair scalar. It is not itself a selected field equation.
An equation would require an active UDT rule fixing a target or equating complete comparison data
for all physical arrows. No such rule is registered.

## 6. Quotient diameter

On smooth compact `S3`, positive `q` gives a continuous geodesic distance. Therefore

```text
D_q = max_{p,r in S3} d_q(p,r)
```

is finite and attained. At a unique regular minimizing geodesic between fixed endpoints, the metric
variation has the familiar exact length-response form

```text
delta d_q = (1/2) integral_gamma delta q(dot gamma,dot gamma) ds_q.
```

For a right metric variation `h`, the exact envelope ordering is

```text
D_q'[h]
= max_(p,r in ArgDiam)
    min_(gamma in Min(p,r))
      (1/2) integral_gamma h(dot gamma,dot gamma) ds_q.
```

It can become nonsmooth when either active set is nonunique. Likewise, the clock-depth range has

```text
Range(phi)'[h]
= max_(Argmax phi) h-min_(Argmin phi) h.
```

`D_q` is therefore an executable branchwise geometric maximum-separation functional. The metric
does not identify it with physical `X_max`, and its attainment does not realize the separate
working asymptotic/unattainability reading.

## 7. Projective display

For supplied signed additive depth `rho` and supplied positive scale `L`,

```text
d = L tanh(rho)
```

has the exact one-dimensional composition law

```text
d_1 plus_L d_2 = (d_1+d_2)/(1+d_1 d_2/L^2)
```

and approaches `+/-L` only as `rho` approaches `+/-infinity`. Its variation is

```text
delta d = tanh(rho) delta L+L sech(rho)^2 delta rho.
```

It does not supply angular composition, a cut-locus rule, `rho`, or `L`. Setting `L=X_max` and then
claiming that the display derived `X_max` is circular.

## 8. Supremum schema and compactness discriminator

The owner type

```text
X_max = sup{D_g(A,B): A,B in O and C_g(A,B)}
```

is exact as a schema. It is not executable until `O`, `C_g`, and `D_g` exist.

For the smooth compact stationary `K`-orbit branch:

- quotient distance has a finite attained maximum;
- smooth endpoint clock depth has a finite attained range;
- the strongly convex directed optical distance is continuous and has a finite attained maximum.

An unattained finite limit therefore requires a different registered global type: an open or
noncompact observer domain, excluded limit points, singular/unbounded profile or weight, a
projective display with independently supplied scale, or another functional not in this frozen
universe. This is a branch discriminator, not a universal no-go.

## 9. Closure ruling

The metric supplies more than a bare diameter: it supplies an exact branchwise directed null-path
geometry coupling clock weighting, angular shape, and twist. It still does not supply the physical
comparison functor that says which observer/event arrows are physical, whether null paths are
signals or readouts, how the founded ruler occupies the complete coframe, or which same-endpoint
paths are identified.

No active premise supplies a cocycle-compatible all-pairs target or equates the clock cocycle, the
directed path functional, the quotient diameter, or the projective display for every physical
arrow. Hence no field-valued global-to-local return equation is selected in this frozen census.
The infinite-rank all-pairs clock map shows that such an equation is not ruled out. Bootstrap
remains `WORKING_ON_SHELL_ADMISSIBILITY_ONLY`.
