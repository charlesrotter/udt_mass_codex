# Preregistration: clean-room metric-reduction readiness audit

Date: 2026-07-27

## Whole question

Does the currently founded UDT reciprocal pair, together with any complete
four-dimensional structure already supplied by the metric, close either

1. an ODE/cohomogeneity-one system that determines metric configurations, or
2. a low-dimensional time-live system that determines their evolution,

without importing an action, field equation, source, carrier, boundary law,
bootstrap equation, strong local CSN, GR dynamics, or a previous solver's
equations?

The audit separately asks which ODEs are already closed **on a supplied metric**
(geodesic, parallel-transport, screen-connection, and Jacobi systems). A closed
transport ODE must not be promoted to a closed metric/background equation.

## Frame and scope

This is a metric-led readiness audit, not a target solve. It uses the current
founded reciprocal pair and the registered complete-coframe extension class.
It tests:

- a clean cohomogeneity-one reduction with every surviving amplitude live;
- a clean `1+1` time-dependent reduction with every surviving amplitude live;
- the stationary twisted-`S3` and reduced-product witnesses only as registered
  conditional controls;
- intrinsic path equations on a supplied configuration; and
- exact closure rank, constraints, gauges, inequalities, and missing data.

It does not claim to enumerate every possible higher-jet or nonlocal UDT law,
every topology, or every coordinate reduction.

## Clean-room quarantine

Before the result is fixed, no previous ODE/time-live implementation, input,
output, notebook, or solver-specific equation may be opened or imported. Their
filenames and tracked metadata may be inventoried only after the clean-room
classification is complete. Later comparison is provenance/adversarial work,
not an equation source.

## Unknowns and premise tags

The general bounded triangular chart has the current eight configuration
amplitudes

```text
(phi,sigma,alpha,k,S10,S11,S20,S21).
```

`phi` is not an extra scalar: it is the founded log-depth readout of the
reciprocal pair. Its realized profile is nevertheless free because no current
law selects that profile. The other seven amplitudes are a complete bounded
chart, not seven asserted physical fields.

Every premise is frozen in `PREMISE_LEDGER.tsv`. In particular:

- `c_E` is an observed calibration anchor;
- strong local CSN is inactive;
- no action, source, carrier, density law, physical boundary, or bootstrap
  optimizer is active;
- symmetry reductions are `CHOSE_REDUCTION_CONTROL`, not selected physics;
- profiles, admissible branches, and boundary data are characterized rather
  than filtered for a desired shape.

## Closure definitions

For `m` reduced configuration functions `q^A(s)`, a first-order background ODE
is closed only if the current premises supply `m` independent differential
relations whose principal map solves for all `q'^A`, after explicitly stated
coordinate/frame gauge. Inequalities, definitions of connection/curvature,
Bianchi identities, and boundary regularity do not count as evolution laws.

For a `1+1` system `q^A(t,x)`, closure requires an evolution principal symbol
for every physical configuration direction plus propagated constraints and a
declared characteristic/boundary domain. A method-of-lines discretization
cannot supply a missing continuum equation.

A path equation is closed only conditionally on a supplied sufficiently smooth
metric, path/initial data, and any required screen reduction. Such closure is
classified `CLOSED_KINEMATIC_ON_SUPPLIED_CONFIGURATION`.

## Preregistered tests

1. Derive the clean one-coordinate coframe jet map without consulting legacy
   solver equations.
2. Count live configuration functions, coordinate/frame presentation freedom,
   metric-supplied differential equations, and unresolved principal directions.
3. Distinguish Cartan definitions and identities from constraints or response
   equations.
4. Repeat the rank accounting for a `1+1` time-dependent chart.
5. Derive the geodesic, ambient parallel-transport, projected-screen, and
   Jacobi first-order systems and state all supplied inputs.
6. Test the stationary twisted-`S3` and constant-depth reduced witnesses without
   inferring selection or evolution.
7. Classify every candidate in `CANDIDATE_SYSTEMS.tsv` exactly once.
8. Exercise every false-promotion catch in `FALSIFICATION_CONTRACT.tsv`.
9. Reconstruct the load-bearing rank and type classification with a separate
   implementation that does not import production code.
10. Only after the verdict is frozen, inventory and compare prior solver
    equation families by provenance. Do not execute them.

## Certification and falsification

A metric-background ODE is certified only if all closure definitions above
pass and every equation has current UDT provenance. Finding only kinematic path
ODEs falsifies authorization for a metric-configuration or time-live solve.

A negative result is bounded: it means the registered current premises do not
close the tested reductions. It is not a theorem that no future metric-native
global, higher-jet, variational, or bootstrap closure can exist.

## Maximum conclusion

At most this audit may say:

- which tested systems are metric-derived and closed on supplied configurations;
- whether a clean metric-configuration ODE or `1+1` time-live system is presently
  closed;
- the exact unresolved configuration directions and missing equation type; and
- whether a coarse solve is authorized now.

It may not select an extension, branch, profile, topology, boundary, action,
source, carrier, density, bootstrap law, `X_max`, mass, or physical dynamics.
It may not run legacy solvers, GPU work, or a numerical background evolution.
