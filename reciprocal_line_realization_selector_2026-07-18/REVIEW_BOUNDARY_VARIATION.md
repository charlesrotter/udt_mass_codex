# Fresh read-only review — boundary and variation audit

Reviewer: `/root/line_selector_boundary_variation_audit`  
Mode: read-only; no file changes  
Verdict: `ACCEPT_WITH_CORRECTIONS`

The reviewer accepted the bounded selector result and confirmed that it derives no required
auxiliary field or full coframe. Required corrections, applied before freeze:

1. `phi=0` was separated from `d phi=0`; only critical/constant regions defeat a gradient selector.
2. A Killing field for `g` need not remain Killing for `Omega^2 g` unless its flow preserves
   `Omega`; the route now requires a representative or CSN-compatible conformal formulation.
3. The flat-jet theorem is stamped to the preregistered unrestricted Lorentz class. `phi=0` alone is
   not treated as proof of flatness, and the native off-shell domain remains open.
4. The collar counterexample uses a spacelike tangential direction and bounded coefficient when
   causal character matters; it proves nonuniqueness among smooth extensions, not within every
   separately prescribed extension algorithm.
5. Real zero sets replace structural SymPy inequalities, and the analytic T3 proof is distinguished
   from its executable anchors.

The reviewer independently confirmed the downstream firewall: `C^2`/Bach remains
`UNIQUE-CONDITIONAL`; EH remains `CONDITIONAL`; the variation domain, two-stage bridge,
shared-static-source route, complete action, carrier/source, differentiable boundary action,
charge, and mass remain `OPEN`.

No files were changed by the reviewer.
