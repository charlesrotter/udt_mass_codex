# Angular bulk Jacobi/selector audit

Date: 2026-07-23
Mode: preregistered metric-led exact CPU derivation
Grade: `VERIFIED-WITH-CAVEATS`

## Result first

The complete non-block metric derives a unique covariant object that
governs how the angular deformation changes through a supplied regular
finite-cell depth flow. It is the projected Jacobi transport identity

```text
D_T(B) + B^2 + K_eff = 0.
```

Here `B` is the complete angular deformation endomorphism and

```text
K_eff =
    projected angular tidal curvature
  + sector-leakage terms
  - moving-projector terms
  - projected flow-acceleration gradient.
```

All terms come from the complete metric and its Levi-Civita connection.
Nothing was imported from GR field equations or an action.

This object is not, by itself, the missing independent law. It is a Cartan/
Jacobi identity: the same freely chosen second metric jets that determine
how `B` changes also determine `K_eff`. At fixed angular metric and first
jet, the three independent angular second-jet components span all three
self-adjoint tidal-source components. Current UDT premises provide no
separate equation fixing them.

The strongest unconditional conclusion is:

```text
COMPLETE_METRIC_DERIVES_THE_COVARIANT_ANGULAR_JACOBI_TRANSPORT_OBJECT_
BUT_CURRENT_UDT_PREMISES_DO_NOT_SUPPLY_ITS_INDEPENDENT_CURVATURE_CLOSURE
```

There is also a new exact conditional theorem. Define the effective-source
difference

```text
Delta_K = K_eff_angular - K_rec.
```

For the founded reciprocal generator

```text
L = diag(-1,+1),
```

its constant effective Jacobi source is

```text
K_rec = -L^2 = -I.
```

If a future UDT rule derives `Delta_K=0`, and if a branch has two regular
mirror seals with a nonsingular parallel angular screen, then the second
seal forces the initially free angular shape amplitude squared to be one.
The angular area remains relatively constant and the unit reciprocal
shape persists throughout the cell.

Neither `Delta_K=0` nor the required two-seal completion is currently
selected. The theorem exposes the smallest exact missing tensor join; it
does not authorize adopting it.

## Complete non-block derivation

Let `T` be a supplied depth flow with `T(phi)=1`, let

```text
M(X) = nabla_X T
a    = nabla_T T,
```

and let `P` project onto the positive angular screen with `Q=I-P`. The
full torsion-free curvature identity is

```text
nabla_T M + M^2 + R_T - nabla(a) = 0,
R_T(X)=R(X,T)T.
```

Define

```text
B = P M P,
X = P M Q,       Y = Q M P,
U = P(nabla_T P)Q,
V = Q(nabla_T P)P.
```

Direct projection, without assuming a block-diagonal metric or a preserved
split, gives

```text
D_T(B) + B^2 + K_eff = 0,

K_eff =
    P R_T P
  + X Y
  - U Y
  - X V
  - P nabla(a) P.
```

`XY` records deformation leaking through the reciprocal complement. `UY`
and `XV` record motion of the screen itself. The final term retains
accelerated or non-affine depth flow. Dropping any of them would silently
restrict the complete metric.

For a projectable normal-flow control, the formula reduces to

```text
B_p - kappa B + B^2 + R_T = 0,
```

where `kappa` is the depth-flow non-affinity. That familiar-looking
Riccati form is a conditional reduction of the full object, not the
universal UDT metric.

The complete formulas are in
[FULL_PROJECTED_JACOBI_FORMULA.json](FULL_PROJECTED_JACOBI_FORMULA.json)
and
[GENERIC_REDUCED_RICCATI_FORMULA.json](GENERIC_REDUCED_RICCATI_FORMULA.json).

## Area, shape, and twist

In the CSN-normalized diagnostic representative, decompose the
two-dimensional screen deformation as

```text
B = A_rel I + J + W,
```

where:

- `A_rel` is the relative angular-area rate;
- `J` is trace-free and self-adjoint;
- `W` is skew and measures screen twist; and
- `S_shape=(1/2)tr(J^2)`.

Two-dimensional matrix algebra gives

```text
B^2 =
  (A_rel^2 + S_shape - omega^2) I
  + 2 A_rel J
  + 2 A_rel W.
```

Therefore the one tensor identity splits exactly into

```text
D_T(A_rel) + A_rel^2 + S_shape - omega^2
  + (1/2)tr(K_eff) = 0,

D_T(J) + 2 A_rel J + SymTF(K_eff) = 0,

D_T(W) + 2 A_rel W + Skew(K_eff) = 0.
```

The desired twist-free reciprocal angular behavior

```text
A_rel=0, S_shape=1
```

would require

```text
tr(K_eff)=-2
```

plus compatible trace-free transport. In the fully general case the trace
condition is

```text
tr(K_eff)=-2+2 omega^2.
```

This is an equivalence, not a selection: assigning those source values
would restate the desired solution in curvature language.

## CSN and the observed `c`

On a supplied reciprocal two-plane/coframe, define the positive local
normalizer

```text
Omega_h = (abs(det h)/c^2)^(1/4)
```

and the diagnostic representative

```text
G_star = Omega_h^-2 G.
```

Under a full common-scale change `G -> lambda^2 G`,

```text
Omega_h -> lambda Omega_h
```

so `G_star` is unchanged and

```text
det(h_star)=-c^2.
```

This packages the transport object in a CSN-invariant diagnostic
representative while retaining the observed `c` anchor. It is conditional
on the supplied reciprocal coframe/area normalization and does not select
the physical split or a dynamical representative.

Exact controls use `c=2`, `c=3`, and `c=299792458`; `c` is never set to
one. The dimensionless Jacobi source remains free after common scale is
removed.

See
[CSN_NORMALIZED_REPRESENTATIVE.json](CSN_NORMALIZED_REPRESENTATIVE.json).

## Why the Jacobi object is an identity, not closure

For a generic positive angular metric `q(phi)`,

```text
B = (1/2) q^-1 q_p.
```

Its reduced tidal operator is

```text
R_T = -B_p + kappa B - B^2.
```

At a point, hold `q` and `q_p` fixed. Varying the three symmetric
components of `q_pp` changes all three self-adjoint components of `R_T`
independently. The exact source map has rank three.

Thus the equation always balances because curvature is constructed from
the same metric jets. Without another UDT relation, it does not tell the
metric which second jet to choose.

The parent endpoint-flat three-knob family strengthens the point globally.
It preserves every endpoint jet through second order and retains exact
non-block extensions while independently changing relative area, fixed-axis
shape, and rotating-axis shape in the cell interior. Cartan and Bianchi
identities remain true for every member.

## The strongest conditional closure

The most informative new result comes from testing the reciprocal source
comparison rather than merely rejecting it.

Assume, strictly conditionally,

```text
Delta_K=0,
K_eff_angular=K_rec=-I.
```

In a parallel screen frame the exact transport equation is

```text
B_p + B^2 - I = 0.
```

At a first regular mirror seal let

```text
B(0)=J0,
tr(J0)=0,
J0^2=s^2 I.
```

Writing

```text
t=tanh(Delta_phi),
```

the exact nonsingular matrix solution is

```text
B(t)=(J0+tI)(I+tJ0)^-1.
```

Its relative-area rate and shape speed are

```text
A_rel =
  t(1-s^2)/(1-s^2 t^2),

S_shape =
  s^2(1-t^2)^2/(1-s^2 t^2)^2.
```

For a nonzero finite cell whose second regular mirror also requires
`A_rel=0`, and away from a Riccati pole,

```text
A_rel(second seal)=0  iff  s^2=1.
```

When `s^2=1`, `B` is constant and

```text
A_rel=0, S_shape=1
```

throughout the cell. The result is orientation-neutral: it fixes the
reciprocal magnitude, not a preferred angular axis.

Four independent exact-rational controls are in
[CONDITIONAL_TWO_SEAL_FLOW.tsv](CONDITIONAL_TWO_SEAL_FLOW.tsv).

The load-bearing caveat is equally exact. Current Reciprocity derives the
abstract clock/ruler generator. It does not state that the angular
effective curvature source equals the reciprocal source. The previous
intertwiner theorem allows a matched representation after it is supplied
but does not select it. Nor does current finite-cell structure select two
regular mirrors over caps, boundaries, quotients, or other completions.

Accordingly this is:

```text
CONDITIONAL_THEOREM_ON_AN_UNREGISTERED_PREMISE
```

not a native UDT derivation.

## Twelve-route audit

No registered route supplies the missing independent source:

| route | ruling |
|---|---|
| complete non-block screen geometry | defines the exact objects; jets free |
| full Cartan curvature block | identity, not field equation |
| reduced phi-normal Riccati form | identity; second-jet source rank three |
| CSN | invariant representative; values free |
| reciprocal/angular comparison | exact missing `Delta_K` join exposed |
| one or two seals | local/integral conditions only without source equality |
| caps and monodromy | constrain completion, not bulk second jets |
| Bianchi and holonomy | consistency identities, not source assignment |
| finite-cell integral | one balance, not a pointwise law |
| bootstrap | no executable functional or response equation |
| observed `c` | scale anchor, not dimensionless source selection |
| twelve completions | all remain parametric; zero on-shell branches |

Machine-readable rulings are in
[ROUTE_RULING_MATRIX.tsv](ROUTE_RULING_MATRIX.tsv).

## What was accomplished

The vague missing “bulk propagation law” has been replaced by three exact
objects:

1. the complete projected Jacobi transport identity;
2. its undetermined effective metric source `K_eff`; and
3. the reciprocal/angular source-difference tensor `Delta_K`.

The first is derived. The second is metric data but not independently
selected. The third is the smallest exact missing join. If it vanished on
a compatible two-seal branch, the unit reciprocal angular behavior would
follow rather than be assumed.

## What remains open

The next scientific question is now narrow:

> Does any already-founded UDT statement—not an invented extension—force
> `Delta_K=0`, or otherwise determine the same effective source?

Current evidence says no. A future answer could come from a more precise
bootstrap closure or another metric-native global identity, but neither may
be presumed.

The following remain open and were not touched:

- universal reciprocal/angular split and physical threading;
- selection of the two-seal completion;
- complete action and independent field equations;
- matter source, carrier, boundary charge, mass, or density response;
- complete on-shell finite-cell branches; and
- global physics interpretation.

No GPU work, SNe recalibration, repository reorganization, canonization, or
startup-navigation edit was performed.

## Verification and four gates

1. **Preregistered:** yes; commit
   `1844bdf884b2cbeb8be7dda0aa81689c249cbc68`.
2. **Full space or bounded scope justified:** complete for the exact
   projected identity on a supplied regular split/flow, its full
   trace/shape/twist decomposition, all twelve preregistered routes,
   registered seals and completions, and the stated conditional theorem.
   Critical-`phi`, unsupplied splits, and complete on-shell universes remain
   outside scope.
3. **Independently verified:** separate standard-library `Fraction`
   reconstruction of the full projection algebra, three generic reduced
   jets, rank-three source freedom, three trace/shape/twist controls, three
   non-block congruences, three `c` controls, four conditional two-seal
   flows, exact endpoint jets, all source hashes, and 27/27 exercised
   mutations.
4. **Every premise audited:** yes within the frozen route universe; the
   conditional source equality and two-seal completion are explicitly
   unregistered.

The grade is `VERIFIED-WITH-CAVEATS` because no fresh zero-context semantic
review was available and the positive closure theorem depends on an
unregistered source equality and completion class.
