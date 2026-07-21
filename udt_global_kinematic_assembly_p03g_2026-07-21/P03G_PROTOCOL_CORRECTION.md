# P03G execution-order correction

The frozen complete-map protocol currently places `P04 / DYNAMICS_BRANCH_RULING` immediately after
the point-local founded-constraint atlas and reserves `P11 / GLOBAL_SOLUTION_CLOSURE` for completed
solutions downstream of dynamics.

P03G changes neither record. It inserts one narrower question between them:

```text
P03  point-local founded constraints
  |
P03G pre-dynamics global kinematic assembly requirements
  |
P04  owner-ruling on a dynamics lane, if and when explicitly authorized
  |
...
P11  global closure of actual solutions
```

This correction was required because P03 proved completeness only for a registered point-local
two-jet atlas. A global finite-cell configuration additionally needs a cover, overlap cocycle,
complete field/coframe transition law, seal lift, boundary/corner data, topology, and treatment of
degenerate closures. Asking which local differential law to solve before recording those axes would
silently convert missing global data into hidden boundary or topology choices.

P03G is not P11. It does not solve a field equation or classify global solutions. It records the
assembly type signature, applies only already-derived compatibility relations, and preserves an
explicit unenumerated remainder wherever the present evidence is not exhaustive.

The frozen `FUTURE_ATLAS_PROTOCOL.tsv`, P00--P03 packages, and all prior evidence remain unchanged.

