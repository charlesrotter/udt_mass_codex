# Exact type and linkage derivation

## 1. Conditional state and readout map

For a registered completion class `FC`, let `X_FC` denote a supplied complete
metric/coframe profile together with every domain, cap, boundary, glue,
lattice, lift, and equivalence datum required by a readout.  The notation

```text
R_geom^FC[X_FC]
```

means a redundant vector assembled from only the components that are defined
on one coherent `X_FC`.  It does not assert that `X_FC` exists in the frozen
registry or that the vector is a physical state.

Every registered class currently fails M02: no complete metric witness is
supplied.  Consequently the matrix can derive component formulas and types,
but it cannot evaluate one complete continuous vector.

## 2. Local and measure channels

R01 is local curvature computed from the complete coframe/metric and its
Levi-Civita connection.  It is tensorial locally but is not a global scalar
readout merely because its formula exists.

For a supplied typed region and representative,

```text
V4[Omega,g] = integral_Omega sqrt(|det g|) d^4x
V3[Sigma,h] = integral_Sigma sqrt(det h) d^3x.
```

Their fixed-domain first variations exist.  A moving seal, cap, glue, corner,
or modulus adds domain/embedding terms; omitting those terms does not define a
complete global response.  R04 is likewise explicitly nonnull/typed boundary,
cap, corner, and joint geometry.  Null and type-changing channels require a
separate protocol.

R05 is not one invariant.  It is an unselected family of integrated curvature
functionals.  The frozen counterfamilies prevent choosing one member merely
because it can be written down.

## 3. Four distinct transport objects

For a supplied path `gamma`, open-path Levi-Civita transport is the endpoint
map

```text
U_gamma = P exp(- integral_gamma Gamma).
```

It transforms with the endpoint frames.  Only on a based closed loop does it
become R07 holonomy; a base-frame change conjugates that loop result, so the
conjugacy data—not the raw matrix—is frame-independent.

For a smooth fixed-rank projector `P(s)`, R08 obeys the Kato equation

```text
dU/ds = [dP/ds, P] U.
```

This is transport in the projector subbundle.  It is neither Levi-Civita
tangent transport nor a loop holonomy unless the additional structures are
supplied.

On a toric region, the angular shift `S` transforms as a `T2` connection and

```text
F = dS
```

is its local curvature (R09).  R10 is the continuous `T2` gauge class obtained
from integrating `S` around a closed base loop with the required lattice
trivialization and global completion lift.  R11 instead records discrete
`GL(2,Z)` monodromy or cap-cycle data.  A supplied character can project `S`
to a circle connection, but that conditional projection is not the full
`T2` holonomy.

## 4. Angular character geometry

For normalized positive angular shape matrix `H` and an integral character
`w`, define

```text
q_w       = w^T H^{-1} w
ell_w     = sqrt(q_w)
systole   = min_{w primitive, w != 0} ell_w
W_min     = argmin_{w primitive, w != 0} ell_w.
```

These four objects are not interchangeable.  On a chamber with fixed `w`,

```text
delta q_w   = -w^T H^{-1} (delta H) H^{-1} w
delta ell_w = delta q_w / (2 ell_w).
```

At a tie, the directional derivative of the minimum uses the minimum of the
active slopes, while `W_min` is a set-valued jump.  Normalized shape values do
not become physical lengths until common angular scale and period data are
supplied.

FC11 has no registered global integral torus lattice.  R09–R12 are therefore
unavailable there.  FC10 retains only a stratum-dependent R11 schema.

## 5. Discrete completion controls

For primitive cap cycles `v_-` and `v_+`,

```text
p = |det(v_-,v_+)|
```

classifies the sampled cap-pair family.  Independent exact arithmetic gives
16 `p=0`, 58 `p=1`, and 182 `p>1` witnesses among the frozen 256 controls.
The integer classifies supplied data; it does not select the cap pair.

Likewise every frozen monodromy control has determinant `+1` or `-1` as
registered.  A `GL(2,Z)` matrix defines discrete bundle gluing but does not
fix the continuous connection holonomy or select its own physical value.

## 6. Conditional relational channels

R14 retains the previously derived conditional construction.  When `dphi` is
everywhere timelike and nonzero and its connected levels are complete,

```text
h0 = |g^{-1}(dphi,dphi)| g
q0 = h0 + dphi tensor dphi
```

makes `q0` positive definite on each `phi` level; its intrinsic distance is a
chart/coframe-invariant observer separation on that branch.  It is not a
universal physical `D_g` and does not apply to the static spatial-`phi`
control.

R15 remains only the working type

```text
X_max = sup { D_g(A,B) : A,B in O and C_g(A,B) }.
```

The observer domain `O`, comparison rule `C_g`, native nonnegative `D_g`,
attainment, controlling paths, and cut/multiple-maximizer behavior remain
open.

## 7. Why no closure relation follows

The tested relations are identities, compatibility conditions, or discrete
classification rules.  None provides a new non-identity equation among
physical readouts on one complete domain with a derived normalization and
off-shell response.

In particular,

```text
Cartan/Bianchi identity != physical response law
F=dS                 != selected holonomy
cap determinant      != selected completion
scale weight         != selected representative
self-consistency word != defined fixed-point operator.
```

A bootstrap closure would require, at minimum, a complete `R_geom`, a native
response `A(X,O)`, and a defined target, normalization, pairing, and closure
operator.  Those are inputs to the closure, not consequences of merely naming
it.
