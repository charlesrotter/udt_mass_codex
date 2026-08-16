# Exact derivation — G103 source-independent restriction ownership

Date: 2026-08-15

## 1. Bounded landing

The preregistered internal landing is

```text
LOCAL_REGULAR_ZERO_AND_FIRST_JET_OBSERVABLE_SURJECTION_DERIVED
__COMMON_SKY_GRAM_AND_GENERIC_MEASURE_CONSISTENCY_ONLY
__NO_NONTRIVIAL_SOURCE_INDEPENDENT_PATTERN_RESTRICTION_OWNED_IN_FROZEN_SOURCE_UNIVERSE
__GLOBAL_CRITICAL_BOOTSTRAP_AND_SOURCE_HISTORY_JOINTS_OPEN
```

This is a regular local/frozen-source ownership result. It is not a generic no-go and does not say
that a future global, singular, source, bootstrap, or dynamical law cannot restrict the observable.

## 2. What would have counted

G102 supplies the conditional map

```text
(g,Q_a,F_a) -> Psi_a=(Z_a,n_a) in R_+ x S_O^2,
cos(theta_ab)=g_O(n_a,n_b),
```

and the branch-safe pair-measure pushforward. A source-independent pattern restriction would have to
exclude at least one regular measure on these observables for every allowed source pair measure and
every allowed physical history/query realization. Positivity, one-sky typing, and generic measure
consistency are real constraints but do not meet that stronger criterion.

## 3. Zero-order local surjection

Let the supplied complete coframe be any regular

```text
E=[[B,0],[Q S,Q]] in GL(4,R).
```

For any target rank-two pair coframe `V_*` with Lorentzian pullback

```text
h_*=V_*^T eta_4 V_*,
```

define

```text
J=E^-1 V_*.
```

Then `rank(J)=2` and exactly

```text
EJ=V_*,
J^T E^T eta_4 E J=V_*^T eta_4 V_*.
```

Thus the complete coframe cannot restrict the local terminal pair coframe while the physical query
realization `J` remains supplied. The production symbolic witness uses nontrivial `B,Q,S`; the
Fraction-only replay independently reconstructs the same arbitrary regular target.

This is not a claim that a future physically owned query leaves `J` arbitrary. It says the current
metric identities do not own that additional relation.

## 4. Every common-sky pair angle is locally realizable

Fix the common observer's unit timelike vector `u_O`. For arbitrary unit vectors `n_1,n_2` in the
positive screen `u_O^perp`, positive `T_a,L_a`, and real shifts `b_a`, set

```text
V_a=[T_a u_O, b_a u_O+L_a n_a].
```

The exact G102 extraction returns the same `u_O,n_a`. Hence

```text
cos(theta_12)=g(n_1,n_2)
```

can be any value in `[-1,1]`. The exact rational witness returns `3/5` with both directions unit and
the observer clocks identical.

The common-observer condition and outward orientation remain query-owned. They type one sky; they do
not select its two-point pattern.

## 5. First-jet/time-live surjection

Differentiate `V=EJ`:

```text
dot V=dot E J+E dot J.
```

For arbitrary target first jet `dot V_*`, define

```text
dot J=E^-1(dot V_*-dot E J).
```

Then `dot(EJ)=dot V_*` identically. The production witness varies every `B,Q,S` block and uses a
generic target `dot V_*`; the independent rational implementation returns exact zero residual.

This closes only the first-jet kinematic question. It does not establish a global smooth history,
solve dynamics, cross a cut locus, or handle a singular/critical branch.

## 6. Why fixed-base positive-Gram reachability does not reverse this result

The pair-terminal atlas proves a nontrivial conditional theorem. In one fixed A-calibrated base

```text
h_0=diag(-t,ell)
```

and for a positive-semidefinite addition, a target `(A,B,Delta)` obeys

```text
0<A<=t,
B>=ell,
(t-A)(B-ell)>=t A Delta^2.
```

Within that declared chart, reciprocal depth cannot decrease. G103 independently replays an interior
positive-Gram witness with inequality margin `6`.

The shared-base and pair-calibration premises are load-bearing. Releasing the query realization gives
the exact regular witness

```text
E=diag(2,3,1,1),
V_*=diag_columns((3,0,0,0),(0,2,0,0)),
J=E^-1 V_*.
```

The base has terminal logarithmic ratio `log(9/4)/4`; the target has `log(4/9)/4`, which is lower.
No contradiction occurs: `J` changed the pair calibration/base projection, so this witness is outside
the fixed-base positive-Gram order. The atlas remains valid, but it is not a universal restriction on
the G102 accumulated endpoint observable.

## 7. Simultaneous Gram restrictions

The complete metric does restrict simultaneous tangent data. Any ambient collection has Gram matrix

```text
K=V_all^T eta_4 V_all,
rank(K)<=4,
negative_index(K)<=1.
```

At one observer, the source directions lie in a three-dimensional positive screen, so their sky Gram
matrix obeys

```text
G_ij=n_i.n_j,
G>=0,
G_ii=1,
rank(G)<=3.
```

An exact four-direction witness has rank three and zero determinant. The hostile target `I_4` has
rank four and cannot be one three-dimensional sky.

For only two directions, however,

```text
G=[[1,c],[c,1]]
```

is realizable for every `c in [-1,1]`. More generally, these Gram laws constrain a proposed matrix of
labelled pairwise cosines; they do not select the angular histogram or correlation curve. Catalogued
RA/DEC directions already satisfy them by construction.

## 8. Reciprocal network composition

Given any finite positive observer-star assignments `Z_i`, set

```text
Phi_i=log Z_i,
Z_ij=exp(Phi_j-Phi_i)=Z_j/Z_i.
```

Then exactly

```text
Z_ij Z_jk=Z_ik,
Z_ji=1/Z_ij.
```

Thus endpoint composition constrains a fully measured closed network, but it does not restrict an
arbitrary positive star of redshifts from one observer. G103 verifies all 125 triple compositions and
25 reversals for a five-object rational witness.

This is conditional endpoint descent on one coherent calibration family. It is not a history or
relation-family selector.

## 9. Pair-measure freedom survives fixed one-point data

Use four sky labels with uniform one-point marginal and directions

```text
{+e1,-e1,+e2,-e2}.
```

Three exact symmetric couplings share the same marginal:

1. identity pairing: all mass at angle `0`;
2. quarter-turn involution: all mass at angle `pi/2`;
3. antipodal involution: all mass at angle `pi`.

Each row and column marginal is exactly `(1/4,1/4,1/4,1/4)`. Therefore even the one-point sky measure
does not determine the two-point angular pattern when the source pair measure is free.

The continuum statement is stronger: for any probability law `rho` on `[-1,1]`, take `n` uniformly
on `S^2`, draw `c` from `rho`, and draw `m` uniformly on the circle `n.m=c`. The resulting rotationally
invariant symmetric coupling has uniform marginals and angle-cosine law `rho`. This is a measure
construction, not a physical source model.

Positivity, symmetry, factorial self-pair conventions, marginal compatibility, cap/shell additivity,
and estimator normalization remain real generic measure constraints. They do not originate in the UDT
history equations and do not select one angular curve.

## 10. Candidate disposition

The frozen ten-class outcome is recorded in `RESTRICTION_ATLAS.tsv`:

- regular support/common observer: derived typing only;
- fixed-base positive-Gram order: exact but conditional, not universal;
- zero-order and first-jet complete-pair maps: locally surjective while `J` is supplied;
- ambient/sky Gram laws: derived simultaneous realizability constraints only;
- endpoint composition: derived network coherence without star selection;
- measure consistency: generic, with exact nonuniqueness at fixed marginal;
- criticality, topology, physical completion, bootstrap, and joint source-history law: open.

## 11. Maximum justified conclusion

Within the frozen sources and regular local/first-jet class, the complete metric currently evaluates
rather than predicts the G102 two-source observable. It supplies lawful support and assembly, but no
nontrivial source-independent angular/redshift pattern restriction survives the released physical
history/query/source degrees of freedom.

The next empirical step therefore cannot pretend to be parameter-free. Before opening BOSS, it must
preregister an explicit source-pair admissibility premise or a genuinely owned joint source-history
law. Global criticality, noninjectivity, topology, bootstrap, and singular completion remain legitimate
future places where a restriction could emerge.
