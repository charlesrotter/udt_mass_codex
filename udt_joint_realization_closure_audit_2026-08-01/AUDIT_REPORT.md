# UDT joint-realization closure audit — report

Date: 2026-08-01

Base: `089e2044be1b2e801f9b4f07e83efb5296dc1375`

Preregistration: `1f79c4b`

Mode: CPU-only, metric-led, observing rather than targeting

## Result first

**Outcome: `FORMAL_COMPATIBILITY_ONLY_COMMON_REALIZATION_OPEN`.**

The current record contains exact reduced stationary P4 solutions and exact formal time-live and
angular-live modules. It does **not** yet contain one nonzero time-and-angular finite-cell field that
solves one native whole-system equation, obeys one differentiable boundary/completion problem, and
uses one compatible premise stack.

This closes a bookkeeping ambiguity rather than the physics gap. The missing object is now typed
precisely as a native joint-realization certificate, `JR_CERT_NATIVE`. The certificate includes the
whole problem and an actual nonzero-live solution. It need not be packaged as an action; bootstrap
or another metric-native whole-solution operation could in principle supply it.

Native stability therefore remains `CONDITIONAL_STABILITY_ONLY`. The separate persistence join is
still downstream and was not tested here.

## Decisive distinctions

1. **Stationary solution is not live lift.** The Route-A stationary solution families are exact in
   their scopes, but Slice 2b explicitly excludes time-live work.
2. **Formal module is not solved field.** T2 says no response law is selected and no solve is
   performed. A3 says nonzero angular-live on-shell coexistence is unproved.
3. **Completion type is not boundary-value problem.** All twelve frozen completion rows lack a
   complete same-solution witness and response; the differentiable finite-cell boundary action is
   open.
4. **Bootstrap diagram is not bootstrap closure.** The two-arrow architecture is exact as a type,
   but neither arrow nor a common fixed point is registered.
5. **Conditional physics cannot be spliced.** The conditional action and carrier branches do not
   share a complete field/equation/boundary/live solution, and their premise stamps remain intact.

`JOINT_GATE_MATRIX.tsv` records the twelve gate objects. `ROUTE_ADJUDICATION.tsv` records all eight
routes. Zero constructive route passes the complete gate.

## Exact controls

Five finite-set controls independently establish the load-bearing logic:

- time-live and angular-live sets can each be nonempty while their common set is empty;
- a shared zero mode can pass every formal clause while both live predicates vanish;
- equation and boundary solution sets can each be nonempty but disjoint;
- clauses from incompatible premise branches can look complete only after an illegal splice; and
- a complete problem specification can exist while its nonzero-live solution set is empty.

These are mathematical controls, not candidate UDT laws. The deterministic checker passes 31/31
checks and catches 9/9 exercised mutations.

## Falsifier disposition

| Falsifier | Result | Reason |
|---|---|---|
| F1 explicit native witness | Not fired | No complete certificate occurs in the frozen record. |
| F2 native equation found | Not fired | Complete native action/response remains open. |
| F3 native boundary found | Not fired | Differentiable finite-cell boundary/completion remains open. |
| F4 same nonzero live on-shell field found | Not fired | T2/A3 and cold Q2 explicitly stop below this quantifier. |
| F5 bootstrap arrows found | Not fired | The record supplies a type skeleton, not both maps or a fixed point. |
| F6 route omission | Clean | All eight preregistered routes are populated. |
| F7 zero-mode promotion | Clean | Liveness is required and mutation-tested. |
| F8 conditional merge | Clean | Action, carrier, reading, posture, and completion premises remain separate. |
| F9 import or target | Clean | No external theory, desired solution, particle, or stability filter enters. |

## What remains valid

- founded reciprocal `phi` and the observed `c_E`/`G_obs` anchors retain their current labels;
- complete reciprocal coframe configurations remain a derived off-shell existence class;
- all exact P4 stationary, time-module, and angular-module results survive in their stated scopes;
- the conditional static finite-box Hopfion result survives unchanged; and
- bootstrap remains a coherent working global/local closure architecture.

No prior result is weakened merely because it is not the common certificate.

## Four evidence gates before banking

1. **Preregistered:** yes, commit `1f79c4b` precedes route-content adjudication.
2. **Full or bounded:** complete for the 140-source frozen universe, twelve gate objects, and eight
   preregistered routes; not universal over unknown UDT laws.
3. **Independent:** production logic and mutation checks pass; a fresh zero-context adversarial
   verifier is required before the final package is banked.
4. **Premises:** 17 premise rows are frozen and every conditional branch retains its stamp.

## Next scientific gate and stop line

The next scientific object is not T4 and not another stability eigenvalue. It is construction or
derivation of `JR_CERT_NATIVE`: one native whole-system finite-cell problem plus one actual field
with both live sectors nonzero. Only afterward is the persistence join well posed.

This audit does not authorize construction of that law in the same outcome pass. It selects no
action, carrier, boundary, branch, source, mass, or bootstrap map; launches no GPU solve; edits no
navigation; and does not integrate into `grok`.
