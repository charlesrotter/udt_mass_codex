# Fresh Adversarial Review — Pre-Correction Return

`FAIL for certification; the core nonselection conclusion survives after correction.`

- Coverage passes: all 23 preregistered sources are present, byte-identical to base `5457a36`, with
  380 total rows and no duplicate within-source keys.
- The 84 rows are exactly `7 motifs x 12 completion classes`. They are compatibility presentations,
  not 84 solved universes.
- There is one conditional reciprocal-toric metric control, repeated across 12 presentation rows—not
  12 distinct connector solutions. Correct the counts to:
  - `conditional_control_presentations = 12`
  - `unique_conditional_metric_controls = 1`
- For that one static metric,
  `g=-c_E^2 dt^2+A^2 dphi^2+Omega^2(e^-2phi dxi1^2+e^2phi dxi2^2)`,
  the declared representative does give `N=1`, `B=0`. Along any fixed positive finite spatial path,
  null time is `L/c_E`, so its proper path rate is exactly `c_E`, independent of angular weight.
  This is an interior kinematic result, not a global information-transfer law.
- The 12 presentation rows do not all establish compatible global realizations:
  - `FC11_NONINTEGRABLE_DISTRIBUTION` conflicts with the control's commuting coordinate torus and
    should be `INCOMPATIBLE` unless explicitly reinterpreted.
  - General `FC07` `GL(2,Z)` monodromy is compatible only for a restricted metric-preserving subset.
  - `FC08`, `FC09`, and `FC10` require additional lift, parity, profile, or stratification checks.
  - No presentation is presently a fully supplied global connector.
- `FC06` is globally orbifold/singular by its registered nonprimitive-cap definition, but its
  interior optical rate remains finite at `c_E`. Do not imply that accessibility itself diverges or
  that metric degeneracy is mandatory; use
  `GLOBAL_ORBIFOLD_OR_SINGULAR_COMPLETION__INTERIOR_RATE_FINITE`.
- The generic connector algebra is correct:
  - determinant `-c_E^2 N^2 H^2`;
  - roots `c_E(-B+/-N/H)`;
  - fixed-path and shift formulas;
  - near-null-shift and bottleneck examples.
- The counterfamilies are valid connector examples, but they are not yet branch-preserving global
  completions. Changing lapse or shift can spoil cap, seal, or global regularity. Rename that scope
  and remove the misleading `branch_preserving_counterfamily_scope` claim unless a per-completion
  extension proof is added.
- Selector rulings are source-consistent: Reciprocity, CSN, finite cell, and seal constrain without
  selecting; bootstrap and density bootstrap remain open; none selects accessibility.

Required verification repairs:

1. Hash and cite the load-bearing toric metric source, preferably
   `udt_motif_hopf_correspondence_audit_2026-07-22/TORIC_CONTROL_RESULT.json`, plus the preceding
   two-frame connector source.
2. Replace tautological production checks such as `1==1` and `1/d==1/d` with computations from
   `N=F D`, `H=1/D`.
3. Independently verify unique-control versus presentation counts, compatibility grades, `FC06`'s
   two separate statuses, and every counterfamily formula.
4. Add catches for missing control provenance, "12 controls" inflation, `FC11` false compatibility,
   `FC06` optical/global conflation, and branch-preserving overclaim.
5. Add a real cross-source overlap/equivalence map; 380 is an evidence-row census, not a unique-branch
   count.

Maximum honest conclusion:

> The retained 380-row evidence census does not supply or select a complete global stationary
> connector. One conditional reciprocal-toric metric, shown in 12 compatibility presentations, has
> exactly `c_E` proper fixed-path null rate in its static representative. Global completion
> compatibility, threading outside that control, shift, path, and physical information transfer
> remain open.

Review conditions: fresh context; read-only; no repository edits or branch operations.
