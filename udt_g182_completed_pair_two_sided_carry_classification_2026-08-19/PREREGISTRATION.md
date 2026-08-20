# G182 preregistration — completed-pair two-sided carry

Date: 2026-08-19

## Question and bounded regime

Classify when two **supplied** one-sided completed observer-pair families meeting at one finite
endpoint define one two-sided pair geometry. Both interiors are assumed smooth, regular, timelike,
and already normalized by the provisionally adopted completed-pair Dual Reciprocity rule. G182
does not select the branches or their physical population.

In each one-sided completed ruler chart,

\[
h_\pm=-T_\pm^2(d\tau_\pm+B_\pm dx_\pm)^2+T_\pm^{-2}dx_\pm^2,
\qquad x_\pm>0,
\]

with the approached seam at `x_+=x_-=0`. G181's finite regular endpoint conditions are assumed:
`T_± -> T_±0 in (0,infinity)` and `B_± -> B_±0 in R`.

The problem is metric-led. It asks what follows from the supplied completed pair metrics, supplied
endpoint calibration identification, and—when immersion carry is tested—the supplied ambient
metric/coframe and pair germs.

## Whole-space classification promised

1. Construct one signed completed coordinate from the two one-sided tape coordinates, retaining
   the relative spatial orientation and time-orientation/calibration identification explicitly.
2. Give necessary and sufficient `C^k` matching conditions for the completed pair metric for every
   finite `k`, and the corresponding `C^infinity` condition.
3. Separate scalar-depth matching from full metric matching; retain the normalized shift.
4. Determine whether the pair metric is sufficient for `C^1` or higher immersion carry.
5. Classify the stronger full pulled-back-coframe/pair-tangent matching condition.
6. Specialize at a regular positive-areal-radius primary spherical point and distinguish complete
   tangent matching from equality of tape density.
7. Register successful joins and counterexamples: depth-only mismatch, shift mismatch, metric-smooth
   but immersion-cusped, direction-rotated, and higher-jet/extrinsic mismatch.

## Premise ledger

| Item | Status for G182 |
|---|---|
| Completed-pair Dual Reciprocity after full pullback | `WORKING_FOUNDATIONAL_CLARIFICATION`; cited G176 |
| One-sided regular completed form and finite endpoint limits | `DERIVED_CONDITIONAL`; cited G179--G181 |
| Two supplied incident branches | `SUPPLIED`; free-and-classified, not selected |
| Endpoint incidence and common ambient point | `SUPPLIED` for immersion tests |
| Relative spatial orientation | `SUPPLIED_DISCRETE_CARRY`; both signs classified |
| Common time orientation and constant clock-origin identification | `SUPPLIED_CALIBRATION_CARRY`; time-reversed control kept separate |
| Smoothness order `k` | `FREE_AND_CLASSIFIED`; theorem for every finite `k` and infinity |
| Ambient coordinates/coframe for germ comparison | `SUPPLIED_CHART`; conclusions restated invariantly as jet equality |
| `c_E` | `OBSERVED` unit calibration only; no numerical value used |
| `X_max`, fits, action, source, matter, bootstrap, dynamics | inactive |

No coefficient, profile, boundary value, preferred path, or target response is pinned.

## Preregistered theorem candidates

Let a supplied carry put both sides into one signed completed chart `s`, with the seam at `s=0`,
and denote the carried coefficient germs by `(T_L,B_L)` and `(T_R,B_R)`.

- **M1.** The piecewise completed pair metric has a `C^k` nondegenerate Lorentzian extension in the
  carried calibration iff the one-sided jets of both `T` and `B` agree through order `k`.
- **M2.** `Phi=-log T` has a `C^k` extension iff the `T` jets agree; this alone is insufficient for
  metric carry because `B` can jump or kink independently.
- **M3.** In outward one-sided coordinates with common time orientation and signed coordinate
  `s=-x_-` on the left, `s=x_+` on the right, the raw jet laws are
  `T_+^(j)(0)=(-1)^j T_-^(j)(0)` and
  `B_+^(j)(0)=(-1)^(j+1) B_-^(j)(0)`.
- **M4.** Smooth matching of `h` is necessary but not sufficient for smooth matching of the
  immersion or complete pair germ. Equality of the complete coframe-valued tangent and its carried
  jets supplies the missing extrinsic/directional information.
- **M5.** At a regular spherical point, equality of
  `m^2=v^2+exp(-2 phi) r^2 b^2` does not imply equality of radial/angular tangent components;
  direction-rotated and cusp controls survive with identical completed scalar metrics.

Any failed candidate will be recorded rather than repaired after inspection.

## Falsification contract

The proposed bounded landing fails if any of the following occurs:

1. matching `T,B` jets is not sufficient to reconstruct matching metric jets;
2. a regular metric join forces the complete tangent/immersion jet uniquely;
3. the raw outward-coordinate parity law has the wrong sign at any derivative order;
4. a scalar-depth join automatically forces shift carry;
5. a registered direction/cusp witness cannot keep the completed pair metric fixed;
6. the conclusion requires an unregistered profile, coefficient, path, `X_max`, or external law.

## Evidence contract

- dependency-free exact production derivation;
- independent implementation using rational jets and finite exact algebra;
- preregistered mutation catches for dropped shift, wrong parity, scalar-to-metric promotion,
  Gram-to-tangent promotion, and cusp erasure;
- frozen source manifest;
- fresh read-only adversarial review before result banking.

## Maximum possible conclusion

At most, G182 may establish a necessary-and-sufficient **conditional two-sided matching theorem**
for supplied completed pair branches and sharply separate intrinsic pair-metric carry from full
pair-germ/immersion carry. It may not select a physical branch, global history, path, singularity,
`X_max`, observation, dynamics, action, source, matter, bootstrap, or signalling law.
