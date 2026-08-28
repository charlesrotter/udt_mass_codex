# G289 audit report — native-kernel Hopfion compatibility and history restriction

Date: 2026-08-28
Grade: `EXTERNAL_REPAIRS_ACCEPTED__BOUNDED_LANDING_UNCHANGED`

## Landing

```text
LOCAL_NULL_DIRECTION_EMBEDDING_EXISTS
__FIXED_ROUND_S2_HOPFION_REQUIRES_SUPPLIED_FRAME_TARGET_AND_BOUNDARY
__RAW_HOPF_CLASS_DOES_NOT_DESCEND_THROUGH_FULL_LOCAL_FRAME_GAUGE
__CONFORMAL_HISTORY_TWINS_CARRY_THE_SAME_NULL_TEXTURE
__STATIC_HOPFION_IS_CONDITIONALLY_COMPATIBLE_NOT_A_CURRENT_HISTORY_SELECTOR
```

## Result

There is a real compatibility bridge. Relative to a supplied observer and orthonormal spatial frame,
every historical unit-vector Hopf configuration defines a section of the metric's projectivized
null cone. This works on every regular primary profile, including G288's center class. The earlier
Hopfion is therefore not algebraically foreign to the native kernel.

The bridge stops before native ownership. The metric supplies a celestial conformal `S2`; the old
stability functional uses a fixed round target. A boost preserves null directions but rescales
round-target tangent norms by a direction-dependent factor. More decisively, a basepoint-fixed large
local frame rotation can turn a constant component direction into the standard unit Hopf map.
Therefore the raw component Hopf number does not descend through the kernel's full frame gauge
without a framing, restricted gauge class, or connection-dependent completion.

Compatibility also does not constrain history. The exact regular family
`g_alpha=exp(2 alpha r^2) eta` carries the same null-line texture for every `alpha`, while
`R(0)=-36 alpha`. The orthonormal embedding is likewise valid for every positive primary `f(r)`.
No current kernel-owned condition rejects a member.

## Earlier stability work

The corrected no-null result remains `SETTLED_STATIC_FINITE_BOX_CONDITIONAL`. It is
compatible after supplying the observer/frame, round carrier, `L2+L4` action, constant exterior,
fixed boundary, and static background. G289 does not re-run or invalidate that result. It shows that
those supplied structures, rather than the native kernel alone, currently carry the stability and
topological-sector claims.

## Evidence

- preregistered and pushed at commit `1156e2a2` before outcome implementation;
- 17 freshly computed symbolic/algebraic/topological identities and 6 separately typed conclusion
  flags;
- implementation-distinct exact-Fraction assertions over 1,200 cases, including an independently
  reconstructed normalized Hopf connection integral and compactification-basepoint witness;
- both boost orientations and the zero orientation covered;
- 122 exact north/south Hopf-fiber controls;
- 5/5 hostile catches, including four primitive-recomputing geometric/topological overclaims;
- the complete 273-row scientific-premise registry and startup-surface audit pass;
- the full repository suite passes 194 tests with one expected `xfail`;
- no old result artifact imported and no GPU, fit, action, source, backreaction, mass, Planck scale,
  history, observation, or `X_max` inserted.

## Maximum conclusion

The older Hopfion is a viable conditional configuration-level passenger on the current kernel. It
is not yet a metric-derived carrier, a frame-gauge-invariant physical Hopf sector, or a selector of
metric history. A gauge-covariant framed/connection construction plus time-live persistence would
be the next bridge; it must distinguish a preregistered regular history pair to count as selection.

## External review and repairs

Fresh sealed external `gpt-5.4` review returned `ACCEPT_WITH_REPAIRS` and retained every part of the
bounded scientific landing. R1 restores the controlling static finite-box conditional status. R2
replaces hard-coded hostile witness outputs with primitive recomputations. R3 independently derives
the normalized Hopf connection integral and compactification basepoint. R4 separates 17 computed
identities from 6 conclusion flags. Those four repairs were submitted unchanged to repair-only review.

The sealed repair-only follow-up returned `REPAIRS_ACCEPTED` with no defects. G289 is closed at its
bounded compatibility/nonselection ceiling; gauge-covariant charge, time-live persistence,
backreaction, and any physical-history restriction remain open future questions.
