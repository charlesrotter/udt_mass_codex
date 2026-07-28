# Clean-room metric-reduction readiness audit

Date: 2026-07-27

Grade: **VERIFIED-WITH-CAVEATS**.

## Result first

The current UDT metric closes exact ODEs for transport **through a supplied
configuration**. It does not close an ODE that determines the configuration or
a `1+1` time-live system that evolves it.

This was derived without opening, importing, or executing any previous ODE or
time-live implementation or result.

In the current bounded complete-coframe chart, all eight amplitudes have
independent metric tangents. `phi` is embedded as the founded reciprocal-pair
depth; it is not counted as an additional native scalar. Its realized profile
and the seven complete-extension directions remain unselected.

Exact closure census:

```text
cohomogeneity-one live profile directions              8
metric-supplied profile equation rank                   0
profile closure deficit                                 8

1+1 time-principal directions                           8
metric-supplied evolution principal rank                0
evolution closure deficit                               8
```

Therefore neither a background ODE solve nor a time-live metric solve is
currently authorized.

## Why familiar geometric equations do not close it

The torsion-free first Cartan equation is an exact `24 x 24` system of rank 24.
Those equations determine the 24 metric-connection coefficients from a supplied
coframe and its first jets. They supply zero equations for the eight coframe
profiles.

The second Cartan equation defines curvature from that connection. Bianchi and
Maurer-Cartan relations are identities. The exact noncommuting `1+1` control

```text
E=[[1+t x,t],[x,1]], det(E)=1
```

has identically zero Maurer-Cartan residual while retaining arbitrary `t,x`
dependence. Thus an integrability identity cannot be counted as the absent
evolution law.

## What can honestly be integrated now

Given a sufficiently smooth metric and the required query data, four pathwise
systems close exactly:

| system | first-order state/equation rank | scope |
|---|---:|---|
| geodesic | `8/8` | supplied metric and initial event/tangent |
| ambient parallel transport | `4/4` | supplied metric, path, and vector |
| projected screen transport | `2/2` | supplied intrinsic screen stratum, path, and vector |
| Jacobi transport | `8/8` | supplied metric, geodesic, curvature, and initial separation data |

These can map bending, focusing, caustics, screen rotation, mixing, and
holonomy. They do not form or evolve the background metric.

## Complete registered candidate census

All 15 preregistered system classes are classified in `SYSTEM_OUTCOMES.tsv`.
Exactly four are conditionally executable, and all four are kinematic path
systems on supplied configurations. Background profile, time-live, curvature-
prescription, bootstrap-density, carrier, and free-boundary systems remain open
or unselected. Cartan evaluators and Bianchi identities remain explicitly
non-dynamical. Legacy systems remain quarantined pending the post-verdict
provenance comparison.

## Interpretation

This confirms that coarse numerics can help us **see the geometry**, but only
if their role is stated honestly. We can sample the complete off-shell coframe
and integrate transport through each sample. We cannot call those samples
solutions or relaxation/time histories.

The repeated algebraic seam is real: the metric maps a coframe to connection,
curvature, transport, and holonomy, but the current premise set does not yet
supply the response that selects one complete coframe history.

## Four evidence gates

1. **Preregistered:** yes, commit `a4c11fc`, before the exact rank derivation.
2. **Full or bounded:** complete for the eight-amplitude bounded chart, the
   tested cohomogeneity-one and `1+1` reductions, 15 registered candidate
   classes, and four pathwise systems. It is not every topology, higher-jet,
   nonlocal, or future closure law.
3. **Independent:** a separate Python-standard-library/Fraction implementation
   reconstructs ranks `8`, `8`, and `24` without SymPy or production imports.
   Eighteen exercised false-promotion mutations all fail closed. No fresh
   zero-context external-model review was used, so the grade retains a caveat.
4. **Premises:** founded `phi`, extension directions, `c_E`, inactive strong
   CSN, symmetry reductions, action, source, carrier, bootstrap, boundary,
   path data, and legacy quarantine are separately stamped.

Exact evidence:

```text
production result SHA-256:
323684180f547edfa956f8ab6ee5a84bee4ad9ce19c8c4da0caaa8f51d19c8c5

independent result SHA-256:
13c7731193895ab0c3116eac59309da44d0edbaecfea1411c8cc37467037cc86

system outcomes SHA-256:
17c0c41e634aaec4f59655a571a12172ca65ae3c3dc02f40827f1d0209d149e1
```

## Authority boundary

No extension, profile, branch, topology, boundary, action, source, carrier,
density, bootstrap law, `X_max`, mass, or physical dynamics was selected. No
legacy solver or GPU work was run. `LIVE.md`, `CANON.md`, frozen evidence, and
the unrelated dirty checkout were not modified.

Maximum conclusion:

`REGISTERED_CURRENT_METRIC_KINEMATICS_CLOSE_PATHWISE_TRANSPORT_ON_SUPPLIED_CONFIGURATIONS_BUT_DO_NOT_CLOSE_A_BACKGROUND_PROFILE_OR_TIME_LIVE_SYSTEM`.
