# Exact derivation — three-observer overlap and calibration carry

Date: 2026-08-10
Mode: metric-led exact CPU algebra and semantic/type audit
Current grade: **VERIFIED-WITH-CAVEATS**

## 1. Primary result

The previous phrase “associative middle calibration carry remains open” combined three distinct
questions:

1. **associativity:** whether rebracketing an already typed composite changes it;
2. **composability:** whether the target calibration state of `A-B` is the same object as the source
   calibration state of `B-C`, or an explicit transition identifies them; and
3. **path independence/descent:** whether the direct `A-C` arrow equals the `A-B-C` composite.

They are not equivalent.

The bounded landing is

```text
ASSOCIATIVE_CARRY_DERIVED_FOR_COMPOSABLE_ENRICHED_QUERY_ARROWS;
DIRECT_EQUALS_COMPOSITE_IS_PATH_INDEPENDENCE_OR_CECH_DESCENT_NOT_ASSOCIATIVITY;
GENUINE_COMMON_PAIR_ATLAS_HAS_IDENTITY_TRIPLE_OBSTRUCTION;
GENERAL_SUPPLIED_PATH_OR_BRANCH_FAMILY_MAY_HAVE_NONTRIVIAL_HOLONOMY;
INDEPENDENTLY_REBUILT_B_STATES_REQUIRE_AN_EXPLICIT_MIDDLE_TRANSITION;
PHYSICAL_OWNERSHIP_OF_ONE_GLOBAL_RELATION_FAMILY_AND_ANY_SCALAR_RECIPROCAL_REDUCTION_REMAIN_OPEN.
```

This is a type correction and a conditional positive result. It does not select the physical pair
relations.

## 2. Correctly typed enriched comparison objects

Let `Q_A`, `Q_B`, and `Q_C` denote supplied complete calibrated observer-query states. A state may
include an event, clock/ruler calibration germ, causal pair flag, local pair-surface branch, and the
other declared data needed by that relation family. A complete regular transition has type

```text
J_AB : Q_A -> Q_B.
```

When the target of `J_AB` is literally the source of `J_BC`, matrix/function composition is defined
and

```text
(J_CD J_BC) J_AB = J_CD (J_BC J_AB)
```

exactly. This is ordinary associativity. The founding reciprocal character is a character on the
corresponding supplied reciprocal reduction; it does not create the enriched objects.

The enrichment remains `CONDITIONAL_QUERY_ENRICHMENT`, as established by the founding ownership
audit. What is new is that no additional dynamical law is needed merely to make already matched
enriched arrows associative.

## 3. Genuine common-atlas overlaps

Suppose `A`, `B`, and `C` label coordinate/calibration charts on one supplied regular pair geometry.
On a triple overlap let

```text
psi_AB : U_A -> U_B,
psi_BC : U_B -> U_C,
psi_AC : U_A -> U_C
```

be genuine transition maps. Then

```text
psi_AC = psi_BC o psi_AB
```

and differentiation gives

```text
J_AC = J_BC J_AB.
```

Define the based triangle product

```text
Omega_A = J_AC^-1 J_BC J_AB : Q_A -> Q_A.
```

For a genuine common atlas, `Omega_A=I` by the chain rule. The local pair metrics obey

```text
h_A = J_AB^T h_B J_AB,
h_B = J_BC^T h_C J_BC,
h_A = J_AC^T h_C J_AC.
```

This is a positive conditional closure theorem. The condition “genuine common atlas” is supplied or
must be derived from the complete solution/query; it is not selected by the chain rule.

## 4. Separately rebuilt pair surfaces are not automatically composable

The maps

```text
F_AB : Sigma_AB -> M,
F_BC : Sigma_BC -> M,
F_AC : Sigma_AC -> M
```

do not have a canonical binary composition. Their domains and images need not define one common
pair surface. Even equal pullback metrics do not identify their embeddings, as the previously
banked opposite-rotating-ruler witness proves.

If `A-B` ends in `Q_B^in` while `B-C` begins in `Q_B^out`, composition requires

```text
M_B : Q_B^in -> Q_B^out.
```

The typed composite is

```text
J_BC M_B J_AB.
```

The corresponding triangle product is

```text
Omega_A = J_AC^-1 J_BC M_B J_AB.
```

If `M_B` is supplied as the exact transition between two presentations of the same carried state,
the product closes. If it is omitted while the two B objects differ, setting `M_B=I` is a hidden
premise. Local `c_E` normalization does not supply this identification.

Thus the open joint is not the algebraic operation of carry. It is the physical ownership of the
objects and transitions that make a proposed composite well typed.

## 5. Associativity is not path independence

For any composable arrows, multiplication is associative. It does not follow that

```text
J_BC J_AB = J_AC.
```

The direct arrow and composite may represent different supplied paths or branch labels. A
nonidentity `Omega_A` then measures the difference.

Two interpretations must remain separate:

- for transition functions of one genuine chart atlas, nonidentity `Omega_A` is a descent/
  compatibility obstruction;
- for path-labelled transport arrows, nonidentity `Omega_A` is triangle holonomy and can be a valid
  geometric invariant.

Calling either outcome an associativity failure is a type error.

## 6. Exact metric-compatible holonomy witness

The production controller uses

```text
J_AB = [[2,1],[1,1]],
J_BC = [[1,1],[2,3]],
P    = J_BC J_AB = [[3,2],[7,5]],
eta  = diag(-1,1).
```

Define `h_B` and `h_C` so that `J_AB`, `J_BC`, and `P` are pairwise metric compatible. Let

```text
H = [[5/3,4/3],[4/3,5/3]],
H^T eta H = eta,
J_AC = P H.
```

Then the direct arrow is also metric compatible, but

```text
Omega_A = J_AC^-1 J_BC J_AB = H^-1 != I.
```

Pairwise metric compatibility therefore does not imply common-atlas descent. The same data are
consistent as path transports with Lorentz holonomy `H^-1`. Reversing the triangle gives the
inverse holonomy exactly.

This witness keeps every off-diagonal entry. Replacing the matrices by diagonal blocks changes the
product and fails an exercised catch-proof.

## 7. Frame covariance and the two kinds of reset

Under independent changes of supplied endpoint frames

```text
J_ij' = S_j J_ij S_i^-1,
```

the triangle product transforms as

```text
Omega_A' = S_A Omega_A S_A^-1.
```

Identity versus nonidentity, determinant, spectrum, and conjugacy class are consequently
frame-covariant.

### Common scale

For `S_i=sigma_i I`, all intermediate factors telescope. The based obstruction is unchanged. This
is the established common-scale cancellation and does not restore strong CSN as a physical
selector.

### Coherent reciprocal presentation change

If an already supplied calibration local system is re-trivialized consistently by `S_i=D(r_i)` on
all incident arrows, the intermediate `D(r_B)` cancels and the obstruction is conjugated at the
base. This is presentation covariance of a supplied local system.

It must not be confused with physically refactorizing one pair tape or using distinct incoming and
outgoing B states. An unmatched physical reciprocal reset survives explicitly in
`J_BC D(r) J_AB`.

## 8. The scalar reciprocal projection remains conditional

On the pure reciprocal subgroup, write multiplicative parameters

```text
D(z)=diag(z^-1,z).
```

Then

```text
D(z_BC)D(z_AB)=D(z_AB z_BC),
Omega=D(z_AC)^-1 D(z_BC)D(z_AB)
     =D(z_AB z_BC/z_AC).
```

In additive depth coordinates the scalar triangle period is

```text
omega = delta_AB + delta_BC - delta_AC.
```

This scalar is exact only after the arrows are reduced to the owned reciprocal calibration
character (or another explicitly supplied character/local system). There is no canonical scalar
projection of a general complete mixing matrix. The terminal pair-metric formula remains exact on
each supplied regular pair cell, but three independently rebuilt terminal values do not become an
edge cocycle merely because each is readable.

Therefore the complete matrix carry closes more generally than a scalar pointwise `phi` descent.
A global point potential exists only when the appropriate scalar loop periods vanish.

## 9. Angular/mixing orchestra

The overlap product uses complete Jacobians. Off-diagonal clock/ruler/screen/mixing data are retained
before any reciprocal readout. The exact production product has all four entries nonzero, and its
diagonal-only substitute differs.

The previously banked supplied-Jacobian pair metric

```text
h=[[-3/16,1/12],[1/12,37/9]]
```

still gives

```text
det h=-7/9,
exp(4 phi_pair)=1792/81.
```

This audit changes no terminal formula. It supplies the correct complete-matrix home for comparing
multiple pair cells before asking for a scalar reduction.

## 10. Loops, branches, seams, and degeneration

- A closed sequence of composable path arrows has ordered holonomy `H`. Rebracketing does not change
  `H`; reversal gives `H^-1`. Reciprocity constrains this transformation but does not force `H=I`.
- At a cut locus, branch labels are part of the arrow. Only compatible concatenated labels compose;
  no branch is postselected.
- A lower-dimensional seam supplies only partial tangent data and cannot determine a full
  two-dimensional clock/ruler calibration transition.
- If an overlap Jacobian loses rank, a pair metric becomes null/degenerate, or no triple overlap
  exists, the inverse triangle product is undefined. Regular local readouts elsewhere survive.

No cutoff or repair is inserted at a failure stratum.

## 11. Relationship to the prior global-phi overlap audit

The August 5 audit proved that complete-coframe factorization transitions admit local presentation
shifts and do not select a unique pointwise `phi` representative. That result is unchanged.

The present audit asks a different downstream question: after complete calibrated observer-query
states and pair relations are supplied, how do their actual transitions compose? It finds exact
matrix carry on matched states and an exact obstruction/holonomy when direct and composite arrows
differ. Neither result selects the factorized depth representative or the physical global relation
family.

## 12. Downstream regrade

The earlier status

```text
ASSOCIATIVE_CALIBRATION_CARRY_NOT_OWNED
```

is too coarse. Replace it operationally with

```text
CARRY_OPERATION_AND_ASSOCIATIVITY_DERIVED_ON_MATCHED_ENRICHED_OBJECTS;
MIDDLE_OBJECT_IDENTIFICATION_AND_PHYSICAL_GLOBAL_RELATION_FAMILY_OPEN;
DIRECT_EQUALS_COMPOSITE_IS_A_SEPARATE_DESCENT_OR_HOLONOMY_QUESTION.
```

This removes the need to hunt for a new scalar equation merely to define composition. It does not
derive the physical observer relation, a global scalar `phi`, universal mixed-geometry `c_eff`, or
path independence.

## 13. Scope

The frozen arena contains 12 cases, 12 axes, and 144 classified cells. It characterizes common
atlases, separate parameterizations, independent pair surfaces, matched/mismatched middle states,
common scale, coherent reciprocal trivializations, complete mixing, branch relations, loops,
partial seams, and degenerate/missing overlaps.

No action, source, carrier, matter, mass, boundary functional, bootstrap optimizer, `X_max` value,
CMB spectrum, signalling law, preferred congruence, new scalar field, or canon statement follows.
