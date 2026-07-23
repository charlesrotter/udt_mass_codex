# UDT coframe-to-Hopf bridge audit

Date: 2026-07-23

Mode: preregistered metric-led CPU exact algebra and evidence crosswalk

## Result first

The new complete-coframe chart-group result connects nontrivially to the
existing Hopf evidence, but only at a precisely bounded chart-algebra level.

The complete positive triangular chart group contains **two independent
scale-free additive diagonal characters**: one in its base block and one in
its angular block. The angular character survives arbitrary upper-triangular
angular shear algebraically. Its common-scale times reciprocal-diagonal
subgroup obeys

```text
D(Omega1,phi1) D(Omega2,phi2)
  = D(Omega1 Omega2, phi1+phi2).
```

After making the already-conditional reciprocal-toric identification of this
angular character with the toric `phi`, that one group law induces exact
composition laws for the existing Hopf connection weight and target-sphere
latitude:

```text
f = 1/(1+exp(4phi)),

f12 = f1 f2 / [f1 f2 + (1-f1)(1-f2)],

z = 2f-1 = -tanh(2phi),

z12 = (z1+z2)/(1+z1 z2).
```

The identity is `phi=0`, equivalently `f=1/2` and `z=0`; inversion sends
`phi -> -phi`, `f -> 1-f`, and `z -> -z`. Common angular scale cancels.

Within the chosen triangular trivialization, and after choosing chart
multiplication as the comparison operation and identifying angular depth
with toric/scalar `phi`, the Hopf weight and latitude are exact homomorphic
reparameterizations. No frame-independent physical composition law follows.

It is not native carrier or Hopfion emergence. Current UDT does not select:

- whether the angular character physically owns positional `phi`;
- the aligned diagonal angular axes or their representative-independent
  meaning;
- the transverse phase `delta`;
- circle periods/action, caps, orientation, or full-range completion;
- the deformation space from the exact seed to the relaxed field; or
- an action, variation law, source, boundary, mass, or time-live persistence.

Maximum conclusion:

`EXACT_CONDITIONAL_CHART_LEVEL_ANGULAR_CHARACTER_TO_HOPF_WEIGHT_AND_LATITUDE_CROSSWALK_IDENTIFIED__FRAME_INDEPENDENT_KINEMATIC_LAW_NATIVE_CARRIER_AND_HOPFION_EMERGENCE_REMAIN_OPEN`

## 1. What the complete group contributes

Write the registered coframe chart as

```text
E(A,D,S) = [[A,0],[D S,D]],
```

where `A` and `D` are positive upper-triangular `2x2` blocks and `S` is an
arbitrary `2x2` shift block. Exact multiplication gives

```text
A12 = A1 A2,
D12 = D1 D2,
S12 = D2^-1 S1 A2 + S2.
```

The inverse has

```text
Ainv = A^-1,
Dinv = D^-1,
Sinv = -D S A^-1.
```

The new audit independently reconstructs these formulas. It then
parameterizes the positive diagonals of both upper-triangular blocks by

```text
A_diag = exp(sigmaA) diag(exp(-alpha),exp(alpha)),
D_diag = exp(sigmaD) diag(exp(-phiD),exp(phiD)).
```

Matrix multiplication forces

```text
alpha12 = alpha1+alpha2,
phiD12  = phiD1+phiD2,
sigmaA12 = sigmaA1+sigmaA2,
sigmaD12 = sigmaD1+sigmaD2.
```

These identities survive the off-diagonal shears because triangular
multiplication multiplies diagonal entries. They also survive arbitrary
shift blocks because `D12` does not depend on `A` or `S`.

This is a useful structural result, but it exposes rather than removes an
ownership question. The complete registered ten-field-plus-scalar space has
base depth `alpha`, angular depth `phiD`, and the separately represented
scalar `phi`. Current premises do not identify them. The controlling
reciprocal-subbundle ownership audit already proves that coframe labels do not
select a physical reciprocal plane. This audit does not reverse that result.

## 2. Complete registered subgroup census

All eight preregistered candidates are classified in
`SUBGROUP_CENSUS.tsv`.

The principal findings are:

- the full ten-field positive triangular family is a chart group;
- its zero-shift block-diagonal subset is a subgroup, but setting the shifts
  to zero remains a choice;
- the complete positive upper-triangular angular factor is closed;
- its diagonal subset is a subgroup;
- common scale times reciprocal diagonal is a commutative subgroup; and
- the diagonal subgroup is **not normal** under the full angular group.

The last point is load-bearing. With

```text
H = [[1,s],[0,1]],
R(phi) = diag(exp(-phi),exp(phi)),
```

the conjugate has off-diagonal entry

```text
s[exp(phi)-exp(-phi)],
```

which is generically nonzero. Therefore the Hopf-friendly diagonal axes do
not form an invariant sector of the complete upper-triangular angular
orchestra. They are an exact subgroup after alignment, not a branch selected
by the current complete group.

## 3. Induced conditional Hopf-coordinate law

In the supplied reciprocal-toric metric,

```text
g_ang = Omega^2[
  exp(-2phi) dxi1^2 + exp(2phi) dxi2^2
],
```

the normalized metric-dual connection weight is

```text
f = exp(-2phi)/[exp(-2phi)+exp(2phi)].
```

Because the squared diagonal odds multiply under coframe multiplication,

```text
(1-f12)/f12 = [(1-f1)/f1][(1-f2)/f2],
```

which gives the exact logistic law in the result. It is associative and
commutative on `0<f<1`, has identity `1/2`, and inverse `1-f`.

The existing quotient map is

```text
n(phi,delta) = (
  sech(2phi) cos(delta),
  sech(2phi) sin(delta),
  -tanh(2phi)
).
```

Its third component is `z=2f-1`, so the coframe law induces the displayed
fractional latitude law. Its transverse magnitude also closes:

```text
rho12 = rho1 rho2/(1+z1 z2).
```

What does not follow is equally explicit. The pointwise coframe group does
not contain or compose the coordinate phase

```text
delta = xi1-xi2.
```

Consequently it does not compose the complete `S2` direction. If `phi` is
chosen to equal `phiD`, differentiating the additive law gives
`dphi12=dphi1+dphi2`; that is exact within the supplied identification, not a
native scalar rule over the complete ten-field-plus-independent-scalar space.

## 4. Conditional null-direction bridge

The quotient above has exact unit norm. In the dual orthonormal frame of a
supplied Lorentzian coframe,

```text
k = E0 + n1 E1 + n2 E2 + n3 E3
```

is therefore null, and positive common-scale rescaling preserves its null
line. This makes the reciprocal-toric Hopf seed an exact section of the
conditional projective null-direction `S2` fiber.

That is a clean correspondence:

```text
aligned angular reciprocal depth + supplied phase
    -> Hopf-seed S2 direction
    -> null-direction section in a supplied coframe.
```

It does not select the coframe representative, phase, section, or transport.
Local Lorentz freedom changes the component direction, and the earlier exact
stabilizer obstruction still prevents coframe labels from becoming a
universal physical reciprocal subbundle.

## 5. Pointwise composition is not topology composition

The finite-endpoint Hopf readout in the conditional toric control is

```text
Q = f_minus-f_plus.
```

The audit gives an exact counterexample to treating the pointwise chart law
as a binary operation on `Q` alone. Two second inputs can have the same separate readout
`Q=1/2`, while composition with the same first input produces respectively

```text
Q_composed = 4/5
Q_composed = 89/112.
```

Therefore the composed readout does not factor through the two separate
readout values; the complete endpoint profiles remain necessary. No target
operation on `Q` is presumed, so this is not phrased as a failed homomorphism.

The conditional unit class still follows when full reciprocal range, two
periodic circles, a free diagonal/anti-diagonal circle action, opposite
primitive caps, orientation, and normalization are supplied. None of those
global data is derived by the pointwise group.

## 6. Relation to the existing stable Hopfion

The prior exact formula

```text
tan(eta)=exp(2phi)
```

continues to identify the reciprocal-toric quotient with the degree-one
`hopf_seed` map exactly. The new contribution is that its connection weight
and latitude are now seen to inherit a precise group law from the aligned
angular coframe subgroup.

The relaxed field is still different. It lives in the independently posited
`Map(S3,S2)` carrier configuration space and is stabilized by the
carrier-conditional `L2+L4` functional in a fixed finite box with its audited
operator and boundary premises. A pointwise coframe group supplies neither
that deformation space nor that action.

Thus the prior status remains unchanged:

`SETTLED_STATIC_FINITE_BOX_CONDITIONAL`.

No time-live persistence, physical boundary completion, native source,
unconditional mass, or carrier emergence follows.

## 7. What was learned

The Hopf correspondence is not floating independently of the complete metric
atlas. One of its coordinates—the reciprocal latitude—is organized by an
exact additive character already present in the complete triangular coframe
group. The connection weight is the common-scale-free logistic image of that
character.

The missing bridge is now better localized:

1. physical ownership/gauge descent for the relevant reciprocal character;
2. native selection or construction of the transverse phase and its
   transport;
3. global finite-cell torus/cap/boundary completion;
4. a deformation space beyond the exact seed; and
5. a native action or variation law.

This is several distinct missing data, not “one last equation.” The audit
does not invent any of them.

## Completeness and evidence gates

This package covers one exact chart-algebra/bundle crosswalk:

- complete registered chart-group and enumerated subgroups;
- exact toric weight/latitude/null-section relations;
- global dependency and finite-endpoint controls; and
- an evidence-level crosswalk to the carrier-conditional Hopfion.

It does not cover field equations, action terms, boundary variation,
dynamics, branch structure, stability recomputation, scale, or mass.

Banking gates:

1. Preregistered: yes, commits `ec8f26b` and source amendment `93f812f`
   precede implementation inspection and outcome assignment.
2. Full or bounded: complete for the literal eight-candidate preregistered
   list and eleven bridge dependencies; not an exhaustive subgroup
   classification or every imaginable bundle/action completion.
3. Independent: the production route is exact symbolic algebra; a separate
   implementation supplies exact-rational anchors and fail-closed mutation
   catches. The first fresh review also reconstructed the general algebra,
   returned `FAIL` on scope/verifier defects, and its exact corrections are
   applied subject to a post-correction fresh review.
4. Premises: metric/group, chart, gauge, scalar ownership, toric, global,
   carrier, action, box, boundary, and dynamics premises are explicit.

No prior package, navigation control, `LIVE.md`, `CANON.md`, research
artifact, physics action, or GPU result is changed.
