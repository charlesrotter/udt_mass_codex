# Exact derivation — open neighborhoods of intrinsic reciprocal pairs

## 1. Scope and premise boundary

This is an off-shell configuration-space theorem for the fixed complete `R x S3` coframe family.
It carries, but does not promote, the four required stamps:

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

The theorem does not use co-presence, an action, a source, or a solution law. It therefore survives
replacement of the co-presence interpretation.

## 2. Configuration topology

For a smooth function `phi` on the compact `S3`, real `a` and `lambda`, and positive coframe scale
`R`, use

```text
tau     = dt + a sigma_3,
theta_0 = exp(-phi) tau,
theta_1 = R exp(+phi) sigma_3,
theta_2 = R exp(lambda phi) sigma_1,
theta_3 = R exp(lambda phi) sigma_2,
g       = -theta_0^2 + theta_1^2 + theta_2^2 + theta_3^2.
```

The parent unit calculation is the slice `R=1`; restoring a positive `R` changes no local
continuity claim. A curvature scalar depends on the metric two-jet, and its first derivative depends
on the metric three-jet. Hence the determinant certificate below is a continuous function on

```text
C3(S3) x R_a x R_lambda x R_positive.
```

This is the weakest standard integer-derivative topology used by this audit. It is not a proposed
physical norm.

## 3. Curvature-rank gate

At the fixed certificate event `p`, let

```text
D_p(phi,a,lambda,R) = det[dI1,dI2,dI3]_spatial,
```

where `I1`, `I2`, and `I3` are scalar curvature, Ricci squared, and Kretschmann scalar of the
complete four-metric. Metric inversion is smooth on the nondegenerate metrics. Differentiation,
finite tensor products and contractions, and evaluation of a three-jet at `p` are continuous.
Therefore `D_p` is continuous in the declared product topology.

The six exact parent values are nonzero rational numbers; they are reproduced in
`DERIVATION_RESULT.json`. Since the inverse image of `R` without zero under a continuous map is
open, each C01–C06 lies in a neighborhood with `D_p != 0`. The parent Killing-transport proof then
continues to identify the unique continuous stationary clock line throughout each such
neighborhood.

No explicit radius is claimed. Certifying one would require a quantitative bound on the variation
of `D_p`, which this audit does not compute.

## 4. The other strict gates

### Nontrivial reciprocal depth

For continuous profiles,

```text
|osc(phi)-osc(psi)| <= 2 ||phi-psi||_infinity.
```

The frozen polynomial has `f(+e1)=5` and `f(-e1)=-1`; with `phi=f/50`,

```text
osc(phi) >= 6/50 = 3/25 > 0.
```

Thus nontrivial depth is open already in the weaker `C0` topology.

### Nonzero twist and ruler line

For the global `S3` Maurer-Cartan coframe, `kappa=-2`, while all six centers have `a=1/64`. Hence

```text
|a kappa| = 1/32 > 0.
```

The clock twist is continuous in `a`, and its direction remains exactly the reciprocal ruler line
for every member of this coframe family. The twist-selected ruler gate is therefore open.

### Positive displayed stationary slice

The required global function, with the positive coframe scale restored as preregistered in the
correction layer, is

```text
m(phi,a,R) = min_S3 [R^2 exp(4 phi)-a^2].
```

The compact minimum is continuous under uniform profile changes and ordinary changes of `a` and
positive `R`. At all six frozen centers `R=1`. The frozen coefficient bound gives
`|phi|<=29/50<1`. Since `e<3`,

```text
exp(4phi)-a^2 > 1/81 - 1/4096 = 4015/331776 > 0.
```

This exact lower certificate holds on the whole displayed slice, not just at `p`, so its positive
set is open in `C0(S3) x R_a x R_positive`.

### Global coframe

Smooth functions on compact `S3` are finite. All exponential factors are strictly positive, and the
coframe determinant remains nonzero for positive `R`. That is an open condition in the registered
family. The Maurer-Cartan forms themselves remain global and are not deformed here.

## 5. Joint theorem

Each of the five gate sets is open in the declared product topology. Their finite intersection is
open. Because every C01–C06 center lies in that intersection, each has a joint `C3` neighborhood in
which the same complete metric intrinsically supplies the clock line and, through its twist, the
reciprocal ruler line.

This proves that the all-gate property is not an isolated coefficient coincidence within the fixed
configuration topology. It does not prove that the set is dense, generic, large in measure, on
shell, stable, or physically selected.

## 6. Degeneration atlas

- `D_p=0`: this three-invariant certificate loses rank. Another event or invariant set may still
  identify the clock; extra symmetry is not proved.
- `a kappa=0`: this clock-twist route no longer supplies the ruler line. In the fixed `S3` coframe,
  `kappa=-2`, so this occurs at `a=0`.
- `osc(phi)=0`: the reciprocal depth becomes constant, although a stationary line may remain.
- `m(phi,a)=0`: the displayed stationary slice reaches its causal boundary. This alone is not a
  complete-spacetime curvature singularity.
- zero scale or loss of finite smooth coframe data: the registered coframe fails, without excluding
  another completion.
- intersections: multiple gates fail, but no physical phase transition follows without a law.
- absent on-shell selector: the configuration remains mathematically available but physically
  unselected.

The exact machine-readable rulings are in `DEGENERATION_STRATUM_OUTCOMES.tsv`.

## 7. Exact bounded verdict

```text
ALL_GATE_INTRINSIC_PAIR_CONFIGURATIONS_CONTAIN_OPEN_C3_NEIGHBORHOODS_AROUND_C01_TO_C06_IN_THE_FIXED_COMPLETE_S3_FAMILY;
STRUCTURAL_AVAILABILITY_IS_NOT_FINE_TUNED_WITHIN_THIS_CONFIGURATION_TOPOLOGY;
NO_EXPLICIT_RADIUS_OR_PHYSICAL_SELECTION_IS_DERIVED.
```
