# G281 SNe validation provenance reconstruction audit

Date: 2026-08-27

## Bounded landing

```text
NO_COMPLETE_NATIVE_SNE_PREDICTION_IN_AUDITED_NONPROTECTED_LINEAGE
__DIRECT_RECIPROCAL_REDSHIFT_SURVIVES
__COMPLETE_METRIC_OPTICAL_EVALUATOR_SURVIVES_CONDITIONALLY
__OLD_HEADLINE_FIT_USED_A_SUPPLIED_PROFILE_AND_WRONG_ONE_FACTOR_TRANSFER
__P1_IS_AN_EMPIRICAL_PROFILE_FAMILY_NOT_THE_RECIPROCAL_KERNEL
__G236_G278_ARE_RECONSTRUCTION_CALIBRATION_AND_HOLDOUT_WITH_DECLARED_IMPORTS
__G279_NATIVE_CORE_PURITY_STANDS
__G280_LOCATES_THE_MISSING_OBJECT_IN_COMPLETE_HISTORY_AND_OPTICAL_AREA
```

This is a source-bounded regrade of 32 tracked, immutable, non-protected historical/evidentiary
files and 24 historical claim tiles. Live startup authorities are checked separately during
repository closure and are not counted as sealed scientific sources. This is not a statement about
excluded protected local packages, and it does not create a new history, transfer law, scale, or
`X_max` value.

## Direct answer to the audit question

The old SNe work was not all fake, and the current kernel is not being silently refitted.

Three different activities had repeatedly been called “validation”:

1. **native conditional evaluation** — a supplied complete metric and observer query determine
   redshift and optical response;
2. **empirical profile reconstruction or calibration** — SNe data determine or calibrate a
   relation such as `R(phi)`;
3. **prediction** — a metric-owned history and query determine the full SNe curve before SNe data
   are inspected.

The first activity is genuine and survives. The second is legitimate when labeled empirical. The
audited lineage does not yet contain the third.

## The exact layer separation

For the declared stationary endpoint-frequency query, the reciprocal structure supplies

\[
Z \equiv 1+z = e^{\Delta\phi}.
\]

For a supplied complete metric history and null bundle, the metric supplies an optical/Jacobi area
and therefore an angular-diameter distance `d_A`. In the supplied central spherical primary chart,

\[
d_A=R,
\]

where `R` is areal radius. This is exact but conditional on that history and query.

The current temporary transparent-transfer import supplies

\[
d_L=Z^2d_A.
\]

Thus a numerical SNe curve needs the composed map

\[
z\longmapsto \phi=\log(1+z)
\longmapsto \text{complete history/null bundle}
\longmapsto d_A
\longmapsto d_L.
\]

The founded reciprocal kernel owns the first arrow. A supplied complete metric owns the middle
optical evaluation. The audited lineage does not yet derive the complete physical history that
turns `phi` into one unique `d_A(phi)` curve. G280 proves that the missing arrow cannot universally
be replaced by “projective position is optical area”: the same complete projective pair state can
have different native Jacobi areas.

## What the old canonical-geometry view got right

`udt_canonical_geometry.md` retains two important insights:

- the reciprocal static-spherical metric makes redshift a direct function of endpoint `phi`;
- in a central spherical history, the angular sector makes the chart radius an areal radius.

Those are not discarded. The framing error was joining them as though the metric form itself also
selected the numerical profile `phi(R)`. The document inserted the locked Branch-C cubic, inverted
it to obtain `R(z)`, used a one-factor luminosity rule `d_L=ZR`, and called the result a zero-parameter
metric prediction. The source itself elsewhere admits that the polynomial basis was a chosen
representation rather than a field-equation solution.

The July optics audit then proved the one-factor rule was short one factor of `Z`; under the
temporary transparent-transfer assumptions the correct relation is `d_L=Z^2R`. The old headline
score therefore remains a reproducible numerical result of its historical stack, but not evidence
for a native UDT SNe prediction.

## What happened to P1

The August M2/M3 lineage compared a chosen profile menu `P1/P2/P3`. P1 scored much better than P2
or P3, with the registered primary result

```text
chi2 = 1260.8480887040496
ndof = 1365
fitted inverse-n shape = 0.9470295666076658
```

That is real evidence that P1 is a useful empirical profile family inside the tested interface. It
does not show that P1 is part of the reciprocal kernel or is selected by the metric. Later G112,
G117, G120, G125, and G185 retyped and replayed the same result without changing that provenance.
G189 finally removed P1 from the kernel and showed that a coefficient-free projective-position
control does not automatically replace it.

## What the recent reconstruction accomplished

G236/G237 stopped pretending that the radial-area curve had already been predicted. They used two
processed SNe releases to reconstruct a finite-resolution relative `R(phi)` state while explicitly
excluding P1, `X_max`, an LCDM distance curve, and a profile optimizer. That is an empirical
reconstruction, not a prediction.

G278 then used the published Cepheid ladder and a declared optical/same-distance bridge to attach
one scale and tested DES without retuning. The holdout is useful robustness evidence:

- zero DES parameters were fitted;
- the kernel and reconstructed state shape were not retuned;
- P1 and `X_max` were absent;
- the DES holdout passed at each registered representation.

But the attached scale changes materially with numerical representation, and the preregistered
resolution gate fails. The correct grade remains a resolution-sensitive lead.

## Chronology result

The 24 claim tiles classify as follows:

| Current class | Count |
|---|---:|
| `NATIVE_CONDITIONAL_EVALUATION` | 7 |
| `REGRESSION_OR_COMPATIBILITY_CONTROL` | 7 |
| `EMPIRICAL_CALIBRATION` | 4 |
| `EMPIRICAL_RECONSTRUCTION` | 3 |
| `SUPERSEDED_OR_REPAIRED` | 2 |
| `SCAFFOLDED_OR_OVERCLAIMED` | 1 |
| `NATIVE_PREDICTION` | 0 |

The full row-by-row record is in `HISTORICAL_CLAIM_CENSUS.tsv`; the six prediction gates are applied
route-by-route in `ROUTE_PROVENANCE_MATRIX.tsv`. Its first gate now states explicitly what the
prediction/evaluator distinction already required: the history must be metric-owned or physically
selected and frozen before SNe. An arbitrary pre-SNe control such as G79 therefore remains a valid
conditional evaluator, not a native prediction.

## Framing repair

The native kernel has not become too abstract. Its abstraction exposed a conflation in the old
canonical treatment:

```text
reciprocal redshift state != areal radius != optical Jacobi area != luminosity transfer.
```

These objects can interlock through one complete metric history, but equality between them is not
automatic. Treating them separately is therefore a repair, not a departure from UDT.

The strongest salvage of the old SNe work is:

- `DERIVED_CONDITIONAL`: direct reciprocal redshift on the declared query;
- `DERIVED_CONDITIONAL`: complete metric/Jacobi optical evaluation on a supplied history;
- `OBSERVED_EMPIRICAL_RECONSTRUCTION`: G236/G237 relative area state;
- `OBSERVED/CONDITIONAL`: Cepheid scale attachment and DES holdout;
- `OPEN`: the metric-owned complete history or native areal/projective bridge that predicts the
  area curve independently of SNe.

## Stale-document finding

`udt_canonical_geometry.md` contains unmistakably stale “all derived” and “beats LCDM” language.
Because it is a fixed historical compatibility source, it should not be silently rewritten to
mimic the current state. G281 records the controlling regrades in `STALE_CLAIM_SCAN.tsv`. A separate
repository closure check—not part of the sealed 32-source scientific evidence—must keep the startup
surface pointed to G281 and treat the old monolith as historical evidence only.

## Verification

The following independent, consistency, or bounded checks passed:

- G281 source/hash, census, class, controller, and protected-boundary verifier;
- independent G281 layer and one-factor/two-factor cross-check;
- saved-output consistency replay across M3, G236, G237, G278, G279, and G280;
- July symbolic optics replay, confirming `d_L=Z^2d_A` under its stated assumptions;
- repository-recorded G279 no-write provenance derivation, 109,549-assertion independent replay,
  and 16/16 hostile mutation catches; these scripts were not rerun from the first G281 intake;
- repository-recorded G280 no-write derivation, 40,960-assertion independent neighboring-ray
  replay, and 8/8 hostile catches plus 10/10 repair mutations; these scripts were not rerun from the
  first G281 intake.

Fresh sealed external `gpt-5.4` review returned `ACCEPT-WITH-REPAIRS`, independently retained every
substantive classification and the bounded landing, and identified only source-scope, gate-wording,
replay-surface, and filename defects. Repairs R1--R4 are evidence/typing repairs; they change no
metric, kernel, history, transfer, score, or scientific conclusion.

A fresh sealed repair-only follow-up then returned `ACCEPT`. It verified all corrected intake
seals and payloads, R1--R4, and the four registered sealed replays; it found no remaining scoped
defect and retained the bounded landing unchanged. The exact return is banked in
`EXTERNAL_REPAIR_FOLLOWUP_REVIEW.md`.

## Next bounded scientific move

Do not fit another unrestricted SNe curve. Instead, preregister one metric-led attempt to derive the
missing complete-history/optical-area bridge without inspecting SNe outcomes. It must either:

1. produce a finite-dimensional `d_A(phi)` family from the complete metric and declared null query,
   after which Cepheids may calibrate constants and both SNe releases become tests; or
2. prove that the current premises cannot do so, identifying the smallest additional premise type.

Only after that bridge is frozen should a new SNe prediction score be computed.
