# Load-bearing algebra rerun contract

The semantic ledger was committed before this rerun. The rerun is deliberately narrow: it tests
the founding reciprocal character, the observer-pair distinction, the stationary Killing branch,
and the two exact presentation-nonselection witnesses. It does not rerun every conditional atlas,
because their mathematics was not adjudicated as ownership-dependent.

Each command runs from an exported clean `HEAD` tree in a fresh temporary directory so that no
historical package output is overwritten. The controller records Python/SymPy versions, exact
command, exit code, wall time, raw stdout/stderr bytes and SHA-256.

Commands, in order:

1. `python3 verify_udt_reciprocal_c_postulate.py`
2. `python3 udt_observer_pair_clock_operator_audit_2026-07-24/derive_observer_pair_clock_operator.py`
3. `python3 udt_observer_pair_clock_operator_audit_2026-07-24/verify_observer_pair_clock_operator_independent.py`
4. `python3 udt_relational_pair_depth_realization_audit_2026-07-24/derive_relational_pair_depth.py`
5. `python3 udt_relational_pair_depth_realization_audit_2026-07-24/verify_relational_pair_depth_independent.py`
6. `python3 udt_complete_physical_comparison_map_audit_2026-07-27/derive_comparison_map.py`
7. `python3 udt_complete_physical_comparison_map_audit_2026-07-27/verify_comparison_map_independent.py`
8. `python3 udt_global_phi_ownership_overlap_audit_2026-08-05/derive_global_ownership.py`
9. `python3 udt_global_phi_ownership_overlap_audit_2026-08-05/independent_global_ownership.py`
10. `python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/derive_founding_ownership.py`
11. `python3 udt_founding_phi_ownership_morphism_audit_2026-08-05/independent_founding_ownership.py`

Certification requires every command to exit zero and the semantic anchors to reproduce:

- reciprocal inverse exponentials and composition;
- observer-pair physical assignment remains open;
- stationary `delta_K=log(N(p)/N(q))`, not the opposite sign;
- local/endpoint presentation shifts leave complete physical coframes/arrows unchanged;
- no command promotes action, source, carrier, mass, density, `X_max`, signalling or dynamics.

Any failure stops the regrade. A success certifies only that the affected algebra survives its
present scoped interpretation.
