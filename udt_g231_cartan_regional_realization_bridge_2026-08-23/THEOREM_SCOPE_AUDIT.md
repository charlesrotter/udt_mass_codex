# G231 standard-theorem scope audit

Date: 2026-08-23

This file sharpens the preregistered reference boundary without modifying any frozen pre-outcome
file.

## Finite-dimensional `G`-realization data

Fernandes--Struchiner, *The Global Solutions to Cartan's Realization Problem*
(arXiv:1907.13614), supplies the load-bearing finite-dimensional result. Its Theorem 4.3 identifies
Cartan data defining a `G`-structure algebroid with the data required for `G`-realizations.
Corollary 4.5 gives the source-fiber model when the algebroid is `G`-integrable, and the local form
of Theorem 6.1 supplies a realization near a point on a transitive leaf under the stated local
`G`-integrability hypotheses.

G231 may therefore say:

```text
finite classifying data satisfying the full G-structure-algebroid,
equivariance, action, regularity, and local G-integrability hypotheses
  -> conditional local G-realization
```

The quotient may be an effective orbifold when the group action is only locally free. An ordinary
Lorentz manifold requires the relevant `SO(1,3)` action to be free/principal, equivalently no
unresolved local isotropy in the quotient. G231 may not silently promote local realizability to a
global metric.

## `G`-structures with connection

Fernandes--Struchiner II associates a classifying Lie algebroid to a **fully regular** `G`-structure
with connection and relates `G`-realizations to such structures. This validates the category used
for an orthonormal frame and connection, but it delegates actual realization to the
`G`-integrability machinery above. It does not prove that an arbitrary UDT curvature prescription
is fully regular, finite type, `G`-integrable, or physically selected.

## Infinite/PDE data

Fernandes--Smilde defines a relative Lie algebroid to be formally integrable. Its Theorem 3.20
states existence of a realization through each prolongation point for an **analytic relative Lie
algebroid**. Thus both analytic regularity and formal integrability are hypotheses. Its Section 7.2
also explains why this coframe realization theorem does not generally produce a principal
`G`-bundle.

G231 may therefore say:

```text
analytic formally integrable relative-algebroid data
  -> conditional local coframe realization
```

It may not promote this to principal `SO(1,3)` descent, arbitrary smooth data, convergence of every
formal jet, global existence, completeness, value generation, or physical-history selection.

## UDT ownership boundary

All three references are standard mathematical machinery. None supplies:

- a UDT curvature profile;
- a UDT classifying invariant map or derivative law;
- populated observer/null relations;
- selected transport;
- a global physical history.

Those remain separate UDT ownership questions.
