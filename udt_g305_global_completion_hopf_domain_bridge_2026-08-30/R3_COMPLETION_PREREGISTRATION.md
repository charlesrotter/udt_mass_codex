# G305 R3 completion preregistration

Date: 2026-08-30
Status: `PREREGISTERED_BEFORE_R3_COMPLETION`
Trigger: external repair-follow-up verdict `REPAIRABLE_DEFECTS_REMAIN`

## Frozen defect

The first R3 repair mutated only a separate `promotions` set. It did not mutate the computed G305
evidence or a required-premise row as required by `REPAIR_PREREGISTRATION.md`.

## Frozen field-mutation map

Replace the promotion-label mechanism with these direct mutations of a deep-copied evidence state:

| Hostile case | Exact evidence/premise mutation | Required named failure |
|---|---|---|
| static zero is material edge | `statuses[positive_static_zero...].status := MATERIAL_EDGE` | `material_edge_contradicts_regular_global_overlap` |
| compact domain supplies target | `requirements[fixed_physical_S2_target].status_after_G305 := DERIVED_FROM_COMPACT_DOMAIN` | `physical_target_has_no_owned_prerequisite` |
| Hopf existence selects history | `requirements[physical_history_selection].status_after_G305 := DERIVED_FROM_HOPF_EXISTENCE` | `history_selection_not_implied_by_map_class_existence` |
| integer fixes curvature | `requirements[curvature_magnitude_mass_or_Xmax].status_after_G305 := DERIVED_FROM_HOPF_INTEGER` | `scale_blind_integer_cannot_fix_curvature_magnitude` |
| ordinary `R3` has Hopf integer | `topology[R0_zero].ordinary_map_class_to_S2 := Z_WITHOUT_BASEPOINT` | `ordinary_R3_requires_extra_basepoint_or_compactification` |
| old action is metric-derived | `requirements[covariant_action].status_after_G305 := DERIVED_FROM_METRIC` | `no_metric_owned_action_in_requirement_ledger` |
| result covers all quotients | `production.scope := ALL_QUOTIENTS_AND_TOPOLOGY_CHANGE` | `promotion_exceeds_standard_simply_connected_scope` |
| algebraic radius is physical `Xmax` | `statuses[curvature_magnitude_mass_or_physical_Xmax].status := DERIVED_PHYSICAL_XMAX` | `physical_Xmax_ownership_absent` |
| kinematic persistence is conservation | `requirements[time_live_dynamics_or_conservation].status_after_G305 := DERIVED_DYNAMICAL_CONSERVATION` | `kinematic_product_slicing_is_not_dynamical_conservation` |
| celestial screen is internal target | mutate both `fixed_physical_S2_target := DERIVED_FROM_CELESTIAL_SCREEN` and `local_frame_gauge_descent := DERIVED_FROM_CELESTIAL_SCREEN` | `celestial_screen_lacks_internal_target_and_gauge_descent` |

The result artifact must record each changed field, its before value, and its after value. The clean
baseline must pass the same validator. A separate corrupted-baseline probe must still be detected.

## Frozen scope and landing

This is an evidence-test repair only. R1 and R2 are accepted by the external reviewer. Production
remains 77 assertions, Hopf integer remains `-1`, and the metric, kernel, topology census, premise
grades, and bounded scientific landing may not change.

## Acceptance contract

1. No `promotions` set or label-only catch remains.
2. Every hostile case changes at least one actual field in `production`, `independent`, `topology`,
   `requirements`, or `statuses`.
3. Every mutation produces its preregistered named failure; the clean baseline produces none.
4. The JSON artifact records all ten mutation paths and before/after values.
5. Package, premise-registry, sealed-layout, and full repository checks pass unchanged.
6. A final repair-only external reviewer confirms this exact R3 completion and unchanged landing.
