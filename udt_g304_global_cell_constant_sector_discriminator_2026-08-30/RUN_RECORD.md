# G304 run record

Date: 2026-08-30

- Device: CPU
- Production method: direct SymPy Christoffel/Ricci derivation plus exact analytic integrals and
  registry scope assertions
- Independent method: standard-library dimensionless quadrature, polynomial monotonicity/root
  census, direct invariant formulas, and arbitrary-constant network telescoping
- Production assertions: 65
- Independent assertions: 55
- Hostile mutations: 10 caught of 10
- Static domain rows: 8
- Source files frozen: 14
- Numerical observations/fits: none
- Source/action/matter/mass input: none
- Numerical scale or `X_max`: none
- Protected-package access: none

Two mechanical implementation corrections occurred before the passing replay: semantic registry
tokens were searched across complete rows rather than only `current_status`, and the independent
Simpson tolerance was set above the measured quadrature truncation error. One hostile mutation was
rewritten to test endpoint behavior rather than finiteness at a fixed cutoff. None changed the
scientific question, formulas, candidate landing, or tolerance on a load-bearing exact identity.

Fresh external review retained the bounded science with caveats and identified two replay-packaging
defects. Their repairs were preregistered at pushed commit `bb1c689e`; a corrected sealed replay
passed both permitted source layouts, rejected zero and multiple source matches, and separated
sealed commands from repository-only gates. The repair-only external follow-up returned
`REPAIRS_VERIFIED`; no scientific claim or count changed.
