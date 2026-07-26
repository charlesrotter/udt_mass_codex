# Macro phi–angular–Xmax extension atlas — preregistration

Date: 2026-07-25

Base commit: `3ff555b4a48a70067313afef0cf10eba2e17fd49`

Status: preregistered before constructing the new cross-product atlas or evaluating its new witnesses. This is a source-led, non-blind audit: the controlling reports and ledgers named below were read before this preregistration, but their branch-by-extension cross-product and the two modulation-channel tests have not yet been generated.

## Whole question and bounded regime

Across the twelve already registered finite-cell completion classes, test each of the seven free directions in the most general pointwise lower-triangular extension of the founded reciprocal clock/ruler pair. Determine separately whether a direction can:

1. change the local observer-rest depth norm `B = h^{-1}(dphi,dphi)` and therefore a conditional distance law `D(phi)`;
2. change transverse or global observer-pair distances without changing that local aligned-depth norm; or
3. fail to descend through the stated global completion.

The audit is algebraic and finite-cell structural. It does not solve a field equation, select a completion, or calculate a numerical `Xmax`.

## Frame

- Metric-led, not template-led.
- The founded reciprocal pair is fixed as
  `theta_clock = exp(-phi) c_E dt` and
  `theta_ruler = exp(phi) dchi`.
- The seven tested extension directions are the three independent entries of a lower-triangular angular `2 x 2` block and the four lower base-to-angular mixing entries. They are basis directions of the allowed extension space, not an assertion that nonlinear combinations factor independently.
- The twelve completion labels and their already registered topology/gluing data are taken without ranking or selecting one.

## Premise ledger

| Item | Status | Scope |
|---|---|---|
| founded reciprocal clock/ruler pair | `pinned-by-THEORY` | exact C0/C1 descendant recorded by the complete-coframe extension audit |
| Einsteinian `c_E` as observational clock/distance calibration | `pinned-by-THEORY` | founded pair only; no local variable-speed mechanism is added |
| seven extension directions | `free-and-explored` | complete pointwise lower-triangular extension basis |
| twelve finite-cell completion classes | `free-and-explored` | registered atlas classes; not claimed exhaustive over all topology |
| angular shape, trace, twist, mixing profiles | `free-and-explored` | no round sphere or carrier is assumed |
| alignment `phi = phi(chi)` | `free-and-explored` | tested as a conditional subcase, never silently imposed globally |
| boundary/gluing data | `free-and-explored` | inherited as open where the completion atlas leaves them open |
| action, source, carrier, density, field equation | absent | no GR, EH, Bach, `S^2`, matter, or bootstrap dynamics imported |
| numerical scale and `Xmax` value | absent | no fit, cutoff, or observational inference |

## Exact preregistered algebraic tests

### T1 — aligned-depth invariance

For an observer-rest spatial lower-triangular coframe

```text
A = [[w, 0, 0],
     [l2, r, 0],
     [l3, e, t]],       h = A^T A,
```

and an aligned scalar `dphi = p dchi`, independently compute

```text
B = dphi^T h^{-1} dphi.
```

The preregistered expected identity is `B = (p/w)^2`: lower angular and mixing entries may tilt the orthonormal spatial coframe but cannot change the norm of a covector confined to the first coordinate in this triangular chart. A contrary symbolic result falsifies this expected identity.

### T2 — non-aligned modulation witness

Construct a smooth local witness with angular dependence in `phi`, calculate `B` on a fixed `phi` level, and test whether `B` varies along that level. The intended witness is only a counterexample to automatic transnormality. It must not be called a selected UDT branch.

### T3 — local versus global channel separation

For every extension direction, classify separately:

- effect on aligned local `B`;
- possible effect on non-aligned local `B`;
- possible effect on transverse/level-set distance or global diameter;
- global descent status in each finite-cell completion.

No change in global diameter may be reported as a derivation of feedback into the scalar `phi` law.

### T4 — branch-by-extension atlas

Generate exactly `12 x 7 = 84` primary rows. Every row must cite its completion evidence, direction definition, local status, global status, and unresolved condition. Missing or duplicate pairs fail verification.

## Falsification and certification contract

The verifier must fail if:

1. the atlas does not contain exactly one row for every completion/direction pair;
2. any row promotes an open completion datum to selected or derived;
3. aligned-depth `B` is reported as angularly modulated contrary to the independently simplified inverse-metric calculation;
4. a non-aligned witness is mislabeled universal or selected;
5. global diameter modulation is conflated with local `D(phi)` modulation;
6. a cap, quotient, mirror, monodromy, or seam is declared globally compatible without the descent data required by its controlling source;
7. an `Xmax` number, action, source, carrier, density, or dynamics is introduced;
8. a source file or frozen package changes.

Load-bearing algebra will be recomputed by a second script that does not import the atlas builder. Structural catches will be exercised by deliberately corrupting temporary copies.

## Maximum allowed conclusion

At most this audit may establish:

- exact local identities for how the allowed coframe extension enters `B`;
- conditional modulation channels for aligned and non-aligned `phi`;
- a branch-by-extension compatibility/status atlas; and
- the smallest remaining metric or global datum needed to turn a conditional observer-pair depth into a finite asymptotic separation.

It may not claim a selected angular completion, feedback equation for `phi`, complete observer-pair clock law, numerical or unique `Xmax`, bootstrap closure, matter emergence, action, source, carrier, cosmology, or canon.

## Controlling sources to freeze

- `udt_founded_phi_complete_coframe_extension_audit_2026-07-25/EXTENSION_CLASS_LEDGER.tsv`
- `udt_founded_phi_complete_coframe_extension_audit_2026-07-25/AUDIT_REPORT.md`
- `udt_metric_native_observer_separation_asymptote_audit_2026-07-24/EXACT_DERIVATION.md`
- `udt_metric_native_observer_separation_asymptote_audit_2026-07-24/AUDIT_REPORT.md`
- `udt_xmax_observer_separation_audit_2026-07-24/AUDIT_REPORT.md`
- `udt_two_observer_separation_selector_audit_2026-07-24/COMPLETION_DESCENT_ATLAS.tsv`
- `udt_finite_cell_completion_atlas_2026-07-21/COMPLETION_AXIS_SCHEMA.tsv`
- `udt_finite_cell_completion_atlas_2026-07-21/GLOBAL_OUTPUT_ATLAS.tsv`
- `udt_angular_generator_branch_census_2026-07-23/BRANCH_GENERATOR_ATLAS.tsv`
- `udt_angular_generator_branch_census_2026-07-23/BRANCH_UNIVERSE.tsv`
- `udt_global_reciprocal_persistence_selector_audit_2026-07-23/AUDIT_REPORT.md`

