# Relative angular-area and shape-speed selector audit

Date: 2026-07-23
Mode: preregistered metric-led exact CPU algebra, complete non-block metric
Grade: `VERIFIED-WITH-CAVEATS`

## Result first

The complete UDT metric defines exact, frame-independent diagnostics for the
two quantities isolated by the preceding angular-generator census:

```text
relative angular-area rate
angular shape-speed squared
```

The currently registered metric algebra, Reciprocity, Common-Scale
Neutrality, finite-cell structure, caps, monodromy, Cartan/Bianchi
identities, bootstrap wording, and observed `c` anchor do **not** force their
global target values

```text
relative angular-area rate = 0
angular shape-speed squared = 1.
```

There is one new positive result. Every registered regular involutive mirror
seal forces the relative angular-area rate to vanish **at its fixed point**.
It does not force unit shape speed there, and it supplies no interior
propagation equation.

The strongest justified conclusion is therefore:

```text
THE_COMPLETE_NONBLOCK_METRIC_DEFINES_EXACT_FULL_CSN_INVARIANT_RELATIVE_
ANGULAR_AREA_AND_SHAPE_SPEED_DIAGNOSTICS_BUT_CURRENT_METRIC_ALGEBRA_
RECIPROCITY_CSN_FINITE_CELL_TOPOLOGY_CARTAN_IDENTITIES_BOOTSTRAP_AND_C_
DO_NOT_FIX_THEIR_GLOBAL_TARGET_VALUES__A_REGULAR_MIRROR_SEAL_FORCES_ZERO_
RELATIVE_AREA_RATE_AT_ITS_FIXED_POINT_BUT_LEAVES_SHAPE_SPEED_AMPLITUDE_
AND_BULK_PERSISTENCE_UNSELECTED
```

This is not a no-go theorem against a later UDT selector. It is a bounded
statement about the executable content of the presently registered
premises.

## The complete non-block metric

No block-diagonal ansatz was assumed. On any supplied reciprocal/angular
split, write the complete metric as

```text
G = [[h, C],
     [C^T, Q]].
```

The angular metric orthogonal to the reciprocal plane is the exact Schur
complement

```text
q = Q - C^T h^-1 C.
```

Consequently

```text
det(G) = det(h) det(q)
```

and a congruence transformation gives

```text
inertia(G) = inertia(h) + inertia(q).
```

Thus an arbitrary nonzero reciprocal-angular cross block `C` does not erase
the angular diagnostic or invalidate the Lorentz-signature control. Using
raw `Q` in place of `q` would be chart- and split-dependent and is explicitly
rejected by the catch proofs.

## Exact diagnostics

For a depth flow `T` normalized by `T(phi)=1`, define

```text
H_h = (1/2) h^-1 Lie_T(h)
H_q = (1/2) q^-1 Lie_T(q).
```

The full-metric Common-Scale-Neutral relative angular-area rate is

```text
A_rel = trace(H_q)/2 - trace(H_h)/2
      = (1/4) T log(det(q)/abs(det(h))).
```

The trace-free angular shape generator and its scalar speed are

```text
J_q     = H_q - (trace(H_q)/2) I
S_shape = (1/2) trace(J_q^2).
```

For the general positive angular metric

```text
q = exp(2w) R(theta)^T
    diag(exp(-2u), exp(2u))
    R(theta),
```

exact algebra gives, in the registered reciprocal gauge,

```text
A_rel   = w_p
S_shape = u_p^2 + theta_p^2 sinh(2u)^2.
```

The target pair is exactly

```text
w_p = 0 AND S_shape = 1.
```

These formulas include both changing angular eigenvalues and rotating
angular axes. They are invariant under a conformal rescaling shared by the
entire metric. CSN therefore makes the quantities meaningful; it does not
set their numerical values.

## What the seal actually derives

At a regular fixed point of a mirror seal with angular lift `R`, the first
angular jet obeys

```text
-q_p = R^T q_p R.
```

Taking a trace after multiplication by `q^-1` forces

```text
A_rel = 0
```

at the fixed seal for all four registered involutive lift types. The
trace-free jet dimensions are:

```text
angular +I:       0
angular -I:       0
axis reflection:  1
axis exchange:    1
```

The first two lifts force zero shape speed. Reflection and exchange leave a
free nonnegative amplitude. Unit shape speed is allowed only when that free
amplitude is separately set to one; it is not selected.

This separates a genuine local theorem from two unjustified promotions:

1. seal stationarity is not an interior equation; and
2. a free one-dimensional jet is not a unit-normalized jet.

The exact lift table is
[SEAL_DIAGNOSTIC_ATLAS.tsv](SEAL_DIAGNOSTIC_ATLAS.tsv).

## Endpoint-flat bulk counterfamily

The finite cell and its endpoint jets do not determine the interior pair.
On normalized cell depth `y` use

```text
p(y) = y^3 (1-y)^3.
```

The function and its first two derivatives vanish at both endpoints. Starting
from the matched profile

```text
w=0, u=y, theta=0,
```

the three independent deformations

```text
w     = alpha p(y)
u     = y + beta p(y)
theta = kappa p(y)
```

preserve the complete endpoint two-jets while independently changing:

- relative area through `alpha`;
- fixed-axis shape speed through `beta`; and
- rotating-axis shape speed through `kappa`.

The construction remains non-block: choose any smooth nonzero `C` and set

```text
Q = q + C^T h^-1 C.
```

Then the exact Schur metric and both diagnostics are unchanged. This is a
counterfamily to a claimed derivation from the current local metric,
finite-cell, or boundary data; it is not asserted to be an on-shell universe.

See
[ENDPOINT_FLAT_COUNTERFAMILY.tsv](ENDPOINT_FLAT_COUNTERFAMILY.tsv).

## Selector-by-selector ruling

| source | relative area | shape speed | global pair |
|---|---|---|---|
| complete metric algebra | not fixed | not fixed | not derived |
| Reciprocity | not fixed | not fixed | not derived |
| CSN | invariant, value free | invariant, value free | not derived |
| finite cell | endpoint-flat bulk freedom | endpoint-flat bulk freedom | not derived |
| mirror seal | zero at fixed seal | zero or free amplitude | not derived |
| cap regularity/topology | constrains endpoints | constrains endpoints | not derived |
| monodromy | constrains descent | constrains descent | not derived |
| Cartan/Bianchi | identities for every smooth countermetric | same | not derived |
| bootstrap | no executable response equation | same | not an equation |
| observed `c` | retained in complete metric | no dimensionless normalization | not derived |
| twelve-family crosscheck | zero forcing families | zero forcing families | not derived |

The machine-readable reasons and countercontrols are in
[SELECTOR_RULING_MATRIX.tsv](SELECTOR_RULING_MATRIX.tsv).

## The role of `c`

The measured Einsteinian `c` remains explicit in

```text
h = diag(-c^2 exp(-2phi), exp(2phi))
```

and in the complete determinant. It is not set to one. It establishes the
clock/ruler conversion and physical scale anchor. The dimensionless
relative rate and shape speed are logarithmic metric rates with respect to
dimensionless `phi`, so `c` does not supply either missing value.

This audit does not test or alter the broader co-presence interpretation,
the small-regime clock-rate hypothesis, or the SNe lane.

## What remains open

The present geometry has now reduced the desired full reciprocal angular
match to two exact invariant scalar values. It supplies one local boundary
condition:

```text
A_rel(seal)=0.
```

What is still absent is an intrinsic bulk law that:

1. propagates or otherwise determines the relative-area diagnostic through
   a complete finite cell;
2. fixes the shape-speed amplitude to one rather than zero or an arbitrary
   value; and
3. selects compatible transport so a pointwise pattern persists globally.

The current bootstrap is an admissibility idea, not an executable equation,
functional, response map, or normal equation. This audit does not invent one.

There remain zero complete on-shell `(G,phi)` branch witnesses in the tested
registry. Therefore no action, carrier, matter source, boundary charge,
mass, or density selection is concluded.

## Verification and four gates

1. **Preregistered:** yes; commit
   `cabb61a1f943b667fe2c2898531e365265588f05`.
2. **Full space or bounded scope justified:** yes for every positive
   rank-two Schur angular metric on a supplied regular split, all eleven
   registered selector sources, all registered mirror lifts, and the twelve
   parametric completion families; no complete on-shell universes are
   claimed.
3. **Independently verified:** yes for load-bearing algebra by a separate
   standard-library/Fraction implementation with independent finite
   differences, rational non-block controls, exact endpoint jets, mirror
   ranks, source replay, and 24/24 mutation catches.
4. **Every premise audited:** yes within the registered selector universe;
   action, source, carrier, and unregistered dynamics remain explicitly
   open.

The grade remains `VERIFIED-WITH-CAVEATS` because the counterfamily is an
off-shell freedom witness and no separately selected native field equation
or complete on-shell branch exists.
