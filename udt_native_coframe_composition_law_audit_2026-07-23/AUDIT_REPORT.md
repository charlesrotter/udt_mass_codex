# Native Complete-Coframe Composition-Law Audit

Date: 2026-07-23

Status: `VERIFIED_WITH_EXPLICIT_REPRESENTATIVE_SCOPE`

Maximum conclusion:

`CURRENT_UDT_PREMISES_SUPPLY_CONDITIONAL_RECIPROCAL_ONE_PARAMETER_COMPOSITION_BUT_NOT_A_WEIGHTED_MULTI_CONFIGURATION_MEAN_OR_NATIVE_COMPLETE_COFRAME_COMPOSITION`

## Result first

This audit found a real intermediate structure rather than another arbitrary
interpolation:

1. The founded reciprocal clock/ruler sector has an exact pairwise
   one-parameter composition law. A weighted mean is an exact algebraic
   construction only after weights and an aligned logarithmic coordinate are
   chosen; UDT does not select those weights or that multi-configuration mean.
2. The complete ten-field triangular coframe chart used by the structural and
   bank atlases is closed under an exact matrix group law. Its base, angular,
   and four shift fields combine coherently, and common scale is central.
3. That complete group law is still a law of a **chosen coframe
   trivialization/section**, not yet a law on physical metric configurations.
   It does not descend through independently equivalent local-Lorentz coframe
   representatives unless UDT supplies a type-correct relative base/internal
   identification and either selects a representative section or defines a
   genuinely local-Lorentz-equivariant quotient operation.
4. The separate scalar `phi`/`dphi` sector is not composed by that ten-field
   coframe group.

Thus J1 and J2 remain chosen configuration charts. The new group structure is
a stronger candidate than either affine chart, but the current registered
metric, Reciprocity, CSN, seal, cocycle, Cartan, and bootstrap record does not
promote it to the unique physical complete-coframe composition law.

## 1. The native part: reciprocal depth

For

```text
P(phi) = diag(exp(-phi), exp(+phi))
```

the founding comparison law and Reciprocity give exactly

```text
P(phi1) P(phi2) = P(phi1 + phi2),
det(P) = 1,
P^T K P = K.
```

After simplex weights are separately chosen, one may construct the aligned
reciprocal-sector mean

```text
P_bar = exp(sum_i w_i log(P_i))
      = P(sum_i w_i phi_i).
```

The formula is
`DERIVED_ALGEBRAIC_IDENTITY_GIVEN_CHOSEN_WEIGHTS_AND_AN_ALIGNED_LOG_COORDINATE`.
UDT supplies the pairwise group law; it does not currently select the simplex
weights or a weighted mean of distinct configurations. The construction does
not compose the transverse metric, shifts, independent scalar field, or
physical CSN representative.

If diagonal clock/ruler logs are `a` and `c`, then

```text
reciprocal depth = (c-a)/2,
common scale     = (c+a)/2.
```

Independent common-scale shifts leave the first expression invariant and
shift only the second. This is why the reciprocal subgroup survives CSN.

## 2. The complete ten-field chart has an exact group law

The atlas coframe can be written in `2+2` block form as

```text
E(A,D,S) = [[ A,   0 ],
            [ D S, D ]],
```

where `A` is the three-field upper-triangular base block, `D` is the
three-field upper-triangular angular block, and `S` contains all four
base-angular shifts. This accounts for all ten coframe fields.

Direct exact multiplication gives

```text
A12 = A1 A2,
D12 = D1 D2,
S12 = D2^-1 S1 A2 + S2.
```

The inverse is again in the same family:

```text
Ainv = A^-1,
Dinv = D^-1,
Sinv = -D S A^-1.
```

Both symbolic residuals are exactly zero. Positive diagonal entries are
preserved by multiplication and inversion. A common coframe scale
`Omega I` commutes with the whole group, so CSN is a central direction in this
chosen chart.

This is a useful exact result:

`DERIVED_ALGEBRAIC_CLOSURE_IN_CHOSEN_TRIVIALIZATION`.

It says the base, angular, and shift “instruments” are not merely a bag of ten
unrelated amplitudes. Once assembled in this complete coframe chart they form
a coherent solvable matrix group, with the shift block coupled
semidirectly to both diagonal blocks.

## 3. Why chart-group closure is not yet physical composition

A coframe maps coordinate tangent components to internal frame components.
Multiplying two coframe matrices treats those two index spaces as the same
vector space. That is legitimate only after a reference coframe/soldering or
trivialization identifies them.

The metric is unchanged by a local Lorentz refactorization `E -> Lambda E`.
Independent refactorizations of the inputs must therefore not change a
physical composition. The exact catch is:

```text
Lambda = diag(1,-1,-1,1),
Lambda^T eta Lambda = eta,
det(Lambda)=1,
Lambda_00=1.
```

Take a first coframe with one base shear,

```text
E1 = I, with (E1)_01 = 1,
```

and take the second physical input as either `I` or the metric-equivalent
coframe `Lambda`. The chart-group products are `E1` and `E1 Lambda`. Their
output metrics differ by

```text
[[0,2,0,0],
 [2,0,0,0],
 [0,0,0,0],
 [0,0,0,0]].
```

Therefore matrix multiplication does not descend through independent
coframe-gauge choices. Selecting the triangular representative repairs this
inside a chosen chart, but that selection is itself the missing physical
section and is not invariant under arbitrary chart changes.

The exact complete group is consequently:

`DERIVED_CHART_GROUP_CLOSURE; CHOSE_AS_PHYSICAL_COMPOSITION`.

## 4. Why the simpler alternatives do not close the seam

### Raw affine coframe mean

`I` and `Lambda=diag(1,-1,-1,1)` are proper, orthochronous
metric-equivalent coframes. Their equal affine mean is

```text
diag(1,0,0,1),
```

which has rank two. Raw coframe averaging therefore neither descends to the
metric quotient nor preserves nondegeneracy.

### Affine metric mean

Two exact Lorentzian metrics with the same coordinate time timelike,

```text
g0 = diag(-1,1,1,1),
g1 = [[-1, 2,0,0],
      [ 2,-3,0,0],
      [ 0, 0,1,0],
      [ 0, 0,0,1]],
```

both have determinant `-1`. Their midpoint has determinant zero. The
Lorentzian domain is not closed under unrestricted affine metric averaging.

### Relative-metric logarithm/geodesic

The strongest direct metric-only candidate forms `A=g0^-1 g1` and attempts
`g(t)=g0 exp(t log A)`. For the exact pair above, `A` has eigenvalues
`{-1,-1,+1,+1}` and only a one-dimensional `-1` eigenspace: one size-two
negative Jordan block. It has no real matrix logarithm because negative-real
Jordan blocks of each size must occur in pairs. Thus this construction is not
a global law over Lorentzian metric pairs. Where a real logarithm exists, it
still requires a branch, base/symmetrization, and multi-input prescription.

### Cocycle, Cartan, and bootstrap

- The reciprocal cocycle composes transition maps on an already supplied
  cover. It glues representations of one geometry; it does not average
  distinct configurations.
- Cartan supplies spacetime transport after one coframe/metric is given. It
  does not currently supply a connection on the space of complete
  configurations.
- The current bootstrap filters completed on-shell solutions. It has no
  multi-input coframe map or off-shell path equation.

These are different tensor and logical types, recorded exhaustively in
`PREMISE_TYPE_LEDGER.tsv`.

## 5. Exact nonuniqueness after every edge or face is fixed

Let `(w0,w1,w2,w3)` be simplex weights.

```text
b_base = w0 w1 w2
```

vanishes at every vertex and on all six edges, but equals `1/27` at the
`B0-B1-B2` barycenter. A reciprocal-depth deformation

```text
delta = epsilon b_base,
R(delta)=diag(exp(-delta),exp(+delta),1,1)
```

is always invertible and has determinant one. With the exact covector
`p=(1,1,0,0)`,

```text
g_delta^-1(p,p) = -exp(2 delta) + exp(-2 delta)
                 = -2 sinh(2 delta).
```

At `delta=+log(2)` the norm is `-15/4`; at `delta=-log(2)` it is `+15/4`.
Thus one freely parameterized reciprocal deformation can reverse the
interior causal sign while every vertex and edge remains fixed and the metric
determinant remains `-1`.

Likewise

```text
b_volume = w0 w1 w2 w3
```

vanishes on all four boundary faces but remains free in the tetrahedral
interior. Complete boundary-face data alone therefore cannot determine the
volume interior without an additional law.

These are not proposed UDT solutions. They are exact counterfamilies to the
claim that the currently registered endpoint, edge/face, CSN, or Reciprocity
data already determine the simplex interior. The implemented deformation is
constant in spacetime and does **not** establish preservation of the physical
finite-cell seal; no seal-compatible spacetime profile is claimed here.

## 6. J1 and J2 regraded

J1 mixes generator coordinates and coefficient tensors before evaluation. J2
evaluates each bank and mixes ten latent coframe fields plus four `dphi`
components afterward. In the exact one-field toy case,

```text
J1(lambda) = lambda^2,
J2(lambda) = lambda,
difference = lambda(lambda-1).
```

They agree at both endpoints and differ everywhere generic in the interior.

- J1 remains `CHOSE_ANALYTIC_CONFIGURATION_CHART`. It preserves a scalar
  within its frozen polynomial family.
- J2 remains `CHOSE_LOCAL_COFIELD_CHART`. It does not assert global scalar
  integrability away from endpoints.
- The triangular chart group supplies a stronger third candidate, but remains
  `CHOSE` as a physical composition until relative base/internal
  identification and either a representative section or a genuinely
  local-Lorentz-equivariant quotient operation are supplied; weighted
  multi-input and compatible `phi/dphi` rules remain separately open.

No result privileges the chart that produced the bounded base pocket.

## 7. What survives without a selected complete join

The following remain valid:

- the registered bank endpoints and prior edge classifications;
- Lorentzian nondegeneracy inside each supplied exponential-triangular chart;
- the exact reciprocal one-parameter group law;
- the exact complete triangular chart-group closure;
- at least one zero of `g^-1(dphi,dphi)` along any supplied continuous join
  whose endpoints have opposite signs.

The following remain join-dependent:

- the `B0-B1-B2` interior pocket;
- whether a fiber crosses once or twice;
- negative-component and null-family counts;
- interface location and shape.

## Smallest genuinely missing object

The new group result narrows the missing structure. UDT does not need an
arbitrary interpolation formula. It needs:

> a type-correct relative identification of the inputs' base/internal spaces;
> plus either a selected representative section or a genuinely
> local-Lorentz-equivariant quotient operation; plus a selected weighted
> multi-input rule and compatible `phi/dphi` rule.

Index identification alone is not gauge selection, and a representative
section is not interchangeable with mere soldering. If the complete data
package above is derived, the already-closed ten-field group provides a
coherent candidate assembly law. Otherwise group multiplication remains a
powerful coordinate tool rather than physics.

The registered finite-cell seal supplies only partial clock/radial soldering
and no unique complete lift. CSN supplies a quotient, not its section.
Bootstrap supplies no current section or path equation. Therefore the
physical promotion remains `OPEN`.

## Four banking gates

1. **Preregistered:** yes, commits `29d9356` and additions-only source amendment
   `374623f`, before registered algebra and outcome assignment.
2. **Full space or bounded scope:** exact for the registered premise types,
   the complete ten-field triangular coframe group, the stated affine and
   relative-log counterexamples, and the registered simplex bubbles; not every
   conceivable configuration-space operation.
3. **Independently verified:** yes, through separate exact reconstruction,
   rational group anchors, six behavioral J1/J2 source comparisons, six
   ten-field coframe reconstructions, and 16 exercised record-integrity
   mutations. The mutations protect saved scope/status records; they are not
   represented as independent mathematical derivations. The load-bearing
   algebra and source behavior are recomputed separately. The first fresh
   review and the post-correction fresh review each returned
   `PASS_WITH_CAVEATS`; every exact correction they required is applied. The
   second review confirmed that its remaining caveat was wording consistency,
   not a defect in the central mathematical verdict.
4. **Premises audited:** yes for metric map, positional composition,
   Reciprocity, CSN, seal, cocycle, Cartan, bootstrap, J1, J2, and the
   triangular group. Action, carrier, source, boundary functional, global
   solution, scale, and physical realization were not loaded.

No physics branch, action, carrier, boundary, mass, scale, or canon has been
selected.
