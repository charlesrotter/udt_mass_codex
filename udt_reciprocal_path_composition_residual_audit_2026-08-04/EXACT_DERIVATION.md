# Exact reciprocal path-composition derivation

## 1. The founding sentence has a precise scope

The founding packet says that comparisons “compose consistently through an intermediate
position.” In the controlling derivation this becomes

```text
D(b) D(a) = D(a+b),
D(a)=diag(exp(-a),exp(a)).
```

The frozen semantic census already distinguishes this Cauchy/character composition from comparing
two spacetime paths with the same endpoints. The founding formula contains no metric, connection,
path, loop, topology, or holonomy variable. It derives the real reciprocal representation after an
additive depth has been supplied.

Because the real exponential character is faithful,

```text
D(Pi)=I  iff  Pi=0.
```

This makes a nonzero supplied loop period observable in the reciprocal character. It does not say
that all physical loop periods must vanish.

## 2. Composition is nontrivial on free depth data but tautological on potentials

Use four observer objects and the six oriented edges `i<j`. Let `B` be the `6 x 4` incidence matrix
and `C` the `4 x 6` triangle-residual matrix. Exact calculation gives

```text
rank(B)=3,
ker(B)=span(1,1,1,1),
rank(C)=3,
C B=0,
ker(C)=image(B).
```

Thus triangle composition is a genuine rank-three restriction on six independently supplied edge
depths. But if the edges come from any endpoint potential,

```text
delta_ij=phi_j-phi_i,
```

then every triangle residual vanishes identically. Its Jacobian with respect to the endpoint values
of `phi` is zero. Composition reconstructs relative potentials from already-consistent edge data;
it does not select a realized potential.

Three nonconstant exact potential witnesses pass, while one free non-coboundary edge cochain fails.
The distinction is therefore not a zero-depth or vacuous test.

## 3. It does not select a reciprocal metric profile

For the exact reciprocal two-dimensional metric block

```text
ds^2=-exp(-2 phi(x)) dt^2 + exp(2 phi(x)) dx^2,
```

the scalar curvature is

```text
R=2(phi''-2(phi')^2) exp(-2 phi).
```

The profiles `phi=0`, `phi=x`, and `phi=x^2` have respective curvature values `0,-4,+4` at
`x=0`. All three nevertheless satisfy exact endpoint character composition between `x=0,1,2`.
This bounded control does not classify complete metrics; it proves that the composition identity
does not itself impose a profile equation even inside the founded reciprocal block.

## 4. Path integration separates additivity from flatness

For any supplied one-form `alpha`,

```text
delta_gamma = integral_gamma alpha
```

adds under path concatenation by definition. On the unit-square control:

```text
alpha_exact = d(x^2 y + 3x)       has d alpha=0 and loop period 0;
alpha_nonclosed = (-y/2)dx+(x/2)dy has d alpha=dx wedge dy and loop period 1.
```

Both forms obey path-concatenation additivity. Therefore:

```text
path additivity  does not imply  d alpha=0.
```

Local endpoint independence would add `d alpha=0`. Global endpoint independence would further add
zero periods on every loop. Those are increasingly strong restrictions, and neither is owned by
the founding composition source.

If `alpha=d phi`, then `d alpha=d^2 phi=0` is an identity. It is not an equation selecting `phi`.

## 5. Metric transport composes for every supplied metric

Levi-Civita transport is functorial:

```text
U_(beta o alpha)=U_beta U_alpha.
```

For an ordered pair-frame generator `X_A`, transport gives

```text
X_B=U_alpha X_A U_alpha^-1,
D_B(b) U_alpha = U_alpha D_A(b).
```

Hence, if depth is additive,

```text
T_alpha=U_alpha D_A(a),
T_beta=U_beta D_B(b),
T_beta T_alpha=U_beta U_alpha D_A(a+b).
```

The production calculation verifies this with two exact rational, noncommuting Lorentz boosts and
nonzero depths `log 2` and `log 3`; the independent standard-library calculation reconstructs it
with rational matrices. This is exact typed kinematics for every supplied metric/path/pair input,
not a field equation restricting the metric.

Levi-Civita transport and reciprocal dilation remain different objects. In the physical
orthonormal control, the former preserves `eta`, while nonzero `D` does not. Neither may be called
the other.

## 6. A nontrivial loop residual exists only after an extra premise

A typed loop can contain two independent contributions:

```text
Pi_gamma = reciprocal depth period,
H_gamma  = Levi-Civita holonomy,
T_gamma  = H_gamma D(Pi_gamma)     (with the required transported typing).
```

Composition permits `T_gamma` to be a nonidentity automorphism. It does not demand `T_gamma=I`.
Imposing identity return would be a genuine global restriction on depth periods and metric
holonomy. It would also choose endpoint-collapse/trivial-loop semantics that the source census
marks open.

The bounded historical holonomy controls show that full endpoint closure can fail while path-labelled
composition remains exact. They are controls against the implication; they are not proposed UDT
topologies or physical branches.

## 7. Observer Reciprocity is a gate, not a residual generator

Observer-frame Reciprocity requires any future law to transform naturally/equivariantly and its
solution set to be observer-orbit saturated when the codomain zero is preserved. Multiple
inequivalent laws satisfy that requirement. Pair cocycles likewise reconstruct relative depths
only after the pair data are supplied.

Therefore neither covariance nor universal-all-query admissibility promotes character composition
into a nontrivial metric equation.

## 8. Source-complete ruling

All 32 frozen sources are individually adjudicated in `SOURCE_ADJUDICATION.tsv`. Their common
logical chain is:

```text
founded reciprocal pair + additive comparison
    -> faithful real character and exact abstract composition;

supplied metric + path + pair + additive depth
    -> exact typed path-groupoid comparison;

current foundation
    -/> metric-native signed depth assignment;
    -/> endpoint-only or path-labelled physical semantics;
    -/> local flatness or global zero periods;
    -/> trivial full-loop return;
    -/> UNIVERSAL_ALL_QUERIES as dynamics;
    -/> nontrivial metric residual.
```

The only nontrivial metric/path residual in the registered universe is conditional: first supply a
metric-dependent depth rule and separately require endpoint/path independence or trivial loop
return. Current sources supply neither join.

## 9. Termination ruling

```text
FOUNDED_RECIPROCAL_COMPOSITION_IS_EXACT_NONSELECTING_KINEMATICS;
IT_RESTRICTS_FREE_DEPTH_DATA_BUT_IS_IDENTICALLY_SATISFIED_BY_EVERY_ENDPOINT_POTENTIAL;
PATH_ADDITIVITY_DOES_NOT_DERIVE_LOCAL_FLATNESS_OR_GLOBAL_ZERO_PERIODS;
LEVI_CIVITA_AND_SEMIDIRECT_TRANSPORT_COMPOSE_FOR_EVERY_SUPPLIED_METRIC;
NONTRIVIAL_LOOP_RESIDUAL_REQUIRES_AN_UNSELECTED_EXTRA_SEMANTIC_AND_DEPTH_PREMISE;
NO_SOURCE_BACKED_METRIC_RESIDUAL_OR_UNIVERSAL_DYNAMICAL_QUANTIFIER_IS_DERIVED.
```

The present composition-to-native-residual route terminates. It may be reopened only by a new
source-backed metric-native depth law or loop/endpoint premise, not by further classification of
the same identity.

