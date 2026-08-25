# G261 preregistration

Date: 2026-08-25

## Question

Does F1--F4/W1/W3 plus provisionally adopted W4 derive the G259 conservative parent-operator class,
and does W4 change the primary metric form?

## Candidate landings

1. `W4_DERIVES_COMPLETE_G259_OPERATOR_CLASS`
2. `W4_OWNS_PROPER_SUBSET__ONE_DYNAMICS_PREMISE_REMAINS`
3. `W4_ONLY_RESTATES_SUPPLIED_METRIC_EVALUATION`
4. `W4_CONFLICTS_WITH_RECIPROCAL_FINITE_SEPARATION_READOUT`

No landing is preferred after evidence inspection.

## Fixed W4 scope

W4 asserts:

- one completed UDT metric supplies local clock/ruler calibration, free-fall connection, and null
  cone;
- freely falling local frames recover special relativity with local `c_E`;
- conditional pair `c_eff` is not promoted to a second local signal speed;
- no post-readout force or independent propagation metric is added.

W4 does not textually assert an action, field equation, source, locality, derivative order,
divergence identity, or boundary/initial data.

## Ownership tests

For each item return exactly one of `DERIVED_FROM_W4`, `SUPPORTED_ACCEPTANCE_REQUIREMENT`, or
`NOT_DERIVED_FROM_W4`:

1. one universal physical metric;
2. Levi-Civita local inertial/free-fall evaluator;
3. diffeomorphism naturality of a future physical law;
4. metric-only gravitational state;
5. symmetric rank-two equation;
6. pointwise locality;
7. at most second metric differential order;
8. identity divergence freedom;
9. nonidentity parent residual;
10. source/history values.

## Separating controls

- The G259 `R^2` Euler tensor retains universal metric coupling but violates second order.
- A covariant nonlocal metric functional can retain universal metric coupling but violates locality.
- A scalar metric equation such as `R=0` retains one metric but is not a rank-two operator.
- `R_ab` is a natural local second-order rank-two tensor but is not identity-divergence-free.
- A universally matter-coupled metric plus an auxiliary gravitational scalar satisfies equivalence
  semantics while violating metric-only state closure.
- The zero residual is compatible with W4 semantics but selects no history.

These are logical separators, not proposed UDT mechanisms.

## Metric-change test

The primary metric may be called changed only if W4 algebraically alters a coefficient, adds a
field/component, or changes F1--F4's implication chain. A change of physical interpretation or
universal coupling alone does not count as a changed metric.

## Certification contract

- exact implication and countermodel table;
- explicit distinction between local inertial kinematics and field dynamics;
- no angular deletion, radial-only substitution, or imported Einstein equation;
- independent implementation must reproduce every classification from the frozen premise strings;
- at least six hostile mutations must be caught;
- maximum conclusion: bounded premise-ownership theorem, not a UDT field equation.
