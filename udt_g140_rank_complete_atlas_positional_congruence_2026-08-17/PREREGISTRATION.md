# G140 preregistration — rank-complete atlas versus positional congruence

Date: 2026-08-17

## Whole bounded question

Determine whether one regular matched-calibration rank-complete network of full pair pullbacks from
one Lorentz metric automatically induces the composition-compatible positional route congruence
required by G139, or whether metricity and positional descent are independent conditions.

## Frame and premise ledger

- Method: metric-led exact finite observer-network construction; no fit, dynamics, or selector.
- Arena: Minkowski metric with `c_E=1`, four static observer worldlines, six affine timelike pair
  strips, one shared clock calibration, one dimensionless pair-strip parameter, regular nondegenerate
  pullbacks, and G137/G138 signed terminal-depth convention.
- `DERIVED`: complete pullback formula; G129 rank-ten faithfulness; G138 cycle criterion; G139
  conditional endpoint-position/path-transport typing.
- `CHOSE / PROVISIONAL`: G139 endpoint positional ownership within each supplied congruent physical
  relation family.
- `FREE_AND_EXPLORED`: observer spatial positions and hence the six affine pair-strip ruler vectors.
- `OPEN/OMITTED`: physical selection of observers, pair strips, routes, or congruence; time-live and
  singular strata; `X_max` value; proper length identification; light/EM, observations, bootstrap,
  action, source, matter, mass, and dynamics.

The affine strip length is a metric/query witness used inside `h=F^*g`; it is not promoted to UDT
proper distance or a physical route selector.

## Preregistered nonclosing witness

Use static worldlines through spatial vertices

```text
A=(0,0,0), B=(1,0,0), C=(0,1,0), D=(0,0,1)
```

and for every unordered pair `i,j` the affine strip

```text
F_ij(y,s)=(y,(1-s)p_i+s p_j),  0<=s<=1.
```

Its pullback is

```text
h_ij=diag(-1, |p_j-p_i|^2),
phi_ij=(1/2)log|p_j-p_i|
```

in the registered increasing-label orientation, with `phi_ji=-phi_ij`. Preregister:

1. all six strips are regular Lorentzian;
2. the six pair-plane restriction design has exact rank ten;
3. every `h_ij` is an exact pullback of the same Minkowski metric;
4. triangle `A-B-C-A` has exact nonzero residual `log(2)/4`;
5. therefore rank-complete metricity does not imply positional descent.

## Preregistered closing control in the same metric

Use a regular Euclidean tetrahedron of unit side length:

```text
A=(0,0,0)
B=(1,0,0)
C=(1/2,sqrt(3)/2,0)
D=(1/2,sqrt(3)/6,sqrt(2/3)).
```

Apply the same affine-strip construction and shared calibration. Preregister:

1. all six pair lengths equal one, hence every terminal depth and cycle residual is zero;
2. the six pair-plane design still has exact rank ten;
3. the ambient metric is the same Minkowski metric as the nonclosing witness.

If both witnesses pass, no predicate of `g` alone can distinguish the closing from nonclosing
observer-query family. Under the adopted G139 clarification, positional congruence is then a
nonidentity admissibility condition on the relation family/query network, not a metric-history
equation.

## Certification and maximum conclusion

Production exact algebra must compute all pullbacks, ranks, lengths, terminal depths, reversals, and
independent cycle residuals. An independent implementation must use a separate rank algorithm and
numerical/log-ratio replay, plus frozen source hashes. A fresh adversarial review must attack unit
typing, matched calibration, route composability, and any overreach from the finite witness.

Maximum possible landing:

```text
RANK_COMPLETE_FULL_PULLBACK_METRICITY_DOES_NOT_IMPLY_POSITIONAL_ROUTE_CONGRUENCE__
THE_SAME_METRIC_SUPPORTS_CLOSING_AND_NONCLOSING_REGULAR_RANK_COMPLETE_QUERY_NETWORKS__
G139_CONGRUENCE_IS_A_NONIDENTITY_RELATION_FAMILY_ADMISSIBILITY_CONDITION_NOT_A_METRIC_EQUATION__
PHYSICAL_FAMILY_VALUES_HISTORY_XMAX_AND_GLOBAL_COMPLETION_OPEN
```
