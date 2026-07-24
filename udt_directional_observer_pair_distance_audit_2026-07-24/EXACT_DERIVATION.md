# Exact directional observer-pair derivation

## 1. No-center definitions

For a supplied complete observer-rest spatial metric `h`, the physical
distance object is

```text
d_h(p,q)=infimum of h-lengths from observer p to observer q.
```

For unit `n` in the observer's tangent space,

```text
X(p,n)=the distance at which exp_p(s n) first ceases to minimize.
```

Then

```text
E(p)=sup_q d_h(p,q)=sup_n X(p,n),
diam(Sigma,h)=sup_p E(p)=sup_(p,q)d_h(p,q).
```

There is no universal center in any of these definitions. A coordinate chart
may be based at any observer without turning that observer into an origin of
the universe.

The global scalar `X_max` is the final supremum. Directional variation, if
present, belongs to `X(p,n)`.

## 2. Complete source census

All 12 finite-cell completion rows and all 28 equation/evidence families
were screened exactly once.

- The 12 FC rows are topology/completion types or an open profile; none
  supplies a complete metric profile and observer pairing.
- `B19` supplies the one observed complete on-shell conditional spatial
  metric: round `S3_b`.
- `B21` supplies the local WR-L clock-depth profile, but not a complete
  global spatial geometry.
- No other equation family supplies a complete on-shell pair-distance
  witness.
- The preceding clock/angular audit supplies no regular complete
  clock-soldered two-cap witness.

The conditional stationary ansatz also supplies a complete nonround
constant-squashing `S3` metric as an off-shell configuration. The correction
registered before banking therefore distinguishes complete metric
configuration, complete on-shell branch, and complete clock-soldered physical
branch.

## 3. Exact round result

Embed the round spatial metric as

```text
S3_b={Z in R4: Z dot Z=b^2}.
```

For any observers `p,q`,

```text
d_h(p,q)=b arccos[(p dot q)/b^2].
```

Given any unit tangent direction `n` at any observer `p`, the unit-speed
geodesic is

```text
gamma(s)=cos(s/b)p+b sin(s/b)n.
```

At `s=pi b`,

```text
gamma(pi b)=-p,
```

independent of `n`. This is the antipodal cut point. Therefore

```text
X(p,n)=pi b,
E(p)=pi b,
diam(S3_b)=pi b,
Delta_X(p)=0.
```

These values do not depend on the observer. The transitive round isometry
group proves observer equivalence; no point is a center.

The prior reciprocal-depth calculation

```text
D(neutral Clifford torus, cap)=pi b/4
```

is a chart/foliation segment. It is one quarter of the full pair diameter,
not `X_max`.

## 4. Complete squashed off-shell control

The registered conditional stationary coframe contains

```text
h_sigma=b^2[e1^2+e2^2+sigma^2 alpha^2],  sigma>0,

e1=d eta,
e2=sin(eta)cos(eta)(d xi1-d xi2),
alpha=cos(eta)^2 d xi1+sin(eta)^2 d xi2.
```

Its coordinate determinant is

```text
det h_sigma
 =b^6 sigma^2 sin(eta)^2 cos(eta)^2.
```

The apparent endpoint zeros are the ordinary primitive-circle coordinate
collapses; the metric is smooth and positive for every `sigma>0`. At
`sigma=1` it is exactly round.

Equivalently,

```text
h_sigma=b^2[h_round+(sigma^2-1)alpha^2].
```

The unitary action on the embedded `S3` preserves both `h_round` and the Hopf
one-form `alpha`, and acts transitively. Thus every point remains equivalent:
the squashing introduces no privileged center.

It does introduce a distinguished direction family. The exact metric energy
is

```text
|v|^2/b^2
 =eta_dot^2
 +sin(eta)^2cos(eta)^2(xi1_dot-xi2_dot)^2
 +sigma^2[cos(eta)^2xi1_dot+sin(eta)^2xi2_dot]^2.
```

Two exact closed geodesics are:

```text
Hopf fiber:      xi1_dot=xi2_dot, length=2 pi b sigma;
horizontal loop: alpha(v)=0,       length=2 pi b.
```

Their half paths both connect `p` to `-p`, giving the exact bound

```text
d(p,-p) <= pi b min(sigma,1).
```

This proves global angular length sensitivity while retaining no privileged
point. It does not by itself give the cut time along every direction, the
injectivity radius, or the diameter. Those require the full geodesic/cut
locus.

The squashed family is an off-shell metric control. The bounded conditional
`C^2` solve observed only the round root among its certified roots, with
unresolved basins retained. The control is neither selected UDT geometry nor
a physical prediction.

## 5. Which changes can affect the directional band

- coordinate changes: cannot affect it;
- orthonormal coframe rotations that leave `h` fixed: cannot affect it;
- round axis exchange: cannot affect it;
- constant scale `b`: multiplies every distance and leaves the round
  fractional spread zero;
- physical Hopf-fiber squashing: changes exact global loop lengths and may
  change the cut-distance band;
- general nonconstant angular profiles: can change distances, but require a
  complete regular metric and cut-locus solution;
- a topology or quotient label without metric, lattice, scale, and pairing:
  determines no distance.

## 6. Physical `X_max` gate

The two strongest branches remain complementary:

| gate | round B19 | WR-L |
|---|---|---|
| complete spatial metric | yes, conditionally | no |
| no-center pair distance | yes | not globally evaluable |
| observer equivalence | yes by round isometry | not globally derived |
| founding clock solder | no; constant lapse | yes locally |
| infinite dilation at pair diameter | no | no global diameter |

No branch passes the complete physical gate.

Therefore:

```text
round geometric diameter = pi b      DERIVED_CONDITIONAL
round directional spread = 0         DERIVED_CONDITIONAL
nonround off-shell loop anisotropy    DERIVED_CONTROL
nonround exact cut-distance band      OPEN
physical UDT X_max                    OPEN_NOT_EVALUABLE
```
