# Exact derivation — reciprocal reduction, path strain, and loop closure

## 1. The founded scalar channel is not the loop object

The founded reciprocal character is one-dimensional:

```text
D(phi)=diag(exp(-phi),exp(phi)),
J=D^-1 dD=H dphi,  H=diag(-1,+1).
```

For smooth `phi`,

```text
dJ+J wedge J=H d^2 phi+[H,H] dphi wedge dphi=0.
```

Thus the derived scalar channel supplies exact path composition but no local non-Abelian loop
defect. A nonzero closure curvature needs a larger reduced structure, singular data, or another
object. This rederives the old negative without using that historical file affirmatively.

## 2. Ordinary spacetime holonomy is too broad

The Levi-Civita connection and curvature exist for every supplied metric representative. The exact
control `R_t x R_x x S2` already has nonzero sphere curvature without any carrier or matter data.
The current registered complete-metric witnesses can even generate full `so(1,3)` holonomy.

Therefore

```text
nontrivial Levi-Civita holonomy != a matter discriminator.
```

It may transport or obstruct a separately supplied reduction, but identifying all metric curvature
with matter would classify ordinary macro curvature as the same object and fails falsifier F02.

## 3. The smallest sharp conditional bridge is a projector reduction

Suppose a complete branch supplies an orthogonal rank-one projector `P` in a three-dimensional
positive spatial or reciprocal bundle. Write locally

```text
P=n n^T,  n dot n=1,  Q=I-P.
```

The sign of `n` cancels, so `P` is naturally an `RP2` rather than an oriented `S2` variable. No
orientation choice is needed for the response derived below.

For a metric-compatible connection `D`,

```text
D_i P=(D_i n)n^T+n(D_i n)^T.
```

At one point choose a normal orthonormal frame with `n=e3` and write

```text
D_i n=(a_i,b_i,0).
```

Then exact matrix multiplication gives

```text
(1/2) tr[(D_i P)^T(D_j P)] = D_i n dot D_j n = S_ij.
```

The canonical path-strain scalar is therefore

```text
L_path=(1/2) sum_i ||D_i P||^2=tr S.
```

This is the existing `L2` form, expressed without choosing an oriented lift.

## 4. The same projector has a canonical relative loop curvature

The derivative commutator is

```text
K_ij=[D_i P,D_j P].
```

In the same frame it acts only on the transverse two-plane and equals its infinitesimal rotation by

```text
F_ij=a_i b_j-b_i a_j=n dot (D_i n cross D_j n).
```

The exact identities are

```text
P K_ij=K_ij P=0,
Q K_ij Q=K_ij,
(1/2) sum_ij ||K_ij||_F^2
  =sum_ij F_ij^2
  =(tr S)^2-tr(S^2).
```

Hence the existing `L4` area form is exactly the squared noncommutation of one and the same
projector's path deformations. This is not an analogy and does not require an oriented `S2` lift.

For the projected connection on the transverse bundle, the full curvature is

```text
R_Q=Q R_D Q+Q(DP wedge DP)Q.
```

The second term is the relative reduction curvature just derived. In a curved spacetime it must not
be confused with total ambient curvature. Selecting the relative term rather than the full `R_Q`,
or selecting a subtraction convention, is not yet a current UDT consequence.

## 5. Exact rank-one and invariant selection result

If every derivative follows one target direction,

```text
D_i n=q_i w,
```

then `K_ij=0` for every pair while `L_path` can be nonzero. Thus rank-one blindness is exactly the
statement that response begins with loop area rather than path strain.

For a supplied unit-direction section, the complete parity-even, domain-rotation and target-rotation
invariant first-derivative inventory through quartic order is:

```text
order 2: tr S,
order 4: alpha (tr S)^2 + beta tr(S^2).
```

On a rank-one strain with eigenvalues `(lambda,0,0)`, the quartic term is

```text
(alpha+beta) lambda^2.
```

Requiring rank-one blindness forces `beta=-alpha`. Therefore the area/commutator form is unique up
to normalization inside this exact bounded class.

The qualification is load-bearing:

- current Reciprocity does not derive rank-one blindness;
- `tr(S^2)` is a same-symmetry countermodel with positive rank-one cost;
- allowing second derivatives adds terms such as `|D^2 n|^2`;
- allowing higher first-derivative order adds positive terms such as `tr(S)[(tr S)^2-tr(S^2)]`;
- a general full-screen or higher-rank reduction has a larger invariant inventory.

Thus `L4` is `UNIQUE_CONDITIONAL`, not uniquely selected by current UDT.

## 6. What the loop premise does and does not select

The historical candidate premise said path-only axis variation is non-material and only loop
closure costs response. Taken literally, that selects the `L4` term and excludes `L2`; it does not
derive `L2+L4`.

To obtain the two-term form, one must independently require both:

1. response to pathwise bending of the reduction; and
2. response to its relative loop curvature.

With locality, positive static norm, parity evenness, and lowest derivative order, these give

```text
E[P]=c2 integral L_path + c4 integral L_loop,
c2>0, c4>0.
```

The form is canonical for a supplied rank-one projector, but the requirement that both responses
are physical is an extra premise. Their relative coefficient also remains continuous.

Under `P_R(x)=P(x/R)` in three spatial dimensions,

```text
E2(R)=R E2(1),
E4(R)=R^-1 E4(1),
R_star=sqrt[c4 E4(1)/(c2 E2(1))].
```

Every positive coefficient ratio supplies a stationary scale. Finite size therefore cannot be
inverted to select the ratio unless an independent metric/global scale equation first fixes that
size. The `c_E` and `G_obs` anchors presently provide no registered coefficient map.

## 7. Carrier and topology consequence

The projector target is `RP2`. On a simply connected compactified three-domain, a continuous map to
`RP2` lifts to `S2`, and the covering preserves the relevant `pi_3` integer. Consequently the
existing `S2` Hopf representation can be a double-cover coordinate representation of this
conditional projector geometry.

This does not select:

- the projector itself;
- a compactified physical domain or boundary;
- a lift, phase, toric quotient, cap, or orientation;
- the deformation space of the relaxed carrier;
- a time-live persistence law.

Topology remains downstream of a supplied global reduction and completion.

## 8. Why the complete metric has not yet closed the bridge

Current complete-coframe evidence supplies several possible local reductions—nonnull-`dphi`
`3+3`, curvature/tidal spectral projectors on simple strata, conditional celestial directions, and
toric projectors—but selects no universal rank-one spatial projector. The active pointwise
extension selector rank is zero, full holonomy generically destroys endpoint reduction, and flat or
degenerate strata select none.

A universal carrier is not required for the plural branch program. A completed metric branch could
derive `P` from its own invariant simple spectral line or reduced holonomy. If that `P` descends
globally, the identities above become branch-native geometry. No current equation or admissibility
law has yet produced such a completed branch.

The sharpened conceptual candidate is therefore:

> matter-like branches may be complete metric branches whose own invariant geometry selects a
> reciprocal projector reduction and sustains nontrivial global closure of that reduction.

That is a coherent candidate architecture, not an adopted premise or a derived matter theorem.

## 9. Exact maximum conclusion

```text
PROJECTOR_PATH_AND_LOOP_RESPONSE_IDENTITY_DERIVED_CONDITIONAL_ON_A_SUPPLIED_RANK_ONE_REDUCTION;
AREA_L4_UNIQUE_CONDITIONAL_IN_THE_RANK_ONE_BLIND_FIRST_DERIVATIVE_QUARTIC_CLASS;
BRANCHWISE_METRIC_SELECTED_RECIPROCAL_REDUCTION_IS_A_COHERENT_CANDIDATE;
REDUCTION_SELECTION_BOTH_RESPONSE_REQUIREMENT_COEFFICIENT_BOUNDARY_DYNAMICS_SOURCE_AND_MASS_OPEN.
```
